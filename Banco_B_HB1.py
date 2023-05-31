from flask import Flask,request
import requests
import json
import time
import datetime
from threading import Thread
import random
import sys

horario = datetime.datetime.now()
ip = str(sys.argv[1])
porta = int(sys.argv[2])
ip_hb = str(sys.argv[3])
acoes = {}
acoes_bolsa = {}

app = Flask(__name__)
@app.route('/hora_errada')
def hora_errada():
    print("hora_errada em algum homebroker")
    print("Enviando o horario")
    return {"hora":horario.strftime('%H:%M:%S')}

@app.route("/acao", methods=["POST"])
def test():
    global acoes_bolsa
    print("entrou")
    acoes_bolsa = json.loads((request.data).decode())
    return ""

@app.route("/acao_especifica", methods=["POST"])
def test_2():
    global acoes_bolsa
    data = json.loads((request.data).decode())
    data_k = data.keys()
    for item in data_k:
        acoes_bolsa[item] = data[item]
    return ""

@app.route('/ajuste_hora/<valor>')
def ajuste_hora(valor):
    global horario
    hora_split = valor.split(":")
    horario = horario.replace(hour=int(hora_split[0]), minute=int(hora_split[1]), second=int(hora_split[2]))
    return "ajustou a hora do banco B"

def adicionar_bv(host,porta):
    texto = str(host)+","+str(porta)+","+horario.strftime("%H:%M:%S")
    requests.get(f"http://{ip_hb}/home/{texto}")

def hora_mais():
    global horario
    while True:
        print(horario.strftime('%H:%M:%S'))
        horario = horario + datetime.timedelta(seconds=1)
        time.sleep(1)

def loop_horario():
    global horario
    while True:
        time.sleep(10)
        if(random.randint(0, 1) == 1):
            if(random.randint(0, 1) == 1):
                horario = horario + datetime.timedelta(seconds=2)
            else:
                horario = horario - datetime.timedelta(seconds=2)

def compra_acao(host, porta):
    while True:
        time.sleep(5)
        if(len(acoes) == 0):
            indice = 1
        else: 
            indice = 0
        if(random.randint(indice, 1) == 1):
            chaves = list(acoes_bolsa.keys()) 
            chave_aleatória = random.choice(chaves)
            if int(acoes_bolsa[chave_aleatória]['quantidade']) == 0:
                print("estoque de acoes zerado para essa")
            else:
                var = requests.get(f"http://{ip_hb}/compra_acao/{host}+{porta}+{horario.strftime('%H:%M:%S')}+{chave_aleatória}")
                if var.text == "fix":
                    print("Erro na compra de acao")
                elif(var.text.find("Estoque") != -1):
                    print("O estoque de acoes que voce tentou comprar estava esgotado")
                else:
                    try:
                        acoes[var.text] = acoes[var.text] + 1
                    except:    
                        acoes[var.text] = 1
                    print(f"Voce comprou uma acao da {var.text}")
        else:
            chaves = list(acoes.keys()) 
            chave_aleatória = random.choice(chaves)
            if(acoes[chave_aleatória] == 0 ):
                print("Voce nao possui acoes dessas para vender.")
                del acoes[chave_aleatória] 
            else:
                var = requests.get(f"http://{ip_hb}/venda_acao/{host}+{porta}+{horario.strftime('%H:%M:%S')}+{chave_aleatória}")
                if var.text == "-1":
                    print(f"vendeu uma acao {chave_aleatória}")   
                    acoes[chave_aleatória] = acoes[chave_aleatória] - 1
                else:
                    print("Erro na venda de acao")

if __name__ == "__main__":
    adicionar_bv(ip,porta)
    thread = Thread(target=loop_horario) 
    thread2 = Thread(target=compra_acao, args=(ip,porta,)) 
    thread3 = Thread(target=hora_mais) 
    thread.start() 
    thread2.start() 
    thread3.start() 
    app.run(host=ip, port=porta)