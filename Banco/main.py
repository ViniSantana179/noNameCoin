from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Cliente(db.Model):
    id: int
    nome: str
    senha: int
    qtdMoeda: float

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Float, unique=False, nullable=False)

@dataclass
class Seletor(db.Model):
    id: int
    nome: str
    ip: str
    qtdMoeda: float
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Float, unique=False, nullable=False)

@dataclass
class Validador(db.Model):
    id: int
    nome: str
    ip: str
    qtdMoeda: float
    flag_alerta: int
    transaction_key: str
    banido: bool
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Float, unique=False, nullable=False)
    flag_alerta = db.Column(db.Integer, unique=False, nullable=False)
    transaction_key = db.Column(db.String(20), unique=True, nullable=False)
    banido = db.Column(db.Boolean, unique=False, nullable=False)

@dataclass
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: float
    horario : datetime
    status: int
    
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Float, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/cliente', methods = ['GET'])
def ListarCliente():
    if(request.method == 'GET'):
        clientes = Cliente.query.all()
        return jsonify(clientes)  

@app.route('/cliente', methods = ['POST'])
def InserirCliente():
    if request.method == 'POST':
        nome = request.form['name']
        senha = request.form['senha']
        qtdMoeda = request.form['quant_moedas']
        if nome and senha and qtdMoeda:
            objeto = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoeda)
            db.session.add(objeto)
            db.session.commit()
            return jsonify(objeto)
        else:
            return jsonify({'message': 'Dados incompletos'}), 400
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>', methods = ['GET'])
def UmCliente(id):
    if(request.method == 'GET'):
        objeto = Cliente.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>/<int:qtdMoedas>', methods=["POST"])
def EditarCliente(id, qtdMoedas):
    if request.method=='POST':
        try:
            cliente = Cliente.query.filter_by(id=id).first()
            cliente.qtdMoedas = qtdMoedas
            db.session.commit()
            return jsonify(['Alteração feita com sucesso'])
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)

    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>', methods = ['DELETE'])
def ApagarCliente(id):
    if(request.method == 'DELETE'):
        objeto = Cliente.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Cliente Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor', methods = ['GET'])
def ListarSeletor():
    if(request.method == 'GET'):
        produtos = Seletor.query.all()
        return jsonify(produtos)  

@app.route('/seletor/<string:nome>/<string:ip>', methods = ['POST'])
def InserirSeletor(nome, ip):
    if request.method=='POST' and nome != '' and ip != '':
        objeto = Seletor(nome=nome, ip=ip, qtdMoeda=0)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>', methods = ['GET'])
