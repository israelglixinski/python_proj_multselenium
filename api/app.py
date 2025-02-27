
from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve  
import base64
import os

try: import banco
except: from api import banco



banco.conectar()
app = Flask(__name__)
CORS(app, resources={r"*":{"origins":"*"}})
diretorio_atual = os.path.dirname(os.path.abspath(__file__))



@app.route("/")
def home():
    return "IGPYDESCELEIUM"

@app.route("/configs", methods=['GET'])
def configs():
    recebido = request.get_json()
    configs_locais      = dict(recebido["configs_locais"])
    usr_host            = recebido["usrhost"]
    banco.conectar()
    configs_main        = banco.select_configs_main()
    configs_usrhost     = banco.select_configs_usrhost(usr_host)  
    configs_adicionais  = {'usr_host':usr_host}
    configs_finais      = {**configs_usrhost}
    configs_finais.update({k:v for k,v in configs_main          .items() if k not in configs_finais})
    configs_finais.update({k:v for k,v in configs_locais        .items() if k not in configs_finais})
    configs_finais.update({k:v for k,v in configs_adicionais    .items() if k not in configs_finais})
    resposta = {'resposta':configs_finais}
    return jsonify(resposta)

@app.route("/passos", methods=['GET'])
def passos():
    recebido    = request.get_json()
    rotina      = recebido["rotina"]
    banco.conectar()
    passos_banco = banco.select_passos(rotina)
    resposta = {'resposta':passos_banco}
    return jsonify(resposta)

@app.route("/horarios", methods=['GET'])
def horarios():
    recebido    = request.get_json()
    horario      = recebido["horarios_exec"]
    banco.conectar()
    horarios = banco.select_horarios(horario)
    resposta = {'resposta':horarios}
    return jsonify(resposta)

@app.route("/lotes", methods=['GET'])
def lotes():
    recebido    = request.get_json()
    rotina      = recebido["rotina"         ]
    lote        = recebido["lote"           ]
    max_qt_lote = recebido["max_qt_lote"    ]
    usr_host    = recebido["usr_host"       ]
    banco.conectar()
    novo_lote = banco.select_lote(rotina,lote,max_qt_lote,usr_host)
    resposta = {'resposta':novo_lote}
    return jsonify(resposta)

@app.route("/update_status", methods=['GET'])
def update_status():
    recebido    = request.get_json()
    regs_lote   = recebido["regs_lote"  ]
    usr_host    = recebido["usr_host"   ]
    status      = recebido["status"     ]
    banco.conectar()
    up_lote  = banco.update_lote(regs_lote,usr_host,status)
    resposta = {'resposta':up_lote}
    return jsonify(resposta)

@app.route("/verifica_drivers", methods=['GET'])
def verifica_drivers():
    global diretorio_atual
    recebido        = request.get_json()
    drivers_locais  = recebido["drivers_locais"]
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_webdrivers = f"{diretorio_atual}\\webdrivers"
    subpastas_com_webdriver = []
    for root, dirs, files in os.walk(diretorio_webdrivers):
        if "msedgedriver.exe" in files:
            subpastas_com_webdriver.append(str(root).split('\\')[-1])
    novos_drivers = []
    for subpasta in subpastas_com_webdriver:
        if subpasta not in drivers_locais:
            arquivo = open(f"{diretorio_webdrivers}\\{subpasta}\\msedgedriver.exe", 'rb')
            dados_binarios = arquivo.read()
            arquivo.close()
            dados_base64 = base64.b64encode(dados_binarios).decode('utf-8')
            novos_drivers.append({
                 "versao":subpasta
                ,"base64":dados_base64
                })
    resposta = {'resposta':novos_drivers}
    return jsonify(resposta)

def iniciar():
    porta = int(banco.select_configs_main()['api_porta'])
    serve(app, host="0.0.0.0", port=porta)

if __name__ == "__main__":
    iniciar()