# Documentação de Testes

Este documento descreve os procedimentos de teste e validação para o sistema de download de imagens orbitais.

## 1. Requisitos para Testes

Para a execução dos testes, é necessário que o ambiente virtual esteja ativo e as dependências instaladas via `requirements.txt`. Além disso, o arquivo `.env` deve estar configurado com as credenciais válidas do Google Cloud e a chave JSON correspondente deve estar presente no diretório `secrets/`.

## 2. Testes de Unidade e Integração

### 2.1 Validação de Inicialização do GEE
O script `tests/test_gee_download.py` realiza a validação básica da conexão com o Google Earth Engine utilizando a conta de serviço configurada.

**Comando:**
```bash
python tests/test_gee_download.py
```

**Resultado esperado:**
- Logs indicando inicialização bem-sucedida.
- Geração de URLs de download para Sentinel e Landsat sem erros de permissão ou de geometria.

## 3. Testes Funcionais da CLI

A Interface de Linha de Comando (CLI) deve ser testada para diferentes cenários de download.

### 3.1 Download em Lote (Landsat)
Validar se o sistema baixa corretamente as imagens de semestres específicos para múltiplos anos.

**Comando:**
```bash
python cli.py --car PA-1504802-FCEA8FAD347340D8BD6D3143A9623468 --sat landsat --years 2023-2024 --semester 2
```

### 3.2 Download em Lote (Sentinel)
Validar se o sistema processa meses específicos e gera os arquivos GeoTIFF correspondentes.

**Comando:**
```bash
python cli.py --car PA-1504802-FCEA8FAD347340D8BD6D3143A9623468 --sat sentinel --years 2024 --months 6,7,8
```

## 4. Testes da Interface Gráfica (GUI)

Para testar a interface gráfica, deve-se iniciar o processo via terminal e interagir com os elementos visuais.

**Comando de inicialização:**
```bash
python gui.py
```

**Cenários de validação na interface:**
1. Alteração entre satélites: Verificar se os campos de período (Semestre/Meses) são atualizados dinamicamente.
2. Seleção de diretório: Validar se o botão "Procurar..." atualiza o caminho de saída.
3. Execução: Iniciar um download e monitorar os logs no console interno da aplicação.
4. Conclusão: Confirmar o aparecimento da caixa de diálogo informando o sucesso da operação.

## 5. Verificação de Saída de Dados

Após os testes, deve-se verificar se os arquivos foram salvos na estrutura de diretórios prevista:
`[OUTPUT_DIR]/[CODIGO_CAR]/[NOME_DO_ARQUIVO].tif`

As imagens devem ser válidas e passíveis de abertura em softwares de SIG como o QGIS.
