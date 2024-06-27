from flask import Flask, request, jsonify
import datetime
import requests

app = Flask(__name__)


# URL do endpoint
url = 'http://127.0.0.1:3000/validador/create'

payload = {'nome': 'teste 1', 'ip': '127.0.0.1:5002', 'moedas': 55}

# Enviando a requisição GET
response = requests.post(url, json=payload)

# Verificando o status da resposta
if response.status_code == 200:
    print('Sucesso!', response.json())
else:
    print('Erro ao fazer a requisição', response.status_code)


accounts = {
    "user1": {"balance": 1000, "last_transaction_time": None, "transaction_count": 0},
    "user2": {"balance": 500, "last_transaction_time": None, "transaction_count": 0},
}

transactions = [
    {
        "id": 1,
        "sender": "user1",
        "receiver": "user2",
        "amount": 1,
        "fee": 1,
        "timestamp": "2024-06-01T12:00:00",
        "status": 0,
        "unique_key": None
    }
]

@app.route('/validador', methods=['POST'])
def validador():
    print("Transacao")
    data = request.json
    print(data)
    transaction_id = data['id']

    # Encontrar a transação
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)
    if not transaction:
        return jsonify({"status": 2, "message": "Transação não encontrada"}), 400

    sender = transaction['sender']
    amount = transaction['amount']
    fee = transaction['fee']
    timestamp = datetime.datetime.fromisoformat(transaction['timestamp'])
    current_time = datetime.datetime.now()

    # Verificar saldo suficiente
    if accounts[sender]['balance'] < amount + fee:
        print("400 aqui")
        return jsonify({"status": 2, "message": "Saldo insuficiente"}), 400

    # # Verificar se o horário da transação é válido
    # if timestamp > current_time or (accounts[sender]['last_transaction_time'] and timestamp <= accounts[sender]['last_transaction_time']):
    #     return jsonify({"status": 2, "message": "Horário da transação inválido"}), 400

    # Verificar o limite de transações por minuto
    # if accounts[sender]['last_transaction_time'] and (current_time - accounts[sender]['last_transaction_time']).seconds < 60:
    #     accounts[sender]['transaction_count'] += 1
    #     if accounts[sender]['transaction_count'] > 100:
    #         return jsonify({"status": 2, "message": "Limite de transações por minuto excedido"}), 400
    # else:
    #     accounts[sender]['transaction_count'] = 1

    accounts[sender]['balance'] -= amount + fee
    accounts[sender]['last_transaction_time'] = current_time

    accounts[transaction['receiver']]['balance'] += amount

    return jsonify({"status": 1, "message": "Transação validada com sucesso"}), 200



def get_data():
    return

if __name__ == '__main__':
    app.run(debug=True, port=5002)