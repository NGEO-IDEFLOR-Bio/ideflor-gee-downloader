import customtkinter as ctk
import os
import sys
import threading
import logging
from datetime import datetime
from tkinter import filedialog, messagebox

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))

from gee_utils import initialize_gee, get_sentinel_image, get_landsat_image, get_download_url, download_image
from db_utils import get_car_geometry_db

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TextHandler(logging.Handler):
    """This class allows sending log records to a Tkinter Text widget."""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert('end', msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.see('end')
        self.text_widget.after(0, append)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IDEFLOR - Geo Downloader")
        self.geometry("900x700")

        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Geo Downloader", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Main Content
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- Section: Parameters ---
        self.param_label = ctk.CTkLabel(self.main_frame, text="Parâmetros de Download", font=ctk.CTkFont(size=16, weight="bold"))
        self.param_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # CAR Code
        self.car_label = ctk.CTkLabel(self.main_frame, text="Código do CAR (separe por vírgula para lote):")
        self.car_label.grid(row=1, column=0, sticky="w")
        self.car_entry = ctk.CTkEntry(self.main_frame, placeholder_text="PA-1504802-FCEA8FAD...", width=600)
        self.car_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.car_entry.insert(0, "PA-1504802-FCEA8FAD347340D8BD6D3143A9623468")

        # Satellite Selection
        self.sat_label = ctk.CTkLabel(self.main_frame, text="Selecione o Satélite:")
        self.sat_label.grid(row=3, column=0, sticky="w")
        self.sat_var = ctk.StringVar(value="Landsat")
        self.sat_option = ctk.CTkSegmentedButton(self.main_frame, values=["Landsat", "Sentinel"], 
                                                command=self.update_dynamic_fields, variable=self.sat_var)
        self.sat_option.grid(row=4, column=0, sticky="w", pady=(0, 10))

        # Year Selection
        self.year_label = ctk.CTkLabel(self.main_frame, text="Anos (ex: 2023 ou 2020-2024):")
        self.year_label.grid(row=5, column=0, sticky="w")
        self.year_entry = ctk.CTkEntry(self.main_frame, placeholder_text="2023-2024")
        self.year_entry.grid(row=6, column=0, sticky="w", pady=(0, 10))
        self.year_entry.insert(0, "2023-2024")

        # Dynamic Options Frame
        self.dynamic_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.dynamic_frame.grid(row=7, column=0, sticky="ew", pady=10)
        self.dynamic_frame.grid_columnconfigure(0, weight=1)
        
        self.update_dynamic_fields(self.sat_var.get())

        # Scale
        self.scale_label = ctk.CTkLabel(self.main_frame, text="Escala (metros):")
        self.scale_label.grid(row=8, column=0, sticky="w")
        self.scale_entry = ctk.CTkEntry(self.main_frame, placeholder_text="30 para Landsat, 10 para Sentinel")
        self.scale_entry.grid(row=9, column=0, sticky="w", pady=(0, 10))

        # Output Directory
        self.output_label = ctk.CTkLabel(self.main_frame, text="Pasta de Saída:")
        self.output_label.grid(row=10, column=0, sticky="w")
        self.output_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.output_frame.grid(row=11, column=0, sticky="ew")
        
        from dotenv import load_dotenv
        load_dotenv()
        self.output_path_var = ctk.StringVar(value=os.getenv('OUTPUT_DIR', 'downloads'))
        self.output_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_path_var, width=400)
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.browse_button = ctk.CTkButton(self.output_frame, text="Procurar...", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1)

        # --- Section: Actions ---
        self.download_button = ctk.CTkButton(self.main_frame, text="INICIAR DOWNLOAD", command=self.start_download_thread,
                                           height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.download_button.grid(row=12, column=0, pady=20, sticky="ew")

        # Progress
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.grid(row=13, column=0, sticky="ew", pady=(0, 10))
        self.progress_bar.set(0)

        # Log Terminal
        self.log_text = ctk.CTkTextbox(self.main_frame, height=200)
        self.log_text.grid(row=14, column=0, sticky="ew")
        self.log_text.configure(state='disabled')

        # Setup Logging redirection
        self.logger = logging.getLogger('gee_utils')
        handler = TextHandler(self.log_text)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def update_dynamic_fields(self, sat):
        # Clear dynamic frame
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        if sat == "Landsat":
            lbl = ctk.CTkLabel(self.dynamic_frame, text="Selecionar Semestre:")
            lbl.grid(row=0, column=0, sticky="w")
            self.semester_var = ctk.StringVar(value="Ambos")
            self.semester_option = ctk.CTkOptionMenu(self.dynamic_frame, values=["1º Semestre", "2º Semestre", "Ambos"], variable=self.semester_var)
            self.semester_option.grid(row=1, column=0, sticky="w")
        else: # Sentinel
            lbl = ctk.CTkLabel(self.dynamic_frame, text="Meses (separados por vírgula):")
            lbl.grid(row=0, column=0, sticky="w")
            self.months_entry = ctk.CTkEntry(self.dynamic_frame, placeholder_text="6,7,8")
            self.months_entry.grid(row=1, column=0, sticky="w")
            self.months_entry.insert(0, "6,7,8")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path_var.set(directory)

    def start_download_thread(self):
        # Basic validation
        if not self.car_entry.get() or not self.year_entry.get():
            messagebox.showerror("Erro", "Campos de CAR e Anos são obrigatórios.")
            return

        self.download_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        thread = threading.Thread(target=self.run_process)
        thread.daemon = True
        thread.start()

    def run_process(self):
        try:
            # Gather inputs
            cars = [c.strip() for c in self.car_entry.get().split(',')]
            years_raw = self.year_entry.get()
            sat = self.sat_var.get().lower()
            output_dir = self.output_path_var.get()
            
            years = []
            if '-' in years_raw:
                start, end = map(int, years_raw.split('-'))
                years = list(range(start, end + 1))
            else:
                years = [int(y) for y in years_raw.split(',')]

            # Scale
            scale_val = self.scale_entry.get()
            if not scale_val:
                scale = 10 if sat == 'sentinel' else 30
            else:
                scale = int(scale_val)

            # Initialize GEE
            initialize_gee()

            for i, car in enumerate(cars):
                self.logger.info(f"\n🌍 Processando CAR: {car}")
                try:
                    region = get_car_geometry_db(car)
                except Exception as e:
                    self.logger.error(f"  ❌ Erro ao buscar geometria: {e}")
                    continue

                car_dir = os.path.join(output_dir, car)
                os.makedirs(car_dir, exist_ok=True)

                for year in years:
                    if sat == 'sentinel':
                        months_raw = self.months_entry.get()
                        months = [int(m) for m in months_raw.split(',')] if months_raw else [6]
                        for month in months:
                            self.logger.info(f"  📅 {year}-{month:02d} (Sentinel)")
                            img = get_sentinel_image(region, year, month, month)
                            if img:
                                url = get_download_url(img, region, scale=scale)
                                filename = f"Sentinel_{year}_{month:02d}.tif"
                                download_image(url, os.path.join(car_dir, filename))
                    else:
                        sem_choice = self.semester_var.get()
                        semesters = [1] if sem_choice == "1º Semestre" else [2] if sem_choice == "2º Semestre" else [1, 2]
                        for sem in semesters:
                            self.logger.info(f"  📅 {year} S{sem} (Landsat)")
                            img, bands = get_landsat_image(region, year, sem)
                            if img:
                                url = get_download_url(img, region, scale=scale)
                                filename = f"Landsat_{year}_S{sem}.tif"
                                download_image(url, os.path.join(car_dir, filename))

            self.logger.info("\n✨ Processo concluído!")
            self.after(0, lambda: messagebox.showinfo("Sucesso", "Download(s) concluído(s) com sucesso!"))

        except Exception as e:
            self.logger.error(f"Erro crítico: {e}")
            self.after(0, lambda: messagebox.showerror("Erro", str(e)))
        
        finally:
            self.after(0, self.reset_ui)

    def reset_ui(self):
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.download_button.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
