
##### * ARQUIVO COM VARIÁVEIS DE CONFIGURAÇÕES, E DADOS DE CONEXÕES COM INFORMAÇÕES SENSÍVEIS CRIPTOGRAFADAS
##### * 
##### * ESTE ARQUIVO É CHAMADO PELOS ARQUIVOS:
##### *     -main.py
##### *     -gerenciador.py
##### *     -banco.py
##### *     -compilar.bat (((OBS: A CONFIGURAÇÃO DESTE ARQUIVO É MANUAL)))
##### * 
##### * ESTE ARQUIVO NÃO CHAMA OUTROS ARQUIVOS.
##### * 

from enum import Enum                           # * PARA OBTER AS VARIAVEIS COMO UM DICIONÁRIO: CHAVE X VALOR
from cryptography.fernet import Fernet          # * PARA A DESCRIPTOGRAFIA DE DADOS SENSÍVEIS

class Sensiveis (Enum):
    """ * Armazena os dados sensíveis em um estado criptografado 
    """
    
    ##### * DADOS SENSÍVEIS CRIPTOGRAFADOS
    DBROB_PASS    = ""
    DBMain_PASS  = ""
    DB496_PASS    = ""
    
    
    def decrypta(senha):
        """ * Utilizado para descriptografar os dados sensíveis
        """
        key = b'N-nMdHttV7-iyB_FxR9Q6NlfkEd1QGp12iVfn-RPEZY='
        f = Fernet(key)    
        dec = f.decrypt(senha)
        dec = str(str(dec).replace("b'", "")).replace("'",'')
        return dec

class Config(Enum):
    """ * Informações de configurações centralizadas para controle.
    """
    ############# CONFIGURAÇÃO ATUAL
    ROBOT_NAME  = ''
    VERSION     = '0.0'
    
    # CONEXÃO COM BANCO DE DADOS DE CONTROLE DOS ROBOS
    DBROB_HOST  = ''
    DBROB_NAME  = ''
    DBROB_USER  = ''
    DBROB_PASS  = Sensiveis.decrypta(Sensiveis.DBROB_PASS.value.encode('ascii'))
    
    # CONEXÃO COM BANCO DE DADOS DE CONTROLE DOS Siadm
    DBMain_HOST  = ''
    DBMain_NAME  = ''
    DBMain_USER  = ''
    DBMain_PASS  = Sensiveis.decrypta(Sensiveis.DBMain_PASS.value.encode('ascii'))

    #CONEXÃO COM BANCO DE DADOS 496
    DB496_HOST  = ''
    DB496_NAME  = ''
    DB496_USER  = ''
    DB496_PASS  = Sensiveis.decrypta(Sensiveis.DB496_PASS.value.encode('ascii'))
	
    
		
