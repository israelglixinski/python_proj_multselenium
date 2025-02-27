from datetime import datetime
from time import sleep
import centro_acoes
import requests
import ast
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
passos = None



def obter_passos():
    global passos
    url = configs_finais['endpoint_api']
    rotina = configs_finais['rotina']
    solicitacao = {"rotina":rotina}
    passos = requests.get(f'{url}passos',json=solicitacao).json()['resposta']
    return passos

def obter_horarios():
    url = configs_finais['endpoint_api']
    horarios_exec = configs_finais['horarios_exec']
    solicitacao = {"horarios_exec":horarios_exec}
    horarios = requests.get(f'{url}horarios',json=solicitacao).json()['resposta']
    return horarios

def obter_lote():
    
    url             = configs_finais['endpoint_api']
    rotina          = configs_finais['rotina']
    lote            = configs_finais['lote']
    max_qt_lote     = configs_finais['max_qt_lote']
    usr_host        = configs_finais['usr_host']
    solicitacao     = {"rotina":rotina,"lote":lote,"max_qt_lote":max_qt_lote,"usr_host":usr_host}
    lote            = requests.get(f'{url}lotes',json=solicitacao).json()['resposta']
    return lote

def update_status(regs_lote,status):
    url             = configs_finais['endpoint_api']
    usr_host        = configs_finais['usr_host']
    solicitacao     = {"regs_lote":regs_lote,"usr_host":usr_host,"status":status}
    up_status       = requests.get(f'{url}update_status',json=solicitacao).json()['resposta']
    return up_status

def executa_passo(passo_atual, identificador=0, varia_dicts_reg={},feed_stats='----'):
    global passos
    print(f'{feed_stats}-{identificador}-{passo_atual['ordem']}-{passo_atual['acao']}-{passo_atual['descricao']}')
    retorno = centro_acoes.acionador(passo_atual, identificador, varia_dicts_reg)
    if retorno['SITUACAO'] == 'SUB_PASSOS': 
        nu_prox_passo = retorno['NU_PROX_PASSO'] 
        prox_passo = passos['acoes'][str(nu_prox_passo)]
        retorno = executa_passo(prox_passo, identificador, varia_dicts_reg,feed_stats)
    else:
        return retorno

def orquestrador():
    global passos
    passos = obter_passos()
    horarios = obter_horarios()
    dias_da_semana = ['SEG','TER','QUA','QUI','SEX','SAB','DOM']
    
    try:
        for numero_passo in passos['ordem_acoes']["INICIAL"]:
            passo = passos['acoes'][str(numero_passo)]
            executa_passo(passo)
    except: pass

    while True:
        
        passos = obter_passos()

        try:
            for numero_passo in passos['ordem_acoes']["PRE_HORA"]:
                passo = passos['acoes'][str(numero_passo)]
                executa_passo(passo)
        except: pass    
        
        indice_dia = datetime.now().weekday()
        dia_da_semana =  dias_da_semana[indice_dia]
        horarios_hoje = horarios[dia_da_semana]
        hora_agora = datetime.now().strftime('%H:%M')
        
        if (
            ((horarios_hoje["horario_ini" ] != "NAO") and (horarios_hoje["horario_fin" ] != "NAO") and (hora_agora > horarios_hoje["horario_ini" ]) and (hora_agora < horarios_hoje["horario_fin" ])) and not
            ((horarios_hoje["excluir1_ini"] != "NAO") and (horarios_hoje["excluir1_fin"] != "NAO") and (hora_agora > horarios_hoje["excluir1_ini"]) and (hora_agora < horarios_hoje["excluir1_fin"])) and not
            ((horarios_hoje["excluir2_ini"] != "NAO") and (horarios_hoje["excluir1_fin"] != "NAO") and (hora_agora > horarios_hoje["excluir2_ini"]) and (hora_agora < horarios_hoje["excluir1_fin"])) and not
            ((horarios_hoje["excluir3_ini"] != "NAO") and (horarios_hoje["excluir1_fin"] != "NAO") and (hora_agora > horarios_hoje["excluir3_ini"]) and (hora_agora < horarios_hoje["excluir1_fin"]))
            ):

            print('dentro do horario de execução')
            print('buscando lote')
            lote = obter_lote()
            qt_lote = len(lote)
            if qt_lote == 0:
                print("não temos mais lotes para trabalhar")
                dormir = 1
            else:
    
                try:
                    for numero_passo in passos['ordem_acoes']["PRE_LOOP"]:
                        passo = passos['acoes'][str(numero_passo)]
                        executa_passo(passo)
                except: pass            
    
                list_update_lote_ok     = []
                list_update_lote_falha  = []
                cont_lote = 0
                rotina      = configs_finais['rotina']
                num_lote    = configs_finais['lote']
                for registro in lote:
                    cont_lote += 1
                    str_atual = f"""r{rotina}l{num_lote}-{qt_lote}/{cont_lote}"""
                    
                    try:    
                        id_reg        = registro['id_reg'       ]
                        identificador = registro['identificador']
                        var_dict      = registro['var_dict'     ]                    
                        print(f'Iniciando o registro: {registro['id_reg']}')
                        
                        try:
                            varia_dicts_reg = ast.literal_eval(var_dict)
                        except:
                            varia_dicts_reg = None
    
    
                        try:
                            for numero_passo in passos['ordem_acoes']["IN_LOOP"]:
                                passo = passos['acoes'][str(numero_passo)]
                                executa_passo(passo, identificador, varia_dicts_reg,str_atual)
                        except: pass

                        
                        list_update_lote_ok   .append(int(id_reg))
                        print(f'Finalizado o registro: {registro['id_reg']}')
                    except:
                        list_update_lote_falha.append(int(id_reg))
                        print(f'Falha no registro registro: {registro['id_reg']}')
                
                try:
                    for numero_passo in passos['ordem_acoes']["POS_LOOP"]:
                        passo = passos['acoes'][str(numero_passo)]
                        executa_passo(passo)
                except: pass
                
                
                update_status(list_update_lote_ok   ,'OK'   )
                update_status(list_update_lote_falha,'FALHA')
                print('finalizado lote')
                dormir = 0


        else:
            print('fora do horario de execução')
            dormir = 1

        try:
            for numero_passo in passos['ordem_acoes']["POS_HORA"]:
                passo = passos['acoes'][str(numero_passo)]
                executa_passo(passo)
        except: pass

        if dormir: sleep(configs_finais["sleep_time"])
        pass
    pass

def iniciar():
    global configs_finais
    configs_finais = centro_acoes.func_OBTER_CONFIGS(None,None,None)
    orquestrador()



if __name__ == "__main__":
    iniciar()