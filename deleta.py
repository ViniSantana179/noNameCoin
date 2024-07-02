import os

# Defina o caminho do arquivo que você deseja deletar
file_path = r'./Banco/instance/site.db'

# Verifique se o arquivo existe
if os.path.exists(file_path):
    try:
        # Delete o arquivo
        os.remove(file_path)
        print(f'O arquivo {file_path} foi deletado com sucesso.')
    except Exception as e:
        print(f'Ocorreu um erro ao tentar deletar o arquivo: {e}')
else:
    print(f'O arquivo {file_path} não foi encontrado.')