import pandas as pd
import logging
import time
import requests
from datetime import datetime
from funcoes_s3 import *
import json

"""
Script de monitoramento do Bucket no S3 para tratar arquivos salvos pelos usuários

Código desenvolvido por: theoalmeida00@gmail.com
"""

# Função de monitoramento do bucket para verificar se algum usuário salvou arquivos a serem tratados
def monitorar_bucket():

    while True:
        # Etapa de coleta dos arquivos:
        logging.info('Baixando todos arquivos a serem tratados')
        try:
            download_all_files_from_s3_folder(bucket=bucket_files, folder_prefix=pasta_tratar, local_dir=pasta_tratamento)
            logging.info('Coleta dos arquivos finalizada')
        except Exception as e:
            logging.error('Erro na coleta dos arquivos: ' + str(e))

        arquivos_a_tratar = os.listdir(pasta_tratamento)

        if len(arquivos_a_tratar) == 0:
            logging.info("Sem arquivos para tratamento")

        else:

            # Etapa de tratamento dos arquivos:
            logging.info('Inicio do tratamento dos arquivos')
            for i, arquivo in enumerate(arquivos_a_tratar):
                logging.info(f'Tratamento do arquivo {i+1}/{len(arquivos_a_tratar)}')
                try:
                    path_arquivo = os.path.join(root_path, 'a ser tratado', arquivo)
                    df = pd.read_excel(path_arquivo)
                    df['nota_pesquisa'] = df.apply(lambda row: round(((row['nota_1'] + row['nota_2']) / 2), 2), axis=1)
                    final_path = os.path.join(root_path, pasta_tratados, arquivo)
                    df.to_excel(final_path, index=False)
                except Exception as e:
                    logging.error(f'Erro durante tratamento do arquivo {arquivo} ' + str(e))
            
                # Etapa de upload do arquivo recebido na pasta correta:
                try:
                    logging.info(f'Salvando {arquivo} recebido na pasta de recebidos')
                    arquivo_recebido = os.path.join(root_path, 'a ser tratado', arquivo)
                    upload_file_to_s3(arquivo_recebido, bucket_files, s3_name='recebidos/' + arquivo)
                except Exception as e:
                    logging.error(f'Erro durante upload do arquivo {arquivo} recebido ' + str(e))

                # Etapa de upload do arquivo tratado na pasta correta:
                try:
                    logging.info(f'Salvando {arquivo} tratado na pasta de tratados')
                    arquivo_tratado = os.path.join(root_path, 'tratados', arquivo)
                    arq_nome = arquivo.split('.')[0]
                    arq_extensao = arquivo.split('.')[1]
                    upload_file_to_s3(arquivo_tratado, bucket_files, s3_name='tratados/' + arq_nome + '_tratado.' + arq_extensao)
                except Exception as e:
                    logging.error(f'Erro durante upload do arquivo {arquivo} tratado ' + str(e))

                # Etapa de upload do arquivo na pasta de 'a tratar':
                try:
                    logging.info(f'Deletando {arquivo} da pasta de a_tratar')
                    delete_file_from_s3(bucket_files, s3_name='a_tratar/' + arquivo)
                except Exception as e:
                    logging.error(f'Erro durante exclusão do arquivo {arquivo} no S3 ' + str(e))

                # Excluindo arquivo local pós tratamento
                try:
                    logging.info(f'Deletando {arquivo} da pasta local')
                    os.remove(arquivo_recebido)
                    os.remove(arquivo_tratado)
                except Exception as e:
                    logging.error(f'Erro durante exclusão do arquivo {arquivo} na pasta local ' + str(e))

                # Montando JSON para salvar no banco de dados
                logging.info('Montando JSON para salvar no banco de dados')
                try:
                    payload_list = []
                    for i, row in df.iterrows():
                        payload_dict = {}
                        payload_dict['nome_pesquisa'] = row['codigo_pesquisa']
                        payload_dict['created_date'] = datetime.now().strftime('%Y-%m-%d')
                        payload_dict['nota_1'] = row['nota_1']
                        payload_dict['nota_2'] = row['nota_2']
                        payload_dict['media_pesquisa'] = row['nota_pesquisa']
                        payload_list.append(payload_dict)
                except Exception as e:
                    logging.error('Erro durante preparo do json para envio a API: ' + str(e))

                logging.info('Enviando requisição para o backend')
                try:
                    response = requests.post('http://localhost:8080/pesquisas/multiples', json=payload_list)
                except Exception as e:
                    logging.error('Erro durante envio da requisição: ' + str(e))
                    logging.info(str(payload_list))
                logging.info(str(payload_list))
                if response.status_code not in (200, 201):
                    logging.error(f'Erro durante envio da requisição ({response.status_code}): {response.json}')




        time.sleep(60)


if __name__ == '__main__':

    timestamp_execucao = datetime.now().strftime('%d_%m_%Y__%H_%M_%S')

    # Declaração de variaveis:
    #TODO: Alterar valores para produção
    bucket_files = 'great-people-teste'
    root_path = r'C:\Users\TSantoro\Desktop\great-people-teste\processamento dados'
    pasta_tratar = 'a_tratar/'
    pasta_tratados = 'tratados/'
    pasta_recebidos = 'recebidos/' 
    pasta_tratamento = os.path.join(root_path, 'a ser tratado')

    logging.basicConfig(
            filename=os.path.join(root_path, 'logs', 'logs_execucao_' + timestamp_execucao),
            level=logging.INFO
            )

    logging.info('Iniciando processo do tratamento de dados: ' + timestamp_execucao)

    monitorar_bucket()

