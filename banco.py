
##### * ARQUIVO RESPONSÁVEL PELAS CONEXÕES E AÇÕES DIRÉTAS NOS BANCOS DE DADOS
##### * 
##### * ESTE ARQUIVO CHAMA O ARQUIVO:
##### *     -config.py
##### * 
##### * ESTE ARQUIVO É CHAMADO PELO ARQUIVO:
##### *     -main.py
##### * 


from config import Config   # * PARA AS INFORMAÇÕES DAS CONEXÕES, E NOME DO ROBÔ
import pyodbc               # * PARA CRIAR A CONEXÃO COM O BANCO DE DADOS
import os                   # * PARA OBTER O USUÁRIO LOCAL DO COMPUTADOR


##### * ABAIXO SEGUE A CRIAÇÃO DE CADA CONEXÃO ESPECÍFICA PARA O BANCO DE DADOS RESPECTIVO
##### * AS CONEXÕES NÃO UTILIZADAS PELO ROBÔ FICARÃO COMENTADAS E NÃO EXCLUÍDAS
##### * PARA FACILITAR O REAPROVEITAMENTO DESTE MÓDULO PARA DEMAIS ROBÔS

connRobo = pyodbc.connect('DRIVER={SQL Server};'
'SERVER='       +str(Config.DBROB_HOST.value)+';'
'DATABASE='     +str(Config.DBROB_NAME.value)+';'
'UID='          +str(Config.DBROB_USER.value)+';'
'PWD='          +str(Config.DBROB_PASS.value),
autocommit=True)

connMain = pyodbc.connect('DRIVER={SQL Server};'
'SERVER='       +str(Config.DBMain_HOST.value)+';'
'DATABASE='     +str(Config.DBMain_NAME.value)+';'
'UID='          +str(Config.DBMain_USER.value)+';'
'PWD='          +str(Config.DBMain_PASS.value),
autocommit=True)

conn496 = pyodbc.connect("DRIVER={SQL Server};"
'SERVER='       +str(Config.DB496_HOST.value)+";"
'DATABASE='     +str(Config.DB496_NAME.value)+";"
'UID='          +str(Config.DB496_USER.value)+";"
'PWD='          +str(Config.DB496_PASS.value),
autocommit=True)


class Robo():
    '''Classe para trabalhar com o controle de fluxo dos robôs no banco de dados'''
   
    class Execucao():
        '''Trabalha com o relatorio de controle de execução dos robos'''
      
        def verifica():
            '''Verifica execução do robô salva no banco de dados
                Retorna: informação do banco de dados
            '''
            retorno = False
            try:
                cur = connRobo.cursor()
                sql = f"""
                SELECT TOP(1) 
                DH_STATUS 
                FROM robotb001_atividade 
                WHERE IC_APLICACAO='{Config.ROBOT_NAME.value}' 
                order by DH_STATUS desc
                """
                cur.execute(sql)
                res = cur.fetchone()
                retorno = res
            except pyodbc.Error as e:
                lastError = format(e)
                retorno = lastError
            return retorno
                
        def grava():
            '''Grava a datahora de execução do robô salva no banco de dados'''
            retorno = False
            usuario = os.getlogin()
            try:
                cur = connRobo.cursor()
                sql = f"""  
                INSERT INTO [dbo].[atividade]
                ([DH_LOGIN]
                ,[CO_USUARIO]
                ,[IC_APLICACAO]
                ,[DH_STATUS])
                VALUES
                (GETDATE(),
                '{usuario}',
                '{Config.ROBOT_NAME.value}',
                GETDATE())                
                """
                cur.execute(sql)
                retorno = True
            except pyodbc.Error as e:
                lastError = format(e)
                retorno = lastError
            return retorno
        
        def atualiza():
            '''Atualiza a datahora de execução do robô salva no banco de dados'''
            retorno = False
            usuario = os.getlogin()
            try:
                cur = connRobo.cursor()
                sql = f"""
                UPDATE [dbo].[atividade]
                SET [DH_STATUS] = GETDATE()
                WHERE IC_APLICACAO = '{Config.ROBOT_NAME.value}'
                AND CO_USUARIO = '{usuario}'                
                """
                cur.execute(sql)
                retorno = True
            except pyodbc.Error as e:
                lastError = format(e)
                retorno = lastError
            return retorno
        
        def apaga():
            '''Apaga a execução do robô salva no banco de dados referente ao usuário que utilizou'''
            retorno = False
            usuario = os.getlogin()
            try:
                cur = connRobo.cursor()
                sql = f"""
                DELETE FROM [dbo].[atividade]
                WHERE IC_APLICACAO = '{Config.ROBOT_NAME.value}'
                AND CO_USUARIO = '{usuario}'                              
                """
                cur.execute(sql)
                retorno = True
            except pyodbc.Error as e:
                lastError = format(e)
                retorno = lastError
            return retorno
        
    class Log():
        '''Classe que trabalha com os logs gerados pelo robo'''
      
        def grava(msg_log,vida,nome_robo):
            '''Verifica execução do robô salva no banco de dados'''
            retorno = False
            usuario = os.getlogin()
            try:
                cur = connRobo.cursor()
                sql = f"""  
                INSERT INTO [dbo].[logs]
                ([DH_INSERT]
                ,[NOME_ROBO]
                ,[USUARIO]
                ,[LOG]
                ,[VIDA])
                VALUES
                (GETDATE(),
                '{nome_robo}',
                '{usuario}',
                '{msg_log}',
                '{vida}')                
                """
                cur.execute(sql)
                retorno = True
            except pyodbc.Error as e:
                lastError = format(e)
                retorno = lastError
            return retorno
   
        def apaga(self):
            '''Apaga os logs antigos do banco de dados'''
            retorno = False
            try:
                cur = connRobo.cursor()
                sql = f"""  
                DELETE
                FROM [dbo].[logs] 
                WHERE	VIDA = 'DIA'		AND DH_INSERT < DATEADD(DAY,	-1 ,GETDATE())
                OR		VIDA = 'SEMANA'		AND DH_INSERT < DATEADD(WEEK,	-1 ,GETDATE())
                OR		VIDA = 'MES'		AND DH_INSERT < DATEADD(MONTH,	-1 ,GETDATE())
                OR		VIDA = 'ANO'		AND DH_INSERT < DATEADD(YEAR,	-1 ,GETDATE())    
                """
                cur.execute(sql)
                retorno = True
            except pyodbc.Error as e:
                lastError = format(e)
                retorno = lastError
            return retorno   

