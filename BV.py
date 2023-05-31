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
lista = {}
horario_bolsa = datetime.datetime.now()
acoes = {
    "teste1" : {
        "valor": 14,
        "quantidade": 70
    },
    "teste2" : {
        "valor": 12,
        "quantidade": 65
    },
    "teste3" : {
        "valor": 10,
        "quantidade": 85
    },
    "teste5" : {
        "valor": 25,
        "quantidade": 75
    }
}

def enviar_acoes(tempo, acao):
    global lista
    
    for item in lista:
        item = f"http://{item}/acao_especifica"
        x = {
        f"{acao}": acoes[acao]
        }
        requests.post(item, json=x)


def enviar_acoes_fixo(hb):
    global lista, acoes
    item = f"http://{hb}/acao"
    requests.post(item, json=acoes)

app = Flask(__name__)

@app.route('/compra_acao/<valores>')
def compra_acao(valores):
    global lista, acoes,horario_bolsa
    #verificar horarios
    soma = 0
    valores = valores.split("+")
    hora_split = (valores[2].split(":"))
    hora_bolsa_ajuste = datetime.datetime.now()
    diferenca = (horario_bolsa - hora_bolsa_ajuste)
    horario_banco = hora_bolsa_ajuste.replace(hour=int(hora_split[0]), minute=int(hora_split[1]), second=int(hora_split[2]))
    diferenca = (horario_bolsa - horario_banco ).seconds
    if(diferenca>80000):
        diferenca = 86400-(horario_bolsa - horario_banco ).seconds
    else:
        diferenca = (horario_bolsa - horario_banco ).seconds
    # if(lista[f"{valores[0]}:{valores[1]}"] - diferenca >= 1 or diferenca-lista[f"{valores[0]}:{valores[1]}"] >= 1):
    if(diferenca > 1):
        arquivo = open("logs_horario.txt", "a")
        texto_log = f"solicitado ajuste de horario pelo {valores[0]}:{valores[1]} diferenca:{diferenca}\n"
        arquivo.write(texto_log)
        arquivo.close()
        for item in lista:
            var = (requests.get(f"http://{item}/hora_errada")).text
            var = json.loads(var)
            hora_split = (var['hora'].split(":"))
            hora_bolsa_ajuste = datetime.datetime.now()
            horario_banco = hora_bolsa_ajuste.replace(hour=int(hora_split[0]), minute=int(hora_split[1]), second=int(hora_split[2]))
            diferenca = (horario_bolsa - horario_banco ).seconds
            if(diferenca>80000):
                diferenca = 86400-(horario_bolsa - horario_banco ).seconds
            else:
                diferenca = (horario_bolsa - horario_banco ).seconds
            soma += diferenca

        for item in lista:
            lista[item] = soma/(len(lista)+1)
            requests.get(f"http://{item}/ajuste_hora/{(horario_bolsa + datetime.timedelta(seconds=soma/(len(lista)+1))).strftime('%H:%M:%S')}")
            horario_bolsa = horario_bolsa + datetime.timedelta(seconds=soma/(len(lista)+1))
        return "fix"
    
    else:
        acao = valores[3]
        if(acoes[acao]['quantidade'] == 0):
            return f"Estoque de acoes {acao} finalizado, aguarde alguma venda"
        else:
            arquivo = open("logs_compra.txt", "a")
            arquivo2 = open("valores_acao.txt", "a")
            texto = f"Foi Comprada uma acao de {acao} pelo valor de {acoes[acao]['valor']}"
            texto_log = f"{valores[0]}:{valores[1]} (diferenca:{diferenca}) Foi Comprada uma acao de {acao} pelo valor de {acoes[acao]['valor']} (Horario_Bolsa:{horario_bolsa};Horario_Banco:{horario_banco})\n"
            texto_log2 = f"{acao} {acoes[acao]['valor']} {horario_bolsa}\n"
            arquivo.write(texto_log)
            arquivo2.write(texto_log2)
            arquivo.close()
            arquivo2.close()
            print(texto)
            acoes[acao]['valor'] = acoes[acao]['valor']*1.05
            acoes[acao]['quantidade'] = acoes[acao]['quantidade']-1
            thread20 = Thread(target=enviar_acoes, args=(0, acao,))
            thread20.start()
            return f"{acao}"

