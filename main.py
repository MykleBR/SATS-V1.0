
##### * ARQUIVO PRINCIPAL, PARA EXECUÇÃO E COMPILAÇÃO.
##### * ESTE ARQUIVO CHAMA TODOS OS OUTROS ARQUIVOS, MAS NÃO É CHAMADO POR NENHUM DELES.
##### * NESTE ARQUIVO QUE FICA A CONSTRUÇÃO DA ROTINA E APLICAÇÃO DO ROBÔ.

from pkg_resources import resource_filename                                                     # * COLOCAR ARQUIVOS DENTRO DO BINÁRIO DA COMPILAÇÃO
from datetime import datetime, timedelta                                                        # * UTILIZAÇÃO E CONTROLE DE DATA E HORA
from Crypto.Cipher import AES                                                                   # * CRIPTOGRAFIA
from threading import Thread                                                                    # * CONTROLE DE CAMADAS DE EXECUÇÃO
from config import Config                                                                       # * ONDE FICA AS CONFIGURAÇÕES BÁSICAS
from queue import Queue                                                                         # * TRANSPORTE DE MENSAGENS ATRAVÉS DA MEMÓRIA
from time import sleep                                                                          # * CONTROLE DE TEMPO DE EXECUÇÃO
from glob import glob                                                                           # * OBTER ACESSO A VÁRIOS ARQUIVOS
import binascii                                                                                 # * CONTROLE DE ENCODE PARA A CRIPTOGRAFIA
import tkinter                                                                                  # * CRIADOR FRONT-END
import base64                                                                                   # * CONTROLE DE BASE PARA A CRIPTOGRAFIA
import banco                                                                                    # * MÓDULO DE FUNÇÕES PARA O BANCO DE DADOS
import sats                                                                                     # * MÓDULO DE FUNÇÕES PARA ACESSO AO X
import json                                                                                     # * CONVERSÃO EM JSON
import os                                                                                       # * MANIPULADOR DIRETO DO SISTEMA OPERACIONAL