def UmSeletor(id):
    if(request.method == 'GET'):
        produto = Seletor.query.get(id)
        return jsonify(produto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>/<float:moedas>', methods=["POST"])
def EditarSeletor(id, moedas):
    if request.method=='POST':
        try:
            seletor = Seletor.query.filter_by(id=id).first()
            db.session.commit()
            seletor.qtdMoeda += moedas
            db.session.commit()
            return jsonify(seletor)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>', methods = ['DELETE'])
def ApagarSeletor(id):
    if(request.method == 'DELETE'):
        objeto = Seletor.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Seletor Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/hora', methods = ['GET'])
def horario():
    if(request.method == 'GET'):
        objeto = int(datetime.now().timestamp())
        return jsonify(objeto)
		
@app.route('/transacoes', methods = ['GET'])
def ListarTransacoes():
    if(request.method == 'GET'):
        transacoes = Transacao.query.all()
        return jsonify(transacoes)

@app.route('/transacoes', methods = ['POST'])
def CriaTransacao():
    if request.method == 'POST':
        remetente = request.form.get('remetente')
        recebedor = request.form.get('recebedor')
        valor = request.form.get('valor')

        if remetente and recebedor and valor:
            if remetente == recebedor:
                return jsonify({'message': 'Remetente e recebedor devem ser clientes diferentes'}), 400
            
            remetente = int(remetente)
            recebedor = int(recebedor)
            valor = float(valor)
            
            # Verificar se o recebedor existe no banco de dados
            remetente_existe = Cliente.query.get(remetente)
            recebedor_existe = Cliente.query.get(recebedor)

            if remetente_existe and recebedor_existe:
                valor_com_taxa = valor + (valor * 0.015)    # Calcular o valor com a taxa de 1.5%

                if remetente_existe.qtdMoeda >= valor_com_taxa:
                     # Verificar transações no último minuto
                    now = datetime.now()
                    one_minute_ago = now - timedelta(minutes=1) #calcular diferenças entre datas.
                    # Contar o número de transações no último minuto
                    transacoes_ultimo_minuto = Transacao.query.filter(
                        Transacao.remetente == remetente,
                        Transacao.horario >= one_minute_ago,
                        Transacao.horario < now
                    ).count()

                    print(f'TESTE1234 {transacoes_ultimo_minuto}')

                    # Verificar transações no próximo minuto
                    next_minute_start = now + timedelta(seconds=1) # manipular datas e horas
                    next_minute_end = now + timedelta(minutes=1)
                    # Contar o número de transações no próximo minuto
                    transacoes_proximo_minuto = Transacao.query.filter(
                        Transacao.remetente == remetente,
                        Transacao.horario >= next_minute_start,
                        Transacao.horario < next_minute_end
                    ).count()

                    print(f'TESTE12 {transacoes_ultimo_minuto}')

                    #Valida as 100 transações no último minuto e qualquer transação no próximo minuto.
                    if transacoes_ultimo_minuto >= 100 or transacoes_proximo_minuto > 0:
                        return jsonify({'message': 'Remetente excedeu o limite de transações. Tente novamente mais tarde.'}), 400
                    
                    remetente_existe.qtdMoeda -= valor_com_taxa
                    recebedor_existe.qtdMoeda += valor

                    objeto = Transacao(remetente=int(remetente), recebedor=int(recebedor), valor=float(valor), status=0, horario=datetime.now())
                    db.session.add(objeto)
                    db.session.commit()

                    return jsonify(objeto)
                else:
                    return jsonify({'message': 'Saldo Insuficiente'}), 400
            else:
                return jsonify({'message': 'ID do recebedor não encontrado no banco de dados'}), 400
        else:
            return jsonify({'message': 'Dados incompletos'}), 400
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405

@app.route('/transacoes/<int:id>', methods = ['GET'])
def UmaTransacao(id):
    if(request.method == 'GET'):
        objeto = Transacao.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transacoes/<int:id>/<int:status>', methods=["POST"])
def EditaTransacao(id, status):
    if request.method=='POST':
        try:
            objeto = Transacao.query.filter_by(id=id).first()
            db.session.commit()
            objeto.id = id
            objeto.status = status
            db.session.commit()
            return jsonify(objeto)
        except Exception as e:
            data={
                "message": "transação não atualizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


# Ajusta para trazer as transacoes pelo id do remetente		
@app.route('/transacoes/remetente/<int:remetente>', methods=['POST'])
def listar_transacoes(remetente):
    if request.method == 'POST':
        # Filtrando transações pelo remetente
        transacoes =  transacoes = db.session.query(Transacao).filter_by(remetente=remetente).all()
        if (len(transacoes) > 1):
            return jsonify(transacoes[-2])
        else:
            return jsonify([])
    else:
        return jsonify(['Method Not Allowed']), 405

@app.route('/validador', methods = ['GET'])
def ListarValidador():
    if(request.method == 'GET'):
        validadores = Validador.query.all()
        return jsonify(validadores)  

@app.route('/validador/<string:nome>/<string:ip>/<int:moeda>/<int:alertas>/<string:transaction_key>', methods = ['POST'])
def InserirValidador(nome, ip, moeda, alertas, transaction_key):
    if request.method=='POST' and nome != '' and ip != '':
        validador = Validador(nome=nome, ip=ip, qtdMoeda=moeda, flag_alerta=alertas, transaction_key=transaction_key, banido=False)
        db.session.add(validador)
        db.session.commit()
        return jsonify(validador)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>', methods = ['GET'])
def UmValidador(id):
    if(request.method == 'GET'):
        validador = Validador.query.get(id)
        return jsonify(validador)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>/<float:moedas>', methods=["POST"])
def EditarValidador(id, moedas):
    if request.method=='POST':
        try:
            validador = Validador.query.filter_by(id=id).first()
            db.session.commit()
            validador.qtdMoeda += moedas
            db.session.commit()
            return jsonify(validador)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])
    
@app.route('/validador/alerta/<int:id>', methods=["POST"])
def PunirValidador(id):
    if request.method=='POST':
        try:
            validador = Validador.query.filter_by(id=id).first()
            db.session.commit()
            validador.flag_alerta += 1
            db.session.commit()
            return jsonify(validador)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>', methods = ['DELETE'])
def ApagarValidador(id):
    if(request.method == 'DELETE'):
        validador = Validador.query.filter_by(id=id).first()
        db.session.commit()
        validador.banido = True
        db.session.commit()

        data={
            "message": "Validador Banido com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/criar_transacao')
def criar_transacao():
    return render_template('create_transaction.html')

@app.route('/criar_cliente')
def criar_cliente():
    return render_template('create_cliente.html')

if __name__ == "__main__":
	with app.app_context():
		db.create_all()
    
app.run(host='0.0.0.0', debug=True)