import sqlite3
import os
import pyodbc



diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect(f'{diretorio_atual}\\banco.db')
cursor = conn.cursor()


def bulk_insert(cursor, dados, batch_size=1000):
    for i in range(0, len(dados), batch_size):
        batch = dados[i:i + batch_size]
        cursor.executemany('''
        INSERT INTO lotes (rotina, lote, identificador,var_dict) VALUES (?, ?, ?, ?)
        ''', batch)


def select_ok():
    global cursor
    sql = f"""
    select identificador 
    from lotes
    where status_desc = 'OK' 
    """
    cursor.execute(sql)
    consulta =  cursor.fetchall()
    list_chamados = []
    for linha in consulta:
        list_chamados.append(int(linha[0]))

    return list_chamados


class X60:

    def __init__(self):
        self.connect()
        pass

    def connect(self):
        sql_HOST = 'CCTDCDADNT0060'                                                                #* NOME DO SERVIDOR           
        sql_NAME = 'gic'                                                                  #* NOME DO BANCO DE DADOS
        sql_USER = 'usr_pesquisa_sms'                                          #* USUÁRIO DE ACESSO
        sql_PASS = 'PesquisaSMS'                                            #* SENHA DE ACESSO

        ##### * A VARIAVEL ABAIXO É A QUE REALIZA A CONEXÃO COM O BANCO DE DADOS
        self.conex = pyodbc.connect('DRIVER={SQL Server};'
            'SERVER='       +str(sql_HOST)+';'
            'DATABASE='     +str(sql_NAME)+';'
            'UID='          +str(sql_USER)+';'
            'PWD='          +str(sql_PASS),
            autocommit=True)
        pass

    def disconnect(self):
        '''Fecha a conexão com o banco de dados SQL'''
        try: self.conex.close()
        except: pass                                                                           
        pass

    def execute(self,command,catch_return='on'):
        '''Realiza a conexão com o banco de dados SQL'''
        try:
            cursor = self.conex.cursor()                                                        #* CRIA O CURSOR  
            cursor.execute(command)                                                             #* EXECUTA O COMANDO RECEBIDO
        except:
            self.connect()
            cursor = self.conex.cursor()                                                        #* CRIA O CURSOR  
            cursor.execute(command)                                                             #* EXECUTA O COMANDO RECEBIDO

        if catch_return=='on': result = cursor.fetchall()                                       #* SE DESEJADO, PEGA O RESULTADO DO COMANDO
        else: result = None                                                                     #* CASO CONTRARIO RETORANARÁ APENAS 'None'
        return result      

    def select_chamados(self):
        '''Apaga os logs antigos do banco de dados'''
        sql = f"""  
        SELECT 
        --count ([co_chamado])
        --top(10)
        [co_chamado]
        FROM [gic].[dbo].[chamados] where [co_status_chamado] = 1 and [co_ambiente] = 44 and [co_ambiente_criacao] = 44 
        and ([dh_chamado] between '2027-01-01 00:00:00' and '2027-01-01 00:00:00'
        --or [dh_chamado] between '2024-01-01 00:00:00' and '2024-03-01 00:00:00' 
        --or [dh_chamado] between '2024-05-01 00:00:00' and '2024-06-01 00:00:00' 
        --or [dh_chamado] between '2024-06-01 00:00:00' and '2024-07-01 00:00:00' 
        --or [dh_chamado] between '2024-07-01 00:00:00' and '2024-08-01 00:00:00' 
        --or [dh_chamado] between '2024-08-01 00:00:00' and '2024-09-01 00:00:00' 
        --or [dh_chamado] between '2024-09-01 00:00:00' and '2024-10-01 00:00:00' 
        or [dh_chamado] between '2024-10-01 00:00:00' and '2024-11-01 00:00:00' 
        or [dh_chamado] between '2024-11-01 00:00:00' and '2024-11-15 00:00:00' 
        ) and [co_meio_acionamento] in (4)								      
        """
        consulta = self.execute(sql,catch_return='on')
        
        dados = []

        for linha in consulta:
            nu_chamado = linha[0]
            dados.append((1,1,nu_chamado,'{}'))

        return dados


    def select_chamados_ok(self,chamados_receb):
        '''Apaga os logs antigos do banco de dados'''
        sql = f"""  
        SELECT 
        [co_status_chamado]
        FROM [gic].[dbo].[chamados] 
        where [co_chamado] in ({chamados_receb})								      
        """
        consulta = self.execute(sql,catch_return='on')
        qt_total = len(consulta)
        qt_stt_1 = 0
        qt_stt_2 = 0
        qt_stt_x = 0
        for linha in consulta:
            if      linha[0] == 1   : qt_stt_1 += 1
            elif    linha[0] == 2   : qt_stt_2 += 1
            else                    : qt_stt_x += 1

        dados = {
             'qt_total':qt_total
            ,'qt_stt_1':qt_stt_1
            ,'qt_stt_2':qt_stt_2
            ,'qt_stt_x':qt_stt_x
        }

        return dados


x60 = X60()

def alimenta_banco():
    dados = x60.select_chamados()

    # Inserir dados em lotes
    bulk_insert(cursor, dados, batch_size=1000)

    # Confirmar as mudanças
    conn.commit()

    # Fechar a conexão
    conn.close()

def confere_trabalhados():
    chamados_ok = select_ok()
    print(len(chamados_ok))
    chamados_ok_str = str(chamados_ok).replace('[','').replace(']','')
    fonte = x60.select_chamados_ok(chamados_ok_str)
    print(fonte)
    pass



if __name__ == "__main__":
    # alimenta_banco()
    
    confere_trabalhados()

    pass


