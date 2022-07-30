from bs4 import BeautifulSoup
import requests
from utils import * 
# #
# Desarrollado por Wachu985
# Libreria de Conexion con Wifi Etecsa Version 1.0
# Contactar en Telegram:
# https://t.me/Wachu985
# #

class Conexion(object):
    
    def __init__(self,user,passw):
        self.username = user
        self.password = passw
        self.loged = False
        self.s = requests.Session()
        self.soup = None

    def request(self):
        with requests.Session() as self.s:
            response = self.s.get('https://secure.etecsa.net:8443/',headers=HEADER,timeout=10)
        content = response.text
        self.soup = BeautifulSoup(content,features='html.parser')

    def queryInput(self,text):
        input = self.soup.find_all('input',id=text)
        for i in input:
            if i.get('id') == text:
                return True,i.get('value')
        return False,''

    """Buscar si hay Error al Inicio de Sesion"""
    def finderror(self):
        lo = self.soup.find_all('script')
        for i in lo:
            if 'El usuario ya está conectado' in str(i.string):
                return True,'El usuario ya Esta Conectado'
            elif 'No se pudo autorizar al usuario' in str(i.string):
                return True,'Revise el Usuario o la Contrasenia'
            elif 'Entre el nombre de usuario y contraseña correctos.' in str(i.string):
                return True,'Revise el Usuario o la Contrasenia'
            elif 'Su tarjeta no tiene saldo disponible' in str(i.string):
                return True,'No Tiene Saldo en la Cuenta'
            elif 'El nombre de usuario o contraseña son incorrectos' in str(i.string):
                return True,'El nombre de usuario o contraseña son incorrectos.'
            elif 'Su estado de cuenta es anormal' in str(i.string):
                return True,'Su estado de cuenta es anormal.'
                
        return False,''

    """Buscamos el Tiempo de la Cuenta"""
    def selecTime(self):
        atri = self.soup.find('script').string
        ini = atri.rfind('op=getLeftTime')
        fin = atri.rfind('g_httpRequest.open("post", "/EtecsaQueryServlet", true);')
        valores = atri[ini:fin].replace('"\r\n            \t\t        \t         ','').replace('"\r\n            \t\t                     ','').replace('";\r\n\t            ','').replace('+ "','').split('&')
        li = []
        for val in valores:
            li.append(val.split('=')[-1])
        payload = {}
        for val,val2 in zip(li,VALUES):
            payload[val2] = val
        response = self.s.post("https://secure.etecsa.net:8443//EtecsaQueryServlet",data=payload,timeout=10)
        return response.text



    """LOGIN"""
    def login(self):
        self.request()
        if not self.loged:
            param = {}
            for f in PARAMLOGIN:
                enco,val = self.queryInput(f)
                if enco:
                    param[f] = val

            ssid = ''
            lang = ''
            param['ssid'] = ssid
            param['lang'] = lang
            param['username'] = self.username
            param['password'] = self.password
                
            response = self.s.post("https://secure.etecsa.net:8443//LoginServlet",data=param,timeout=10)

            self.soup = BeautifulSoup(response.text,features='html.parser')

            err,val =  self.finderror()
            if not err:
                tim = self.selecTime()
                self.loged = True
            else:
                tim = ''
            ret = {'error':err,'valerr':val,'time':tim}
            return ret
        else:
            ret = {'error':True,'valerr':'Ya se Encuentra Iniciado','time':'00:00:00'}
            return ret
    """Verifacion de Logeado"""
    def isloged(self):
        if self.loged:
            err,val =  self.finderror()
            if not err:
                tim = self.selecTime()
                self.loged = True
            else:
                tim = ''
            ret = {'error':err,'valerr':val,'time':tim}
            return ret    
        
    """LOGOUT"""
    def logout(self):
        if self.loged:
            atri = self.soup.find('script').string
            ini = atri.rfind('ATTRIBUTE_UUID')
            fin = atri.rfind('g_httpRequest.open("post", "/EtecsaQueryServlet", true);')
            valores = atri[ini:fin].replace('"\r\n            \t\t        \t         ','').replace('"\r\n            \t\t                     ','').replace('";\r\n\t            ','').replace('+ "','').split('&')
            li = []
            for val in valores:
                li.append(val.split('=')[-1])
            payload = {}
            for val,val2 in zip(li,VALUES2):
                payload[val2] = val
            payload['remove'] = '1'
            response = self.s.post("https://secure.etecsa.net:8443//LogoutServlet",data=payload,timeout=10)
            if 'SUCCESS' in response.text:
                self.loged = False
                return True
            elif 'FAILURE' in response.text:
                return False
        else:
            return False

    def set_user(self,user):
        self.username = user
    
    def set_passw(self,passw):
        self.password = passw