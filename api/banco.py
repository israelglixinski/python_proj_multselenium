import sqlite3
import os
from datetime import datetime

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
conexao = None

def conectar():
    global conexao
    conexao = sqlite3.connect(f'{diretorio_atual}\\banco.db')

def desconectar():
    global conexao
    if conexao != None:
        conexao = None

def executar(comando, retorno='off'):
    global conexao
    cursor = conexao.cursor()
    cursor.execute(comando)
    if retorno == 'commit': 
        conexao.commit()
        resposta = 'ok'
    elif retorno == 'select': 
        resposta = cursor.fetchall()
    else:
        resposta = 'off'
    cursor.close()
    return resposta

def select_configs_main():
    sql=f"""
    SELECT rotina, lote, max_qt_lote, delay, horarios_exec, sleep_time, api_porta, webdrivers
    FROM configs_main
    WHERE ativo = 1
    ORDER BY id_reg ASC
    LIMIT 1
    """
    consulta = executar(sql,'select')[0]

    return {
     'rotina'        : consulta[0]                  
    ,'lote'          : consulta[1]                  
    ,'max_qt_lote'   : consulta[2]                      
    ,'delay'         : consulta[3]                  
    ,'horarios_exec' : consulta[4]                          
    ,'sleep_time'    : consulta[5]                      
    ,'api_porta'     : consulta[6]                      
    ,'webdrivers'    : consulta[7]                      
    }

def select_configs_usrhost(usrhost):
    sql=f"""
    SELECT rotina, lote, max_qt_lote, delay, horarios_exec, sleep_time, usr_host
    FROM configs_usrhost
    WHERE ativo = 1
    AND usr_host = '{usrhost}'
    ORDER BY id_reg ASC
    LIMIT 1
    """
    try:
        consulta = executar(sql,'select')[0]
        return {
        'rotina'        : consulta[0]                  
        ,'lote'          : consulta[1]                  
        ,'max_qt_lote'   : consulta[2]                      
        ,'delay'         : consulta[3]                  
        ,'horarios_exec' : consulta[4]                          
        ,'sleep_time'    : consulta[5]                      
        ,'usr_host'      : consulta[6]                      
        }
    except:
        return {}

def select_passos(rotina):
    sql=f"""
    SELECT estagio, ordem, acao, var_dict, sub_passos, descricao
    FROM passos
    WHERE rotina = {rotina}
    AND ativo = 1
    ORDER BY ordem ASC
    """
    try:
        consulta = executar(sql,'select')
        if len(consulta) == 0:
            return {"ordem_acoes":[], "acoes":{}}

        else:
            acoes = {}
            ordem_acoes         = []
            ordem_INICIAL       = []
            ordem_PRE_HORA      = []
            ordem_PRE_LOOP      = []
            ordem_IN_LOOP       = []
            ordem_POS_LOOP      = []
            ordem_POS_HORA      = []
            ordem_SUB_PASSO     = []
            for linha in consulta:
                ordem = linha[1]
                ordem_acoes     .append(ordem)
                if linha[0] == "INICIAL"    : ordem_INICIAL   .append(ordem)             
                if linha[0] == "PRE_HORA"   : ordem_PRE_HORA  .append(ordem)             
                if linha[0] == "PRE_LOOP"   : ordem_PRE_LOOP  .append(ordem)             
                if linha[0] == "IN_LOOP"    : ordem_IN_LOOP   .append(ordem)             
                if linha[0] == "POS_LOOP"   : ordem_POS_LOOP  .append(ordem)             
                if linha[0] == "POS_HORA"   : ordem_POS_HORA  .append(ordem)             
                if linha[0] == "SUB_PASSO"  : ordem_SUB_PASSO .append(ordem)             
                acoes[ordem] = {
                      "estagio"     : linha[0]
                    , "ordem"       : linha[1]
                    , "acao"        : linha[2]
                    , "var_dict"    : linha[3]
                    , "sub_passos"  : linha[4]
                    , "descricao"   : linha[5]
                    }
                #estagio, ordem, acao, var_dict, sub_passos
            ordem_acoes     .sort()
            ordem_INICIAL   .sort()
            ordem_PRE_HORA  .sort()
            ordem_PRE_LOOP  .sort()
            ordem_IN_LOOP   .sort()
            ordem_POS_LOOP  .sort()
            ordem_POS_HORA  .sort()
            ordem_SUB_PASSO .sort()
            resposta = {
                "acoes":acoes
                ,"ordem_acoes":{
                     "TODAS"     : ordem_acoes     
                    ,"INICIAL"   : ordem_INICIAL   
                    ,"PRE_HORA"  : ordem_PRE_HORA  
                    ,"PRE_LOOP"  : ordem_PRE_LOOP  
                    ,"IN_LOOP"   : ordem_IN_LOOP   
                    ,"POS_LOOP"  : ordem_POS_LOOP  
                    ,"POS_HORA"  : ordem_POS_HORA  
                    ,"SUB_PASSO" : ordem_SUB_PASSO 
                    }
                }
            return resposta
    except:
        return {"ordem_acoes":[], "acoes":{}}

