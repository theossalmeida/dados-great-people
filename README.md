# Processamento de Dados

Este repositório contém scripts para monitoramento, tratamento e upload de arquivos de dados armazenados no AWS S3. O sistema foi desenvolvido para automatizar o processamento de planilhas Excel, calcular médias e integrar os dados tratados a um backend.

## Funcionalidades

- **Monitoramento:** Verifica periodicamente a existência de novos arquivos na pasta configurada do bucket S3.
- **Download:** Realiza o download dos arquivos para processamento local.
- **Processamento:** 
  - Lê planilhas Excel.
  - Calcula a média entre as colunas `nota_1` e `nota_2` e adiciona o resultado na coluna `nota_pesquisa`.
- **Upload:** Envia os arquivos originais e os arquivos tratados de volta ao S3, organizando-os em pastas específicas (ex.: `recebidos/` e `tratados/`).
- **Integração com API:** Monta e envia um JSON com os dados processados para um backend via requisição HTTP.
- **Logging:** Registra todas as etapas e erros para facilitar a identificação e solução de problemas.

## Pré-requisitos

- **Python 3.x**
- **AWS CLI e Credenciais AWS:** As credenciais devem estar configuradas corretamente no ambiente para acesso ao AWS S3.
- **Bibliotecas Python:**  
  - boto3  
  - pandas  
  - requests

## Instalação

1. **Clone o repositório:**
git clone https://github.com/theossalmeida/dados-great-people


2. **Instale as dependências:**
pip install boto3 pandas requests


## Configuração

Antes de executar, ajuste os parâmetros no arquivo `rotina_tratamento.py` conforme seu ambiente:

- **bucket_files:** Nome do bucket S3 onde os arquivos serão manipulados.
- **root_path:** Caminho local onde os dados serão processados.
- **Pastas configuradas:**
- `pasta_tratar`: Pasta no S3 contendo os arquivos a serem processados.
- `pasta_tratados`: Pasta onde os arquivos processados serão salvos.
- `pasta_recebidos`: Pasta para armazenar os arquivos originais recebidos.
- `pasta_tratamento`: Pasta local utilizada para armazenar os arquivos baixados.

## Estrutura do Repositório

- **funcoes_s3.py:**  
Contém funções para operações com o AWS S3:
- `upload_file_to_s3`: Realiza o upload de arquivos.
- `download_file_from_s3`: Faz o download de um arquivo específico.
- `download_all_files_from_s3_folder`: Baixa todos os arquivos de uma pasta.
- `delete_file_from_s3`: Exclui um arquivo do S3.

- **rotina_tratamento.py:**  
Script principal que:
- Monitora o bucket S3 para detectar arquivos a serem processados.
- Processa os dados das planilhas Excel (cálculo da média entre `nota_1` e `nota_2`).
- Realiza o upload dos arquivos originais e tratados para o S3.
- Envia os dados processados para um backend via requisições HTTP.
- Registra logs detalhados de todas as etapas do processo.

## Como Executar

1. **Configure as credenciais da AWS:**  
Certifique-se de que o ambiente possui as credenciais AWS configuradas corretamente.

2. **Execute o script principal:**
python rotina_tratamento.py

O script entrará em um loop contínuo, verificando o bucket a cada 60 segundos para processar novos arquivos.

## Logging

- Os logs são salvos no diretório `logs` (definido pelo parâmetro `root_path`), com o nome contendo o timestamp da execução.
- Consulte os logs para monitorar o andamento do processamento e identificar eventuais problemas.