@app.route('/venda_acao/<valores>')
def venda_acao(valores):
    global lista, acoes,horario_bolsa
    #verificar horarios
    soma = 0
    valores = valores.split("+")
    hora_split = (valores[2].split(":"))
    hora_bolsa_ajuste = datetime.datetime.now()
    diferenca = (horario_bolsa - hora_bolsa_ajuste)
    horario_banco = hora_bolsa_ajuste.replace(hour=int(hora_split[0]), minute=int(hora_split[1]), second=int(hora_split[2]))
    diferenca = (horario_bolsa - horario_banco ).seconds
    if(diferenca>80000):
        diferenca = 86400-(horario_bolsa - horario_banco ).seconds
    else:
        diferenca = (horario_bolsa - horario_banco ).seconds
    if(diferenca > 1):
        arquivo = open("logs_horario.txt", "a")
        texto_log = f"solicitado ajuste de horario pelo {valores[0]}:{valores[1]} diferenca:{diferenca}\n"
        arquivo.write(texto_log)
        arquivo.close()
        for item in lista:
            var = (requests.get(f"http://{item}/hora_errada")).text
            var = json.loads(var)
            hora_split = (var['hora'].split(":"))
            hora_bolsa_ajuste = datetime.datetime.now()
            horario_banco = hora_bolsa_ajuste.replace(hour=int(hora_split[0]), minute=int(hora_split[1]), second=int(hora_split[2]))
            diferenca = (horario_bolsa - horario_banco ).seconds
            if(diferenca>80000):
                diferenca = 86400-(horario_bolsa - horario_banco ).seconds
            else:
                diferenca = (horario_bolsa - horario_banco ).seconds
            soma += diferenca

        for item in lista:
            lista[item] = soma/(len(lista)+1)
            requests.get(f"http://{item}/ajuste_hora/{(horario_bolsa + datetime.timedelta(seconds=soma/(len(lista)+1))).strftime('%H:%M:%S')}")
            horario_bolsa = horario_bolsa + datetime.timedelta(seconds=soma/(len(lista)+1))
        return "fix"

    else:
        acao = valores[3]
        arquivo = open("logs_compra.txt", "a")
        arquivo2 = open("valores_acao.txt", "a")
        texto = f"Foi vendida uma acao de {acao} pelo valor de {acoes[acao]['valor']}"
        texto_log = f"{valores[0]}:{valores[1]} (diferenca:{diferenca}) Foi Vendida uma acao de {acao} pelo valor de {acoes[acao]['valor']} (Horario_Bolsa:{horario_bolsa};Horario_Banco:{horario_banco})\n"
        texto_log2 = f"{acao} {acoes[acao]['valor']} {horario_bolsa}\n"
        arquivo.write(texto_log)
        arquivo.close()
        print(texto)
        acoes[acao]['valor'] = acoes[acao]['valor']*.95
        acoes[acao]['quantidade'] = acoes[acao]['quantidade']+1
        arquivo2.write(texto_log2)
        arquivo2.close()
        thread20 = Thread(target=enviar_acoes, args=(0, acao,))
        thread20.start()
        return "-1"

@app.route('/home/<valores>')
def inicio(valores):
    global lista,horario_bolsa
    soma = 0
    valores = valores.split(",")
    hora_split = (valores[2].split(":"))
    hora_bolsa_ajuste = datetime.datetime.now() 
    horario_banco = hora_bolsa_ajuste.replace(hour=int(hora_split[0]), minute=int(hora_split[1]), second=int(hora_split[2]))
    lista[f"{valores[0]}:{valores[1]}"] = (horario_bolsa - horario_banco ).seconds
    if(lista[f"{valores[0]}:{valores[1]}"]>80000):
        lista[f"{valores[0]}:{valores[1]}"] = 86400-(horario_bolsa - horario_banco ).seconds
    else:
        lista[f"{valores[0]}:{valores[1]}"] = (horario_bolsa - horario_banco ).seconds
    for item in lista:
        soma += lista[item]
    for item in lista:
        lista[item] = int(soma/(len(lista)+1))
    enviar_acoes_fixo(f"{valores[0]}:{valores[1]}")
    # thread2 = Thread(target=enviar_acoes_fixo, args=(,))
    # thread2.start()
    return ("HB adicionado a lista")

def hora_mais():
    global horario_bolsa
    while True:
        time.sleep(1)
        horario_bolsa = horario_bolsa + datetime.timedelta(seconds=1)


        
if __name__ == "__main__":
    arquivo = open("valores_acao.txt", "w")
    arquivo.close()
    thread3 = Thread(target=hora_mais)
    thread3.start()
    # thread = Thread(target=enviar_acoes, args=(4,))
    app.run(host=ip, port=porta, debug=True)       