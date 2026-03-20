# IDEFLOR - Geo Downloader (Plugin QGIS)

Ferramenta universal para automação do download de imagens orbitais (Landsat e Sentinel) via Google Earth Engine (GEE), integrada diretamente ao QGIS.

## 1. Estrutura do Projeto

- `ideflor_gee_downloader/`: Pasta principal do Plugin do QGIS.
    - `scripts/`: Lógica de GEE.
    - `secrets/`: Chaves JSON de Contas de Serviço (não versionado).
    - `.env`: Configurações de acesso ao GEE (não versonado).
- `requirements.txt`: Dependências Python.

## 2. Configuração e Instalação

### 2.1 O Plugin do QGIS
1. Siga as instruções de configuração da Conta de Serviço do Google em [CONFIGURACAO.md](CONFIGURACAO.md).
2. Copie a pasta `ideflor_gee_downloader` para o diretório de plugins do seu perfil do QGIS (`%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`).
3. Ative o complemento em **Gerenciar e Instalar Complementos**.

### 2.2 Requisitos
Instale as dependências no Python do QGIS (OSGeo4W Shell):
```bash
python -m pip install earthengine-api requests python-dotenv
```

## 3. Funcionalidades

- **Busca por Área Geográfica**: Use a extensão atual do seu mapa ou de qualquer camada (Vetor/Raster) do projeto.
- **Sentinel-2 Flexível**: Downloads semestrais ou mensais específicos.
- **Landsat**: Downloads semestrais.
- **Integração Visual**: Os arquivos baixados (GeoTIFF) são carregados automaticamente no QGIS.

## 4. Desenvolvedor

**Samuel Santos (IDEFLOR)**
- [LinkedIn](https://www.linkedin.com/in/samuelsantos-amb/)
- [GitHub](https://github.com/samuel-c-santos)
- [Site Pessoal](https://samuelsantos.site/)
