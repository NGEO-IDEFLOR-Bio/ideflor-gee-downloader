# Guia de Instalação: IDEFLOR Geo Downloader (QGIS)

Este guia descreve os passos necessários para instalar e ativar o plugin de download de imagens orbitais (Landsat e Sentinel) no seu QGIS.

## 1. Preparação da Pasta

O plugin é fornecido como uma pasta chamada `ideflor_gee_downloader`. Dentro desta pasta, as configurações de acesso (arquivo `.env` e chaves na pasta `secrets`) já devem estar configuradas para a conta do IDEFLOR.

### Passos:
1. Localize a pasta de plugins do seu perfil do QGIS no Windows:
   *   Pressione `Win + R` e cole o seguinte caminho:
       `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
2. Copie a pasta inteira `ideflor_gee_downloader` para dentro deste diretório.

## 2. Instalação de Dependências (Obrigatório)

O plugin utiliza bibliotecas do Google Earth Engine que não vêm por padrão no QGIS. Para instalá-las:

1. Feche o QGIS.
2. No menu Iniciar do Windows, procure por **OSGeo4W Shell** e execute-o **como Administrador**.
3. Na janela preta que se abrir, digite ou cole exatamente o comando abaixo e pressione `Enter`:
   
   ```bash
   python -m pip install earthengine-api requests python-dotenv
   ```
4. Aguarde a conclusão da instalação (pode levar alguns minutos). Quando terminar, você pode fechar a janela.

## 3. Ativação do Plugin no QGIS

1. Abra o QGIS.
2. No menu superior, vá em **Complementos** > **Gerenciar e Instalar Complementos...**.
3. No painel à esquerda, clique em **Instalados**.
4. Procure por **IDEFLOR Geo Downloader** na lista e marque a caixa de seleção ao lado do nome.
5. O ícone do plugin (logotipo do IDEFLOR ou ícone de download) aparecerá na sua barra de ferramentas.

## 4. Primeiro Uso e Dicas

*   **Área de Interesse**: Você pode definir a área de download usando a tela atual do seu mapa ou selecionando a extensão de uma camada (shapefile ou raster) que já esteja no seu projeto.
*   **Buffer**: Se a imagem parecer muito "justa" na borda, use as **Opções Avançadas** para aumentar o "Fator de Buffer" (ex: mudar de 2.0 para 3.0).
*   **Destino**: Certifique-se de escolher uma pasta de saída onde você tenha permissão de escrita.

---
**Suporte Interno**: Samuel Santos (IDEFLOR)
