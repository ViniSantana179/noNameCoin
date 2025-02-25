from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import time
import requests
import sys


app = Flask(__name__)


# Verifica se o número correto de argumentos foi passado
if len(sys.argv) != 5:
    print("Uso: python script.py <porta>")
    sys.exit(1)

# Pega o segundo argumento da linha de comando
nome = sys.argv[1]
porta = sys.argv[2]
moedas = sys.argv[3]
impostor = sys.argv[4]

res1 = 1
res2 = 2

if (impostor.lower()[0] == "s"):
    print("LOG :: Logando um validador (impostor)")
    res1 = 2
    res2 = 1

# # URL do endpoint
url = 'http://127.0.0.1:3000/validador/create'

payload = {'nome': nome, 'ip': f'127.0.0.1:{porta}', 'moedas': moedas}

# Enviando a requisição GET
# Criando meu validador
response_validator = requests.post(url, json=payload)

# Verificando o status da resposta
if response_validator.status_code == 200:
    print('Sucesso!', response_validator.json())
else:
    print('Erro ao fazer a requisição', response_validator.status_code)


@app.route('/validador', methods=['POST'])
def validador():
    transaction_data = request.json['transaction']
    transaction_key = request.json['transaction_key']
    
    # Dados da Transacao
    remetente_id = transaction_data['remetente']
    valor = transaction_data['valor']
    trasaction_time = timestamp_transform(transaction_data['horario'])

    # Pegando o horario do servidor 
    response_time = requests.get('http://127.0.0.1:5000/hora')
    if (response_time.status_code == 200):
        server_time = int(response_time.text)

    # Pegando os dados do remetente
    response_remetente = requests.get(f'http://127.0.0.1:5000/cliente/{remetente_id}')
    if (response_remetente.status_code == 200):
        remetente = response_remetente.json()

    # Pegando as ultimas transacoes do remetente
    last_transaction_time = ''
    response_last_transaction = requests.post(f'http://127.0.0.1:5000/transacoes/remetente/{remetente_id}')
    if(response_last_transaction.status_code == 200 and len(response_last_transaction.json()) > 0):
        object_last_transaction = response_last_transaction.json()
        last_transaction_time = timestamp_transform(object_last_transaction['horario'])

    # ====================== REGRAS ======================
    # Verificar saldo suficiente do cliente
    if remetente['qtdMoeda'] < valor or remetente['qtdMoeda'] < (valor + (valor * 0.015)):
        return jsonify({"status": res2, "message": "Saldo insuficiente"}), 400


    # Verificar se o horário da transação é válido
    if trasaction_time > server_time and (trasaction_time > last_transaction_time if last_transaction_time != '' else True):
        return jsonify({"status": res2, "message": "Horário da transação inválido"}), 400

    return jsonify({"status": res1, "message": "Transação validada com sucesso", "key": transaction_key}), 200


def timestamp_transform(data):
    # Tratando horarios da transacao, transformando em timestamp 
    date_obj = datetime.strptime(data, '%a, %d %b %Y %H:%M:%S GMT')
    trasaction_time = int( time.mktime(date_obj.timetuple()))
    print(trasaction_time)
    return trasaction_time


def get_data():
    return

if __name__ == '__main__':
    app.run(debug=False, port=porta)