class Main():
    ''' Classe que trabalha com o(s) banco(s) utilizados pelo Main'''
    
    def seleciona_matriculas_reset():
        ''' Selecionas as matriculas cadastrada para terem suas senhas resetadas'''
        cur = connMain.cursor()
        sql = f"""
        SELECT
        [CO_MAT_RESET],
        [CO_MAT_SOLICITANTE]
        FROM [Main].[REQUISICAO]
        WHERE 
        IC_STATUS = 0
        order by 1 desc
        """
        cur.execute(sql)
        resp = cur.fetchall()
        return resp
        
    def seleciona_contrato_matricula(matricula):
        ''' Seleciona o contrato que a matricula pertence'''
        cur = conn496.cursor()
        sql = f"""
        SELECT IdContrato 
        FROM [bd_controle_pessoal].dbo.[empregados] 
        WHERE LOGIN ='{matricula}'
        """
        cur.execute(sql)
        resp = cur.fetchone()
        resp = resp[0]
        return resp
        
    def seleciona_gestor(contrato):
        ''' Seleciona o próximo gestor ativo do contrato específicado
            Retorna : a matricula do gestor e sua senha criptografia
        '''
        cur = connMain.cursor()
        sql = f"""
        SELECT TOP (1)
        [CO_MATRICULA],
        [DE_SENHA]
        FROM [Main].[GESTOR]
        WHERE CO_CONTRATO = {contrato}
        AND
        IC_SENHA_INVALIDA = 0
        ORDER BY DT_ALTERACAO ASC
        """
        cur.execute(sql)
        resp = cur.fetchone()
        return resp    
    
    def atualiza_status_reset(matricula,status):
        ''' Atualiza no banco o status (resultado) da matrícula resetada
            Parâmetros:
                * matricula : Matrícula resetada
                * status    : Resultado
                    * 1 - Sucesso
                    * 2 - Falha
        '''
        cur = connMain.cursor()
        sql = f"""
        UPDATE [Main].[REQUISICAO] 
        SET [IC_STATUS] = {status}, 
        DT_RESET = GETDATE() 
        WHERE [CO_MAT_RESET]='{matricula}' 
        AND [IC_STATUS] = 0
        """
        cur.execute(sql)
        
    def atualiza_status_gestor(matricula):
        ''' Define a senha do gestor como inválida no banco de dados'''
        cur = connMain.cursor()
        sql = f"""
        UPDATE [Main].[GESTOR]
        SET [IC_SENHA_INVALIDA] = 1
        WHERE CO_MATRICULA = '{matricula}'
        """
        cur.execute(sql)        
        
    def envia_email_solicitante(matricula_solicitante, matricula_reset, status):
        ''' Executa a procedure que envia e-mail com o ressultado do reset realizado
            Parâmetros:
                * matricula_solicitante : quem solicitou o reset
                * matricula_reset : a matricula que foi resetada
                * status : 
                    * 1 - Sucesso
                    * 2 - Falha
        ''' 
        cur = connMain.cursor()
        sql = f"""
        EXEC ssat.ResetSenha_email_V2 @TIPO = {status}, @mat_oper = '{matricula_reset}', @mat_so = '{matricula_solicitante}', @senha_pad = '123'
        """
        cur.execute(sql)
        
    def envia_email_gestor_invalido(matricula_gestor):
        ''' Executa a procedure que envia o e-mail para o gestor informando que a sua senha está inválida '''
        cur = connMain.cursor()
        sql = f"""
        EXEC ssat.ResetSenha_email_V2 @TIPO = 6, @mat_GESTOR = '{matricula_gestor}', @senha_pad = 'Error'
        """
        cur.execute(sql)        
        
        
        
        
        
        
    
