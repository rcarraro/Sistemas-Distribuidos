from flask import Flask, request
import datetime
import random
import requests
import json
from threading import Thread
import time
import sys


ip = str(sys.argv[1])
porta = int(sys.argv[2])
ip_bv = str(sys.argv[3])
ip_banco = ""
app = Flask(__name__)

def enviar_acoes(banco, acao):
    item = f"http://{banco}/acao_especifica"
    requests.post(item, json=acao)

def enviar_acoes_fixo(banco, acoes):
    item = f"http://{banco}/acao"
    requests.post(item, json=acoes)

@app.route('/compra_acao/<valores>')
def compra_acao(valores):
    url = f"http://{ip_bv}/compra_acao/{valores}"
    return requests.get(url).text

@app.route('/venda_acao/<valores>')
def venda_acao(valores):
    url = f"http://{ip_bv}/venda_acao/{valores}"
    return requests.get(url).text

@app.route('/home/<valores>')
def inicio(valores):
    global ip_banco
    valores = valores.split(',')
    ip_banco = valores[0]+":"+valores[1] 
    valores[0] = ip
    valores[1] = porta
    requests.get(f"http://{ip_bv}/home/{valores[0]},{valores[1]},{valores[2]}")
    return ""
        
@app.route('/hora_errada')
def hora_errada():
    return requests.get(f"http://{ip_banco}/hora_errada").text

@app.route('/ajuste_hora/<valor>')
def ajuste_hora(valor):
    global horario
    requests.get(f"http://{ip_banco}/ajuste_hora/{valor}")
    return ""

@app.route('/acao',methods = ['POST'])
def ajuste_acao():
    # enviar_acoes_fixo(f"{valores[0]}:{valores[1]}")
    thread2 = Thread(target=enviar_acoes_fixo, args=(ip_banco,json.loads(request.data.decode()),))
    thread2.start()
    # item = f"http://{ip_banco}/acao"
    # requests.post(item, json=json.loads(request.data.decode()))
    return ""

@app.route('/acao_especifica', methods=["POST"])
def ajuste_acoes():
    thread2 = Thread(target=enviar_acoes, args=(ip_banco,json.loads(request.data.decode()),))
    thread2.start()
    return ""

if __name__ == "__main__":
    app.run(host=ip, port=porta, debug=True)       