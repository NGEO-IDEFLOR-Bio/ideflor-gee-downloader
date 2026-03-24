# IDEFLOR - Geo Downloader (Plugin QGIS) - v2.0 Híbrido 🛰️

Ferramenta universal para o IDEFLOR que combina dados globais do **Google Earth Engine** (Landsat/Sentinel) e dados nacionais de alta resolução do **INPE** (CBERS-4A).

## 1. Estrutura do Projeto

- `ideflor_gee_downloader/`: Pasta do Plugin para QGIS 3.44+.
    - `scripts/`: Lógica de integração GEE e INPE STAC.
    - `secrets/`: Chaves JSON de Contas de Serviço (não versionado).
    - `.env`: Configurações de acesso (GEE e Credenciais INPE).
- `requirements.txt`: Dependências Python (cbers4asat, rasterio, geopandas, etc).

## 2. Configuração e Instalação

### 2.1 O Plugin do QGIS
1. Siga o guia completo em [COMO_INSTALAR.md](COMO_INSTALAR.md).
2. **Instalação Automática**: O plugin possui um botão interno ("FORÇAR REINSTALAÇÃO") que instala todas as dependências complexas (geopandas, rasterio) diretamente no QGIS, resolvendo conflitos de ambiente.

## 3. Funcionalidades de Elite

- **CBERS-4A (WPM 2m/8m)**: Acesso direto ao catálogo do INPE com download, composição RGBN e recorte automático por AOI.
- **Sentinel-2 & Landsat (GEE)**: Processamento em nuvem para séries históricas e mosaicos semestrais/mensais.
- **Reprojeção Automática**: O plugin detecta o sistema de coordenadas e converte a área de interesse (AOI) para o sistema nativo do satélite antes do recorte.
- **Buffer/Borda Flexível**: Aumente a área de interesse para visualizar o contexto da vizinhança.
- **Integração Visual**: Carregamento automático de GeoTIFFs no QGIS com reamostragem cúbica para melhor visualização.

## 4. Desenvolvedor

**Samuel Santos (IDEFLOR)**
- [LinkedIn](https://www.linkedin.com/in/samuelsantos-amb/)
- [GitHub](https://github.com/samuel-c-santos)
- [Site Pessoal](https://samuelsantos.site/)