class automacao:
    ''' * Classe principal responsável pela a aplicação do robô'''
    
    def __init__(self):
        ''' * Inicializador'''
        self.conta_linha    = 1                                                                 # * PARA EXIBIÇÃO DAS MENSAGENS NO FRONT-END
        self.caixa_de_msg   = Queue()                                                           # * TRANSPORTE DAS MENSAGENS PELA MEMÓRIA
        self.janela         = tkinter.Tk()                                                      # * CRIAÇÃO DA JANELA NO FRONT-END
        self.define_configuracoes()                                                             # * VERIFICA SE FOI PASSADA ALGUMA CONFIGURAÇÃO PELO USUÁRIO
        Thread(target = self.controle_de_acoes).start()                                         # * EXECUTA A ROTINA PRINCIPAL DENTRO DE UMA CAMADA DE THREAD
        self.front = self.criar_monitor()                                                       # * EXECUTA A JANELA PRINCIPAL, A CHAMANDO DENTRO DE UM LOOP PERPÉTUO
    
    
    def define_configuracoes(self):
        modo_firefox = 'oculto'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
        try:                                                                                    # * TENTA LOCALIZAR ARQUIVO DE CONFIGURAÇÃO
            arquivo = open ('configs','r')                                                      
            leitura = (str(arquivo.read()).replace(' ','')).split('\n')                         # * RETINA OS ESPAÇOS EM BRANCO
            for linha in leitura:                                                               # * VERIFICA LINHA À LINHA SE EXISTE ALGUMA CONFIGURAÇÃO
                linha = linha.split('=')                                    
                try:
                    chave = linha[0]                                        
                    valor = linha[1]
                except:
                    chave = 'erro'
                    valor = 'erro'
                ##### * ABAIXO FICA AS DEFINIÇÕES
                ##### * DAS OPÇÕES DE CONFIGURAÇÕES DESEJADAS   
                if chave == 'visual' and valor == 'on':                                         # * VERIFICA CONFIGURAÇÃO DO VISUAL DO FIREFOX
                    modo_firefox = 'visivel'
            arquivo.close()
        except:
            pass
        ##### * MOMENTO ONDE SÃO APLICADAS AS CONFIGURAÇÕES NO CÓDIGO
        if modo_firefox == 'oculto':
            os.environ['MOZ_HEADLESS'] = '1'                                                    # * DEIXA O FIREFOX INVISÍVEL
        else:
            pass
    
    
    def criar_monitor(self):
        ''' * Cria os aparatos do front-end, objetivo alvo: monitoramento'''
        
        icone = resource_filename(__name__, 'favicon.ico')                                      # * PARA CARREGAR O ICONE NO ARQUIVO BINÁRIO COMPILADO              
        self.janela.iconbitmap(icone)                                                           # * DEFINE O ICONE NA JANELA
        self.janela.title(f"Robô {Config.ROBOT_NAME.value}, Versão: {Config.VERSION.value}")    # * DEFINE O TITULO DA JANELA
        self.janela.resizable(True,True)                                                        # * DEIXA A JANELA ABILITADA PARA REDIMENSIONAMENTO
        self.janela.geometry("750x450")                                                         # * DEFINE O TAMANHO INICIAL DA JANELA
        frameTexto = tkinter.Frame(self.janela)                                                 # * CRIA UM FRAME PARA O TEXTO QUE FICARÁ NA JANELA
        frameTexto.pack(fill='both',expand=1)                                                   # * CHAMA O FRAME DE TEXTO PARA A JANELA
        tkinter.Label(frameTexto,text=" ").pack(side=tkinter.LEFT)                              # * CRIA UM LABEL SOMENTE PARA ORGANIZAÇÃO VISUAL DA JANELA
        self.txtResult = tkinter.Text(frameTexto)                                               # * CRIA A CAIXA DE TEXTO PARA A JANELA
        self.txtResult.pack(side=tkinter.LEFT,expand=True,fill='both')                          # * COLOCA A CAIXA DE TEXTO NA JANELA
        scrl = tkinter.Scrollbar(frameTexto,command=self.txtResult.yview)                       # * CRIA UM SCROOL PARA A CAIXA DE TEXTO
        scrl.pack(side=tkinter.RIGHT,fill=tkinter.Y)                                            # * COLOCA O SCROOL DA CAIXA DE TEXTO NA JANELA
        tkinter.Label(frameTexto,text=" ").pack(side=tkinter.LEFT)                              # * CRIA UM LABEL SOMENTE PARA ORGANIZAÇÃO VISUAL DA JANELA
        tkinter.Label(self.janela,text=" ").pack(side=tkinter.BOTTOM)                           # * CRIA UM LABEL SOMENTE PARA ORGANIZAÇÃO VISUAL DA JANELA

        self.txtResult.tag_config('RED',    foreground='#FF0000')                               # * 
        self.txtResult.tag_config('GREEN',  foreground='#006400')                               # * 
        self.txtResult.tag_config('ORANGE', foreground='#FF8C00')                               # * 
        self.txtResult.tag_config('PURPLE', foreground='#A020F0')                               # * 
        self.txtResult.tag_config('INDIGO', foreground='#4B0082')                               # * CONFIGURAÇÕES DE OPÇÕES DE CORES PARA O TEXTO DAS MENSAGENS
        self.txtResult.tag_config('BROWN',  foreground='#8B4513')                               # * 
        self.txtResult.tag_config('TOMATO', foreground='#FF6347')                               # * 
        self.txtResult.tag_config('BLUE',   foreground='#4169e1')                               # * 
        self.txtResult.tag_config('BLACK',  foreground='#000000')                               # * 


        def recursivo():
            ''' * Função recursiva para verificar continuamente se existe mensagens para exibir na tela'''
            while self.caixa_de_msg.qsize():                                                    # * PARA CADA ITEM ENVIADO PARA O QUEUE
                carta = self.caixa_de_msg.get()                                                 # * CAPTURA O OBJETO ENVIADO PARA O QUEUE
                texto = carta[0]                                                                # * MENSAGENS DE TEXTO ENVIADA
                cor = carta[1]                                                                  # * COR QUE DESEJA QUE SEJA EXIBIDA A MENSAGEM    
                self.txtResult.insert(f'{self.conta_linha}.0',str(texto)+'\n',cor)              # * COLOCA A MENSAGEM NA CAIXA DE TEXTO
                self.conta_linha = self.conta_linha +1                                          # * CONFIGURA PARA A PROXIMA MENSAGEM SER COLOCADA NA LINHA DE BAIXO DA CAIXA DE TEXTO
                self.txtResult.see("end")                                                       # * DEFINE PARA A VISUALIZAÇÃO IR PARA O FIM DA CAIXA DE TEXTO
            self.janela.after(200,recursivo)                                                    # * APÓS 200 MILISEGUNDOS CHAMA NOVAMENTE A FUNÇÃO 'recursivo'
        recursivo()                                                                             # * CHAMA A FUNÇÃO 'recursivo' PELA PRIMEIRA VEZ
        
        self.janela.mainloop()                                                                  # * INICIA A JANELA, FIM DA CIRAÇÃO DO MONITOR


    def registrando(self, txt, color='BLACK', vida='DIA'):
        """ * Tratativa dos registros gerados manualmente
        # Args:
            * txt  : A mensagem que será enviada ou salva
            * color: Cor que deseja que a a mensagem seja exibida
            * vida : Tempo de vida util que o log deve ser mantido
                    * 'DIA'
                    * 'SEMANA'
                    * 'MES'
                    * 'ANO'
                    * 'ETERNO'
        """
        registro = str(datetime.now().strftime('%Y/%m/%d-%H:%M:%S-'))+str(txt)                  # * FORMATO EM QUE FICARÁ A MENSAGEM
        self.caixa_de_msg.put([registro,color])                                                 # * ENVIO DA MENSAGEM PARA O FRONT
        banco.Robo.Log.grava(txt,vida,f'{Config.ROBOT_NAME.value}')                             # * SALVA O LOG NO BANCO DE DADOS
        
        registro_dtm = str(datetime.now().strftime('%Y%m%d'))                                   # * 
        nome_arquivo_log =f'Log_{Config.ROBOT_NAME.value}_{registro_dtm}.txt'                   # * 
        arquivo_log = open(nome_arquivo_log,'a')                                                # * SALVA O LOG LOCALMENTE NA MÁQUINA
        print (registro, file=arquivo_log)                                                      # * 
        arquivo_log.close()                                                                     # * 
        pass
    
    
    def apaga_logs(self):
        '''Limpa os arquivos de logs mais antigos'''
        list_arquivos_log = glob('Log_' + Config.ROBOT_NAME.value + '*')                        # * LISTA OS ARQUIVOS DE LOGS EXISTENTES NA PASTA
        for for_arquivo_log in list_arquivos_log:                                               # * PARA CADA ARQUIVO FAZ A VERIFICAÇÃO
            data_arquivo = for_arquivo_log.split(Config.ROBOT_NAME.value)[1]
            data_arquivo = datetime.strptime(data_arquivo,'%Y%m%d.txt')
            if data_arquivo < datetime.now() - timedelta(days=8):                               # * SE FOR MAIS ANTIGO QUE OS DIAS ESTIPULADOS, APAGA O ARQUIVO
                os.remove(for_arquivo_log)
            else:
                pass       
        banco.Robo.Log.apaga()                                                                  # * LIMPA LOGS ANTIGOS NO BANCO DE DADOS        


    def decripta(self,texto):
            """
            Função que descriptografa senha do gestor para poder acessar o sats
            """
            global PASSPHRASE
            PASSPHRASE = b'25b890c6103dbc87e533eb0338fffc1f2adf6eab4c4873cfdd4f24c497d49704';
            try:
                key = binascii.unhexlify(PASSPHRASE)
                encrypted = json.loads(base64.b64decode(texto).decode('ascii'))
                encrypted_data = base64.b64decode(encrypted['data'])
                iv = base64.b64decode(encrypted['iv'])
                tag = base64.b64decode(encrypted['tag'])
                cipher = AES.new(key, AES.MODE_GCM, iv)
                decrypted = cipher.decrypt_and_verify(encrypted_data, tag)
                return json.loads(base64.b64decode(decrypted).decode('ascii'))
            except:
                return 'Erro ao decriptar'
    
    
    def login_from_zero(self,contrato):
        ''' * Faz o login do gestor no sats conforme o contrato informado'''
        gestor_bd = banco.Main.seleciona_gestor(contrato)                                      # * SELECIONA O PROXIMO GESTOR ATIVO DO CONTRATO
        if gestor_bd != None:                                                                   # * CASO EXISTA GESTOR ATIVO NO CONTRATO
            gestor_user = gestor_bd[0]                                                          # * SELECIONA MATROCULA DO GESTOR
            gestor_pass = self.decripta(gestor_bd[1])                                           # * SELECIONA SENHA DO GESTOR
            if self.sats.login(gestor_user,gestor_pass) == 'ok':                               # * TENTA FAZER O LOGIN NO sats
                retorno = 'ok'
            else:                                                                               # * CASO NÃO CONSIGA FAZER O LOGIN COM O GESTOR SELECIONADO
                banco.Main.atualiza_status_gestor(gestor_user)                                 # * DEFINE A SENHA DO GESTOR COMO INVALIDA NO BANCO DE DADOS
                banco.Main.envia_email_gestor_invalido(gestor_user)                            # * ENVIA UM E-MAIL PARA O GESTOR INFORMANDO QUE SUA SENHA ESTÁ INVALIDA
                self.registrando(f'Senha do gestor {gestor_user} incorreta','RED','MES')
                second_chance = self.login_from_zero(contrato)                                  # * TENTA NOVAMENTE SELECIONANDO O PROXIMO GESTOR ATIVO DO CONTRATO
                retorno = second_chance                                                         # * CAPTURA A RESPOSTA EM CASCATA DEVIDO À RECURSIVIDADE
        else:
            self.registrando(f'Não temos gestor ativo para o contrato {contrato}','RED','MES')  # * CASO NÃO EXISTA GESTOR VALIDO PARA O CONTRATO ENTÃO A FUNÇÃO RETORNA 'erro'
            retorno = 'erro'
        return retorno
    
    
    def controle_de_acoes(self):
        ''' * Função principal, responsável por orquestrar a rotina de reset de senhas'''
        self.registrando('Iniciando Navegador... isto pode demorar um pouco...','BLUE','SEMANA')
        self.sats = sats.Sessao()                                                             # * INICIA O NAVEGADOR FIREFOX
        status_janela = self.janela.state()                                                     # * CAPTURA O STATUS DA JANELA FRONT-END DO ROBÔ
        self.proxima_exec = datetime.now()-timedelta(seconds=1)                                 # * CONTROLE DE EXECUÇÃO DO ROBÔ
        while status_janela ==  'normal':                                                       # * LOOP PERPÉTUO ENQUANTO A JANELA DO FRONT-END DO ROBÔ ESTIVER ABERTA
            if self.proxima_exec < datetime.now():                                              # * CASO ESTEJE DENTRO DO HORARIO DE EXECUÇÃO
                lista_matriculas_reset = banco.Main.seleciona_matriculas_reset()               # * VERIFICA NO BANCO DE DADOS SE EXISTEM MATRICULAS PARA RESETAR
                if len(lista_matriculas_reset) == 0:
                    self.registrando('Não existe matrículas para reset de senha')
                else:                                                                           # * CASO EXISTAM MATRICULAS NO BANCO DE DADOS PARA RESETAR
                    self.registrando(f'Foi encontrado {len(lista_matriculas_reset)} matrículas para resetar','BLUE','SEMANA')
                    login_contrato          = None                                              # * LIMPEZA DE VARIÁVEIS ANTES DA EXECUÇÃO DO LOOPING DA LISTA DE RESETS
                    contrato_reset_anterior = None                                              # * PARA QUE POSSA SER REAPROVEITADO O LOGIN CASO O GESTOR SEJA DO MESMO CONTRATO
                    for item_reset in lista_matriculas_reset:                                   # * PARA CADA RESET NA LISTA DE RESETS
                        resetar_matricula       = item_reset[0]                                 # * MATRICULA QUE SE DESEJA RESETAR
                        solicitante             = item_reset[1]                                 # * QUEM SOLICITOU QUE A MATRICULA SEJA RESETADA
                        contrato_reset_atual    = banco.Main.seleciona_contrato_matricula(resetar_matricula)               # * VERIFICA NO BANCO DE DADOS A QUAL CONTRATO PERTENCE A MATRICULA QUE SE DESEJA RESETAR
                        if contrato_reset_atual != contrato_reset_anterior:                                                 # * CASO O CONTRATO SEJA DIFERENTE DA ULTIMA VEZ QUE FOI FEITO O LOGIN
                            contrato_reset_anterior = contrato_reset_atual                                                  # * REDEFINE AS VARIÁVEIS DE CONTRATO
                            if login_contrato  != None:                                                                     # * E SE JÁ FOI FEITO LOGON ANTES
                                self.sats.logoff()                                                                         # * REALIZA O LOGOFF DO sats
                            login_contrato = self.login_from_zero(contrato_reset_atual)                                     # * ENTÃO FAZ O LOGON COM O GESTOR DO CONTRATO ATUAL
                            if login_contrato == 'ok':                                                                      # * SE O LOGIN FOI REALIZADO COM SUCESSO
                                self.sats.resetar_senha()                                                                  # * VAI PARA A PAGINA DO sats QUE RESETA A SENHA
                                reset_de_senha = self.sats.selecionar_matricula_reset(resetar_matricula)                   # * E RESETA A MATRICULA DESEJADA
                                if reset_de_senha == 'ok':                                                                  # * SE O RESET FOI BEM SUCEDIDO
                                    banco.Main.atualiza_status_reset(resetar_matricula,1)                                  # * ATUALIZA ESTA INFORMAÇÃO NA TABELA DE REQUISIÇÕES DO SATS
                                    banco.Main.envia_email_solicitante(solicitante, resetar_matricula, 1)                  # * E ENVIA UM E-MAIL INFORMANDO O SUCESSO PARA O SOLICITANTE E PARA O USUÁRIO DA MATRICULA RESETADA
                                    self.registrando (f'Resetado a matrícula {resetar_matricula}','GREEN','SEMANA')
                                else:                                                                                       # * E EM CASO DE FALHA NO RESET DE SENHA
                                    banco.Main.atualiza_status_reset(resetar_matricula,2)                                  # * ATUALIZA ESTA INFORMAÇÃO NA TABELA DE REQUISIÇÕES DO SATS, COM ERRO
                                    banco.Main.envia_email_solicitante(solicitante, resetar_matricula, 2)                  # * E ENVIA UM E-MAIL INFORMANDO O ERRO PARA O SOLICITANTE
                                    self.registrando (f'Falha no reset da matrícula {resetar_matricula}','RED','MES')
                            else:                                                                                           # * CASO ELE NÃO TENHA CONSEGUIDO FAZER LOGIN COM NENHUM GESTOR DO CONTRATO ELE TENTA NOVAMENTE MAIS TARDE
                                self.registrando (f'Tentarei resetar a matrícula {resetar_matricula} mais tarde.','RED','MES')      
                        else:                                                                                               # * SE O CONTRATO FOR O MESMO UTILIZADO NO ULTIMO RESET DE SENHA ENTÃO É REAPROVEITADO O LOGIN
                            contrato_reset_anterior = contrato_reset_atual                                                  # * REDEFINE AS VARIAVEIS PARA A VERIFICAÇÃO DO PROXIMO LOOPING
                            if login_contrato == 'ok':                                                                      # * SE A ULTIMA VEZ QUE FOI FEITO O LOGIN RESULTOU EM SUCESSO
                                self.sats.resetar_senha()                                                                  # * ELE VAI PARA A PAGINA DE RESET DE SENHA
                                reset_de_senha = self.sats.selecionar_matricula_reset(resetar_matricula)                   # * E RESETA A MATRICULA DESEJADA
                                if reset_de_senha == 'ok':                                                                  # * SE O RESET FOI BEM SUCEDIDO
                                    banco.Main.atualiza_status_reset(resetar_matricula,1)                                  # * ATUALIZA ESTA INFORMAÇÃO NA TABELA DE REQUISIÇÕES DO SATS
                                    banco.Main.envia_email_solicitante(solicitante, resetar_matricula, 1)                  # * E ENVIA UM E-MAIL INFORMANDO O SUCESSO PARA O SOLICITANTE E PARA O USUÁRIO DA MATRICULA RESETADA
                                    self.registrando (f'Resetado a matrícula {resetar_matricula}','GREEN','SEMANA')
                                else:                                                                                       # * E EM CASO DE FALHA NO RESET DE SENHA
                                    banco.Main.atualiza_status_reset(resetar_matricula,2)                                  # * ATUALIZA ESTA INFORMAÇÃO NA TABELA DE REQUISIÇÕES DO SATS, COM ERRO
                                    banco.Main.envia_email_solicitante(solicitante, resetar_matricula, 2)                  # * E ENVIA UM E-MAIL INFORMANDO O ERRO PARA O SOLICITANTE
                                    self.registrando (f'Falha no reset da matrícula {resetar_matricula}','RED','MES')                   
                            else:                                                                                           # * CASO ELE NÃO TENHA CONSEGUIDO FAZER LOGIN COM NENHUM GESTOR DO CONTRATO ELE TENTA NOVAMENTE MAIS TARDE
                                self.registrando (f'Tentarei resetar a matrícula {resetar_matricula} mais tarde.','RED','MES')          
                    self.sats.logoff()                                                                                     # * AO TERMINAR TODOS OS RESETS DAS MATRICULAS NA LISTA, É EFETUADO O LOGOFF
                    self.registrando (f'Terminado rotina','BLUE','SEMANA')
                self.proxima_exec = datetime.now()+timedelta(seconds=30)                                                    # * DEFINE A PROXIMA EXECUÇÃO DA ROTINA PARA DAQUI A 30 SEGUNDOS
            try:
                status_janela = self.janela.state()                                                                         # * VERIFICA SE A JANELA DO FRONT-END DO ROBÔ CONTINUA ABERTA
            except:
                status_janela = 'Finalizado'
            sleep(2)                                                                                                        # * DORME 2 SEGUNDOS ANTES DE VER SE JÁ ESTÁ NA HORA DE EXECUTAR NOVAMENTE A ROTINA


automacao() # * FAZ A INVOCAÇÃO DA CASSE PRINCIPAL PARA A EXECUÇÃO DO ROBÔ