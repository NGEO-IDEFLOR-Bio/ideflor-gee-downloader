# Guia de Instalação: IDEFLOR Geo Downloader (QGIS)

Este guia descreve os passos necessários para instalar e ativar o plugin de download de imagens orbitais (Landsat, Sentinel e CBERS-4A) no seu QGIS.

## 1. Preparação da Pasta

O plugin é fornecido como uma pasta chamada `ideflor_gee_downloader`. Dentro desta pasta, as configurações de acesso (arquivo `.env` e chaves na pasta `secrets`) já devem estar configuradas para a conta do IDEFLOR.

### Passos:
1. Localize a pasta de plugins do seu perfil do QGIS no Windows:
   *   Pressione `Win + R` e cole o seguinte caminho:
       `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
2. Copie a pasta inteira `ideflor_gee_downloader` para dentro deste diretório.

## 2. Instalação de Dependências (Obrigatório)

O plugin utiliza bibliotecas avançadas (Google Earth Engine e INPE) que não vêm por padrão no QGIS. Você tem duas formas de instalar:

### Opção A: Pelo próprio Plugin (Recomendado ⭐)
1. Abra o QGIS e ative o plugin (veja o item 3 abaixo).
2. Se aparecer um **Botão Laranja** escrito `⚠️ Erro nas ferramentas CBERS`, clique em **"FORÇAR REINSTALAÇÃO CBERS"**.
3. Aguarde o aviso de sucesso e **reinicie o QGIS**.

### Opção B: Pelo OSGeo4W Shell (Manual)
1. Feche o QGIS.
2. No menu Iniciar, procure por **OSGeo4W Shell** e execute como **Administrador**.
3. Cole o comando:
   ```bash
   python -m pip install --upgrade --force-reinstall cbers4asat rasterio geopandas shapely scikit-image geomet geojson "numpy<2.0"
   ```

## 3. Ativação do Plugin no QGIS

1. Abra o QGIS.
2. No menu superior, vá em **Complementos** > **Gerenciar e Instalar Complementos...**.
3. No painel à esquerda, clique em **Instalados**.
4. Procure por **IDEFLOR Geo Downloader** na lista e marque a caixa de seleção ao lado do nome.
5. O ícone do plugin (logotipo do IDEFLOR ou ícone de download) aparecerá na sua barra de ferramentas.

## 4. Primeiro Uso e Dicas

*   **Área de Interesse**: Você pode definir a área de download usando a tela atual do seu mapa ou selecionando a extensão de uma camada (shapefile ou raster) que já esteja no seu projeto.
*   **Buffer**: Se a imagem parecer muito "justa" na borda, use as **Opções Avançadas** para aumentar o "Fator de Buffer".
*   **CBERS-4A**: Para usar o CBERS, é necessário criar uma conta gratuita no portal **DGI do INPE**:
    - **Cadastre-se aqui**: [INPE Explorer / Registro](http://www.dgi.inpe.br/catalogo/explore)
    - Configure o seu `INPE_EMAIL` e `INPE_PASSWORD` no arquivo `.env` para que o plugin consiga buscar e baixar as imagens.
*   **Destino**: Certifique-se de escolher uma pasta de saída onde você tenha permissão de escrita.

---
**Suporte Interno**: Samuel Santos (IDEFLOR)
