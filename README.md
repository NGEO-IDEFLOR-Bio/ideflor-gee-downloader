# IDEFLOR - Sistema de Download de Imagens Orbitais

Este repositório fornece ferramentas para a automatização do processo de download de imagens dos satélites Landsat e Sentinel via Google Earth Engine (GEE). O sistema foi desenvolvido para operar localmente, oferecendo interfaces de linha de comando (CLI) e gráfica (GUI).

## 1. Estrutura do Projeto

A organização dos diretórios e arquivos principais é detalhada a seguir:

- `cli.py`: Interface de Linha de Comando para processamento em lote.
- `gui.py`: Interface Gráfica baseada em CustomTkinter.
- `scripts/`:
    - `gee_utils.py`: Módulos de integração com a API do Google Earth Engine.
    - `db_utils.py`: Utilitários para consulta de geometrias de áreas de interesse.
- `secrets/`: Diretório destinado ao armazenamento de chaves JSON de Contas de Serviço (não versionado).
- `downloads/`: Diretório padrão para armazenamento dos arquivos GeoTIFF resultantes.

## 2. Configuração do Ambiente

### 2.1 Requisitos de Software
- Python 3.x
- Dependências listadas em `requirements.txt`

### 2.2 Guia de Configuração
Para instruções detalhadas sobre a criação da Conta de Serviço no Google Cloud, habilitação das APIs e configuração das variáveis de ambiente, consulte o arquivo [CONFIGURACAO.md](CONFIGURACAO.md).

### 2.3 Credenciais do Google Earth Engine
O sistema utiliza Contas de Serviço para autenticação. É necessário configurar o arquivo `.env` na raiz do projeto baseado no modelo em `env.example`.

## 3. Interfaces de Operação

### 3.1 Interface de Linha de Comando (CLI)
A CLI permite a execução de downloads automatizados para múltiplos anos e áreas.

**Sintaxe Básica:**
```bash
python cli.py --car [CODIGO_CAR] --sat [landsat|sentinel] --years [INTERVALO_ANOS]
```

**Exemplo de uso (Landsat):**
```bash
python cli.py --car PA-1504802-FCEA8FAD... --sat landsat --years 2023-2024 --semester 2
```

### 3.2 Interface Gráfica (GUI)
A GUI oferece um ambiente visual intuitivo para usuários que preferem não utilizar o terminal.

**Acionamento:**
```bash
python gui.py
```

A interface adapta-se dinamicamente ao satélite selecionado, permitindo a definição de semestres para Landsat ou meses específicos para Sentinel.

## 4. Testes e Validação

Para informações detalhadas sobre como validar a instalação e o funcionamento das ferramentas, consulte o arquivo [TESTES.md](TESTES.md).

## 5. Notas de Segurança
O diretório `secrets/` e o arquivo `.env` contêm informações sensíveis e não devem ser incluídos em sistemas de controle de versão. Este projeto já possui as devidas exclusões configuradas.
