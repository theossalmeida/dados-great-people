import os
import boto3

"""
Importante que no ambiente que o script for rodar é necessário configurar o aws corretamente com as credenciais
"""


def upload_file_to_s3(file_path, bucket, **kwargs):
    """
    Função para salvar os arquivos no S3 bucket
    params:
        file_path: Path do arquivo a ser salvo
        bucket: Bucket que o arquivo será salvo
        s3_name: Nome do arquivo na S3
    """

    # Cria cliente S3
    s3 = boto3.client('s3')

    if kwargs.get('s3_name'):
        s3_name = kwargs.get('s3_name')
    else:
        s3_name = file_path.split('\\')[-1]

    # Faz upload do arquivo
    s3.upload_file(file_path, bucket, s3_name)


def download_file_from_s3(bucket, s3_name, local_path):
    """
    Função para salvar os arquivos no S3 bucket
    params:
        bucket: Bucket que o arquivo será coletado
        s3_name: Nome do arquivo na S3
        local_path: Local onde o arquivo baixado será salvo
    """

    # Cria cliente S3
    s3 = boto3.client('s3')

    # Faz download do arquivo para o caminho final desejado
    s3.download_file(bucket, s3_name, local_path)


def download_all_files_from_s3_folder(bucket, folder_prefix, local_dir):
    """
    Função para salvar os arquivos no S3 bucket
    params:
        bucket: Bucket que os arquivos serão coletados
        folder_prefix: Prefixo da pasta no S3 bucket
        local_dir: Pasta local que os arquivos serão tratados
    """

    s3 = boto3.client('s3')

    response = s3.list_objects_v2(Bucket=bucket, Prefix=folder_prefix)

    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'] == 'a_tratar/':
                continue
            key = obj['Key']
            file_name = os.path.basename(key)
            local_path = os.path.join(local_dir, file_name)
            download_file_from_s3(bucket, key, local_path)


def delete_file_from_s3(bucket, s3_name):
    """
    Função para salvar os arquivos no S3 bucket
    params:
        bucket: Bucket que o arquivo será deletado
        s3_name: Nome do arquivo na S3
    """

    # Cria cliente S3
    s3 = boto3.client('s3')

    # Deleta o arquivo
    s3.delete_object(Bucket=bucket, Key=s3_name)


