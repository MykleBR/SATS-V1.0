
##### * ARQUIVO RESPONSÁVEL PELA CONEXÃO E AÇÕES COM O SITE 'X' ATRAVÉS DO FIREFOX
##### * 
##### * ESTE ARQUIVO É CHAMADO PELO ARQUIVO: 'main.py'
##### * 
##### * ESTE ARQUIVO NÃO CHAMA OUTROS ARQUIVOS
##### * 


from selenium.webdriver.common.keys import Keys     # * PARA USO DE TECLAS NO FIREFOX
from pkg_resources import resource_filename         # * PARA COMPILAR RECURSOS NO BINÁRIO
from selenium import webdriver                      # * PARA CRIAR UMA SESSÃO NO FIREFOX
from time import sleep                              # * PARA COMPASSAR O ROBÔ

class Sessao:
    '''Classe onde é criada e manipulada uma sessão do Firefox'''
    
    def __init__(self):
        variavel_gecko = resource_filename(__name__, 'geckodriver.exe')                             # * PARA O GECKODRIVER SER INCLUSO NA COMPULAÇÃO
        self.navegador = webdriver.Firefox (executable_path = variavel_gecko)                       # * CRIA A SESSÃO DO FIREFOX
        
    def try_send(self,elemento,texto,tentativa=1):
        ''' Faz a tentativa de envio de texto para o xpath informado.
        Caso não consiga na primeira vez, continua tentando mais 8 vezes.
        Realiza uma tentativa a cada 1 segundo.
        # Parâmetros
            * elemento : xpath alvo da ação  
            * texto :   que será enviado para o elemento
        '''
        if tentativa < 10:
            try:
                self.navegador.find_element('xpath',elemento).send_keys(texto)
                retorno = 'ok'
            except:
                retorno = 'erro'
                sleep(1)
                tentativa += 1
                self.try_send(elemento,texto,tentativa)
        else:
            retorno = 'erro'
        return retorno

    def try_click(self,elemento,tentativa=1):
        '''Faz o click no elemento xpath desejado. Em caso de falha tenta mais 8 vezes a cada 1 segundo
        '''
        if tentativa < 10:
            try:
                self.navegador.find_element('xpath',elemento).click()
                retorno = 'ok'
            except:
                retorno = 'erro'
                sleep(1)
                tentativa += 1
                self.try_click(elemento,tentativa)
        else:
            retorno = 'erro'
        return retorno

    def try_clear(self,elemento,tentativa=1):
        '''Apaga os textos escritos no elemento xpath desejado. Em caso de falha tenta mais 8 vezes a cada 1 segundo
        '''        
        if tentativa < 10:
            try:
                self.navegador.find_element('xpath',elemento).clear()
                retorno = 'ok'
            except:
                retorno = 'erro'
                sleep(1)
                tentativa += 1
                self.try_clear(elemento,tentativa)
        else:
            retorno = 'erro'
        return retorno

    def login(self,usuario,senha):
        '''Faz o GET inicial na pagina do X, e em seguida realiza o login com usuário e senha do gestor'''
        self.navegador.get  ('X')
        self.try_send       ('//*[@id="loginForm:accountId"]',usuario)
        self.try_send       ('//*[@id="loginForm:password"]',senha)
        self.try_click      ('//*[@id="loginForm:loginButton"]')
        if self.try_click   ('/html/body/div[2]/div[1]/div[1]/nav/ul[2]/li[3]/a/div/span') == 'ok':
            retorno = 'ok'
        else:               # * TENTA UMA SEGUNDA VEZ ANTES DE RETORNAR COMO 'ERRO'
            sleep(3)
            self.navegador.get  ('X')
            self.try_send       ('//*[@id="loginForm:accountId"]',usuario)
            self.try_send       ('//*[@id="loginForm:password"]',senha)
            self.try_click      ('//*[@id="loginForm:loginButton"]')
            if self.try_click   ('/html/body/div[2]/div[1]/div[1]/nav/ul[2]/li[3]/a/div/span') == 'ok':
                retorno = 'ok'
            else:
                retorno = 'erro'
        return retorno

    def resetar_senha(self):
        '''Vai da pagina home até a pagina de reset de senha'''
        self.try_click   ('/html/body/div[2]/div[1]/div[1]/nav/ul[1]/li[1]/a/i[1]')
        self.try_click   ('/html/body/div[2]/div[1]/div[3]/section/nav/ul[2]/li[2]/a/span[2]')
        self.try_click   ('/html/body/div[2]/div[1]/div[3]/section/nav/ul[2]/li[2]/div/ul/li[2]/a')

    def selecionar_matricula_reset(self,matricula):
        ''' Digita a matricula que deseja-se resetar na pagina, e seleciona o usuário
            Caso ele não consiga na primeira vez a função tenta mais algumas vezes antes de retornar "erro"
            Função feita com aninhamento de if-else para que seja mais fácil de editar a cadência do compasso das tentativas
        '''
        self.try_clear('/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input')    
        self.try_send('/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input',matricula)
        self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(Keys.BACKSPACE)
        sleep(2)
        self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(matricula[-1])
        sleep(2)
        if self.check_matricula_reset(matricula) == 'ok':
            self.finalizar_reset()
            result_select_mat = 'ok'        
        else:
            self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(Keys.BACKSPACE)
            sleep(2)
            self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(matricula[-1])
            sleep(2)
            if self.check_matricula_reset(matricula) == 'ok':
                self.finalizar_reset()
                result_select_mat = 'ok'        
            else:
                if self.check_matricula_reset(matricula) == 'ok':
                    self.finalizar_reset()
                    result_select_mat = 'ok'        
                else:
                    self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(Keys.BACKSPACE)
                    sleep(2)
                    self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(matricula[-1])
                    sleep(2)
                    if self.check_matricula_reset(matricula) == 'ok':
                        self.finalizar_reset()
                        result_select_mat = 'ok'        
                    else:
                        if self.check_matricula_reset(matricula) == 'ok':
                            self.finalizar_reset()
                            result_select_mat = 'ok'        
                        else:
                            self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(Keys.BACKSPACE)
                            sleep(2)
                            self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(matricula[-1])
                            sleep(2)
                            if self.check_matricula_reset(matricula) == 'ok':
                                self.finalizar_reset()
                                result_select_mat = 'ok'        
                            else:
                                if self.check_matricula_reset(matricula) == 'ok':
                                    self.finalizar_reset()
                                    result_select_mat = 'ok'        
                                else:
                                    self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(Keys.BACKSPACE)
                                    sleep(2)
                                    self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[1]/div/div/input').send_keys(matricula[-1])
                                    sleep(2)
                                    if self.check_matricula_reset(matricula) == 'ok':
                                        self.finalizar_reset()
                                        result_select_mat = 'ok'        
                                    else:
                                        result_select_mat = 'Matrícula não encontrada'        
        return result_select_mat
                                        
    def check_matricula_reset(self,matricula):
        '''Informa se a matrícula que foi retornada pela pagina de internet é realmente a matricula desejada para o resete'''
        try:
            alvo = self.navegador.find_element('xpath','/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[2]/div/div/div[1]/h3/a').get_attribute('innerHTML')
            alvo = (alvo.replace('\t','')).replace('\n','')
        except:
            alvo = ''
        if str(alvo).lower() == str(matricula).lower():        
            result_test = 'ok'
        else:
            result_test = 'erro' 
        return result_test

    def finalizar_reset(self):
        '''Faz os passos finais para a realização do reset'''
        self.try_click   ('/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-home/div/div/div/div/div[2]/div/div/div[2]/div/a')
        self.try_send    ('//*[@id="paw"]','123')
        self.try_click   ('/html/body/div[2]/div[2]/div/section/ng-view/passwordmanager-change/div/div/div/div[2]/div/div[1]/form/div[3]/div[2]/button')
        self.try_click   ('/html/body/div[5]/div/div[3]/button[3]')
        self.try_click   ('/html/body/div[5]/div/div[3]/button[1]')

    def logoff (self):
        '''Faz logoff do gestor atual na pagina do X'''
        self.try_click('/html/body/div[2]/div[1]/div[1]/nav/ul[2]/li[3]/a/div/span')
        self.try_click('/html/body/div[2]/div[1]/div[1]/nav/ul[2]/li[3]/ul/li[4]/a')







