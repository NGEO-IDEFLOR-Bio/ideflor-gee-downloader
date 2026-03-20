import os
try:
    path = r"h:\Meu Drive\IDEFLOR\plugin-landsat\cli.py"
    if os.path.exists(path):
        os.remove(path)
        print("Deletado com sucesso via Python")
    else:
        print("Arquivo não encontrado")
except Exception as e:
    print(f"Erro: {e}")