def select_horarios(horario):
    dias_semana = ["SEG", "TER", "QUA", "QUI", "SEG", "SAB", "DOM"]
    negativa_dia_padrao = {
          "horario_ini"     : 'NAO'
        , "horario_fin"     : 'NAO'
        , "excluir1_ini"    : 'NAO'
        , "excluir1_fin"    : 'NAO'
        , "excluir2_ini"    : 'NAO'
        , "excluir2_fin"    : 'NAO'
        , "excluir3_ini"    : 'NAO'
        , "excluir3_fin"    : 'NAO'
    }

    negativa_semana_padrao = {}
    for dia in dias_semana:
        negativa_semana_padrao[dia] = negativa_dia_padrao

    sql=f"""
    SELECT dia_semana, horario_ini, horario_fin, excluir1_ini, excluir1_fin, excluir2_ini, excluir2_fin, excluir3_ini, excluir3_fin
    FROM horarios_exec
    WHERE id_config = {horario}
    ORDER BY id_reg ASC
    """

    try:
        consulta = executar(sql,'select')
        if len(consulta) == 0:
            return negativa_semana_padrao

        else:
            horarios = {}
            for linha in consulta:
                dia_semana = linha[0]
                horarios[dia_semana] = {
                      "horario_ini"  : linha[1]
                    , "horario_fin"  : linha[2]
                    , "excluir1_ini" : linha[3]
                    , "excluir1_fin" : linha[4]
                    , "excluir2_ini" : linha[5]
                    , "excluir2_fin" : linha[6]
                    , "excluir3_ini" : linha[7]
                    , "excluir3_fin" : linha[8]
                    }
            return horarios
    except:
        return negativa_semana_padrao

def select_lote(rotina,lote,max_qt_lote,usr_host):
    sql=f"""
    SELECT id_reg, identificador, var_dict
    FROM lotes
    WHERE lote = {lote}
    AND rotina = {rotina}
    AND status_desc IS NULL
    LIMIT {max_qt_lote}
    """
    try:
        consulta = executar(sql,'select')
        if len(consulta) == 0:
            return []
        else:
            registros = []
            para_update = []
            for linha in consulta:
                para_update.append(linha[0])
                registros.append(
                    {
                      "id_reg"          : linha[0]
                    , "identificador"   : linha[1]
                    , "var_dict"        : linha[2]
                    }
                    )
            
            para_update_tratado = str(para_update).replace('[','').replace(']','')
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql_update = f"""
            UPDATE lotes
            SET 
              status_desc       ='RESERVADO'
            , status_usrhost    ='{usr_host}'
            , status_dtm        ='{agora}'
            WHERE id_reg in ({para_update_tratado})
            """
            executar(sql_update,'commit')            
            return registros
    except:
        return []


def update_lote(regs_lote,usr_host,status):
    try:
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        para_update_tratado = str(regs_lote).replace('[','').replace(']','')
        sql_update = f"""
        UPDATE lotes
        SET 
          status_desc       ='{status}'
        , status_usrhost    ='{usr_host}'
        , status_dtm        ='{agora}'
        WHERE id_reg in ({para_update_tratado})
        """
        executar(sql_update,'commit')            
        return "OK"
    except:
        return "FALHA"



if __name__ == "__main__":
    
    conectar()
    print(select_configs_main())
    pass