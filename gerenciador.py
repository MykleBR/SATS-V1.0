from datetime import datetime, timedelta
from config import Config
from pathlib import Path
from time import sleep
from glob import glob
import os.path
import os
import psutil

sizeLog             = None                                      # VARIÁVEL DO TAMANHO DO LOG
newSizeLog          = None                                      # VARIÁVEL DO TAMANHO DO LOG ATUALIZADA
robo_exe            = f'Robo_{Config.ROBOT_NAME.value}.exe'     # NOME DO ARQUIVO EXECUTÁVEL DO ROBÔ
pre_robo_log        = f'Log_{Config.ROBOT_NAME.value}_'         # NOME DO ARQUIVO DE LOG DO ROBÔ
lista_pids_filhos   = []
tempo_verificacao   = 5                                         # TEMPO TOLERÁVEL PARA A PRIMEIRA INICIALIZAÇÃO

os.system(f'title Gerenciador {robo_exe}')

def registrando(txt):
    registro = str(datetime.now().strftime('%Y/%m/%d-%H:%M:%S-'))+str(txt)
    registro_dtm = str(datetime.now().strftime('%Y%m%d'))
    nome_arquivo_log =f'Log_Gerenciador_{Config.ROBOT_NAME.value}_{registro_dtm}.txt'
    arquivo_log = open(nome_arquivo_log,'a')
    print (registro, file=arquivo_log)
    print (registro)
    arquivo_log.close()        

def apaga_logs():
    '''Limpa os arquivos de logs mais antigos'''
    list_arquivos_log = glob('Log_Gerenciador_' + Config.ROBOT_NAME.value + '*')    # * LISTA OS ARQUIVOS DE LOGS EXISTENTES NA PASTA
    for for_arquivo_log in list_arquivos_log:                                       # * PARA CADA ARQUIVO FAZ A VERIFICAÇÃO
        data_arquivo = for_arquivo_log.split(Config.ROBOT_NAME.value)[1]
        data_arquivo = datetime.strptime(data_arquivo,'%Y%m%d.txt')
        if data_arquivo < datetime.now() - timedelta(days=8):                       # * SE FOR MAIS ANTIGO QUE OS DIAS ESTIPULADOS, APAGA O ARQUIVO
            os.remove(for_arquivo_log)

def reinicializar():
    global lista_pids_filhos, tempo_verificacao
    for pid in lista_pids_filhos:
       os.system(f'taskkill /pid {str(pid)} /F') 
    lista_pids_filhos   = []
    os.popen(str(robo_exe))
    tempo_verificacao = 5                                                           # * DEFINE A PROXIMA VERIFICAÇÃO COM MAIS TEMPO, PARA NÃO OCORRER ERRO

def get_pids():
    pid_principal = os.getpid()
    cadeia_de_processos = psutil.Process(pid_principal)
    for processo in cadeia_de_processos.children(recursive=True):
        if processo.pid not in lista_pids_filhos: 
            lista_pids_filhos.append(processo.pid)

registrando(f'Iniciando "{robo_exe}" pela primeira vez...')
os.popen(robo_exe)

sleep (60*tempo_verificacao)

##### A PARTIR DESTE PONTO É UM LOOPING ETERNO
while True:
    get_pids()
    
    ##### REINICIA O ROBÔ PELO MENOS 1 VEZ AO DIA PARA CERTIFICAR QUE ESTÁ TUDO CERTO.
    if (datetime.now()).strftime('%H') == '02':
        registrando(f"REINICIALIZAÇÃO DIÁRIA: {str(robo_exe)}")
        reinicializar()
    robo_log = f'{pre_robo_log}{datetime.now().strftime("%Y%m%d")}.txt' 
    ##### CAPTURA O TAMANHO ATUAL DO LOG DO ROBÔ
    try:
        newSizeLog = Path(robo_log).stat().st_size
    except:
        registrando('Excessão - falha na busca o tamanho do log')
    ##############################################################
    ##### COMPARA O TAMANHO DO LOG ATUAL COM O DA ULTIMA VEZ QUE FEZ A VERIFICAÇÃO
    ##### CASO NÃO TENHA ALTERAÇÃO ELE JÁ REINICIA O ROBÔ
    ##### CASO O LOG ESTEJA SENDO GRAVADO NORMALMENTE, ELE VERIFICA POSTERIORMENTE.
    if sizeLog == newSizeLog:
        registrando (f"Será necessário reiniciar {robo_exe}")
        reinicializar()
    else:
        registrando (f"Tudo ok...")
        tempo_verificacao = 1                                                       # * DEFINE A VERIFICAÇÃO COM MENOS TEMPO, PARA SER MAIS ACERTIVO                
    try:
        sizeLog = Path(str(robo_log)).stat().st_size
    except:
        registrando(f'Excessão - falha ao atualizar a variável do tamanho do log')
        pass
    ##############################################################

    sleep (60*tempo_verificacao)