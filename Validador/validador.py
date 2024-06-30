from flask import Flask, request, jsonify
from datetime import datetime
import time
import requests

app = Flask(__name__)


# # URL do endpoint
# url = 'http://127.0.0.1:3000/validador/create'

# payload = {'nome': 'teste 1', 'ip': '127.0.0.1:5002', 'moedas': 55}

# # Enviando a requisição GET
# # Criando meu validador
# response_validator = requests.post(url, json=payload)

# # Verificando o status da resposta
# if response_validator.status_code == 200:
#     print('Sucesso!', response_validator.json())
# else:
#     print('Erro ao fazer a requisição', response_validator.status_code)


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
    response_last_transaction = requests.post(f'http://127.0.0.1:5000/transacoes/remetente/{remetente_id}')
    if(response_last_transaction.status_code == 200):
        object_last_transaction = response_last_transaction.json()
        last_transaction_time = timestamp_transform(object_last_transaction['horario'])


    # ====================== REGRAS ======================
    # Verificar saldo suficiente do cliente
    if remetente['qtdMoeda'] < valor:
        return jsonify({"status": 2, "message": "Saldo insuficiente"}), 400


    # Verificar se o horário da transação é válido
    if trasaction_time > server_time and (trasaction_time > last_transaction_time if last_transaction_time != '' else True):
        return jsonify({"status": 2, "message": "Horário da transação inválido"}), 400

    # Verificar o limite de transações por minuto
    # if accounts[remetente]['last_transaction_time'] and (current_time - accounts[remetente]['last_transaction_time']).seconds < 60:
    #     accounts[remetente]['transaction_count'] += 1
    #     if accounts[remetente]['transaction_count'] > 100:
    #         return jsonify({"status": 2, "message": "Limite de transações por minuto excedido"}), 400
    # else:
    #     accounts[remetente]['transaction_count'] = 1

    # accounts[remetente]['balance'] -= valor + fee
    # accounts[remetente]['last_transaction_time'] = current_time

    # accounts[transaction['receiver']]['balance'] += valor

    return jsonify({"status": 1, "message": "Transação validada com sucesso", "key": transaction_key}), 200


def timestamp_transform(data):
    # Tratando horarios da transacao, transformando em timestamp 
    date_obj = datetime.strptime(data, '%a, %d %b %Y %H:%M:%S GMT')
    trasaction_time = int( time.mktime(date_obj.timetuple()))
    return trasaction_time

def get_data():
    return

if __name__ == '__main__':
    app.run(debug=True, port=5002)