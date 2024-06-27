from flask import Flask, request, jsonify, render_template
from datetime import datetime
import requests

app = Flask(__name__)

#@app.route('/', methods=['POST', 'GET'])
#def homepage():
#    return render_template('home.html')

@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('create_transaction.html')


if __name__ == "__main__":
    app.run(debug=True)