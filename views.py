import os
import sys
from PyQt5.QtWidgets import QPushButton,QLabel,QMainWindow,QComboBox,QLineEdit,QCheckBox,QGraphicsDropShadowEffect,QDialog,QApplication
from PyQt5.QtCore import QSize,QPropertyAnimation,QAbstractAnimation,QRect,Qt,QTimer
from PyQt5.QtGui import QIcon,QPainter,QFontMetrics,QFont,QPixmap,QColor
from screeninfo import get_monitors
from Conexion import Conexion
from utils import *
import pickle
import requests
# #
# Desarrollado por Wachu985
# Vistas de la App Mi Cuenta Nauta (Version Linux)
# Contactar en Telegram:
# https://t.me/Wachu985
# #


"""==================================Definiendo Label Vertical=================================="""
class VerticalLabel(QLabel):

    def __init__(self, *args):
        QLabel.__init__(self, *args)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(0, self.height())
        painter.rotate(-90)
        # calculate the size of the font
        fm = QFontMetrics(painter.font())
        xoffset = int(fm.boundingRect(self.text()).width()/2)
        yoffset = int(fm.boundingRect(self.text()).height()/2)
        x = int(self.width()/2) + yoffset
        y = int(self.height()/2) - xoffset
        # because we rotated the label, x affects the vertical placement, and y affects the horizontal
        painter.drawText(y, x, self.text())
        painter.end()
        
    def minimumSizeHint(self):
        size = QLabel.minimumSizeHint(self)
        return QSize(size.height(), size.width())

    def sizeHint(self):
        size = QLabel.sizeHint(self)
        return QSize(size.height(), size.width())

"""=======================Creando Animaciones==============================="""
class hoverButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        
        self.setMouseTracking(True)

        self.fuente = self.font()

        self.posicionX = int
        self.posicionY = int

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = self.pos().y()
        
        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX-15, self.posicionY-6, 120, 38))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)
        
        self.fuente.setPointSize(11)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(10)
        self.setFont(self.fuente)
        
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 100, 30))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)


class ButtonDialog(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        
        self.setMouseTracking(True)

        self.fuente = self.font()

        self.posicionX = int
        self.posicionY = int

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = self.pos().y()
        
        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX-15, self.posicionY-6, 80, 30))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)
        
        self.fuente.setPointSize(11)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(10)
        self.setFont(self.fuente)
        
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 70, 25))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)


class hoverLabel(QLabel):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        
        self.setMouseTracking(True)

        self.fuente = self.font()

        self.posicionX = int
        self.posicionY = int

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = self.pos().y()
        
        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX, self.posicionY, 40, 50))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)
        
        self.fuente.setPointSize(11)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(10)
        self.setFont(self.fuente)
        
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 40, 40))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)
"""========================================================================="""


"""========================Creando CLase Principal===================================="""
class MainApp(QMainWindow):
    
    def __init__(self,parent = None ,*args, **kwargs):
        super(MainApp, self).__init__(parent)
        """Tamano de la Pantalla --setMiniumSize() --setMaximumSize() --setFixedSize()"""
        self.setFixedSize(500,200)

        """Definiendo Titulo de la ventana"""
        self.setWindowTitle('Mi Cuenta Nauta')
        self.setStyleSheet("MainApp{background-image: url(./images/image.jpg)}")
        self.setWindowIcon(QIcon('./images/internet.png'))

        if os.path.exists('./data.pickle'):
            if not os.stat('./data.pickle').st_size == 0:
                pickle_file = open('data.pickle', 'rb')
                print('Cargando')
                global Usuarios
                Usuarios = pickle.load(pickle_file)
                pickle_file.close()
        else:
            pickle_file = open('data.pickle', 'w')
            pickle_file.close()



        # """Input Usuario"""
        # self.user = QLineEdit(self)
        # self.user.setPlaceholderText('Inserte el Usuario')
        # self.user.setClearButtonEnabled(True)
        # self.user.setGeometry(int(500/2)-100,50,200,30)
        # self.user.setMaxLength(50)
        self.resolucion_ancho = 0
        self.resolucion_alto = 0
        self.get_size()
        left = (self.resolucion_ancho /2) - (self.frameSize().width() / 2)
        top = (self.resolucion_alto /2) - (self.frameSize().height() / 2)
        self.move(int(left), int(top))

        """Combo Usuario"""
        self.conbo = QComboBox(self)
        self.conbo.setGeometry(int(500/2)-175,50,350,30)
        self.conbo.setEditable(True)
        self.listarRegistros()
        self.conbo.setObjectName(("comboBox"))
        self.conbo.setPlaceholderText('Inserte la Contrasena')
        self.conbo.setFont(QFont('Arial',15,QFont.Bold))
        self.conbo.setStyleSheet("background-color: rgba(100, 255, 255, 10);color:#FFFFFF;border-bottom: 1px solid blue; border-left: 1px solid blue;border-radius: 5px;")
        self.colocarSombra(self.conbo)

        """Labels"""
        self.labe_user = QLabel('Usuario:',self)
        self.labe_user.setGeometry(55,20,100,30)
        self.labe_user.setAlignment(Qt.AlignCenter|Qt.AlignLeft)
        self.labe_user.setStyleSheet('color:#FFFF00')
        self.colocarSombra(self.labe_user)

        self.labe_pass = QLabel('Contraseña:',self)
        self.labe_pass.setGeometry(67,75,100,30)
        self.labe_pass.setAlignment(Qt.AlignCenter|Qt.AlignLeft)
        self.labe_pass.setStyleSheet('color:#FFFF00')
        self.colocarSombra(self.labe_pass)

        self.labe_user_icon = QLabel('',self)
        self.labe_user_icon.setPixmap(QPixmap('./images/icon.png'))
        self.labe_user_icon.setGeometry(30,45,100,40)
        self.colocarSombra(self.labe_user_icon)

        self.labe_config_icon = hoverLabel(self)
        self.labe_config_icon.setPixmap(QPixmap('./images/config.png'))
        self.labe_config_icon.setGeometry(450,0,40,40)
        self.labe_config_icon.setToolTip('Configuracion')
        self.labe_config_icon.setStyleSheet('color:#E90505')
        self.colocarSombra(self.labe_config_icon)

        self.labe_pass_icon = QLabel('',self)
        self.labe_pass_icon.setPixmap(QPixmap('./images/pass.png'))
        self.labe_pass_icon.setGeometry(30,95,100,40)
        self.colocarSombra(self.labe_pass_icon)

        """Input Contrasena"""
        self.passw = QLineEdit(self)
        self.passw.setPlaceholderText('Inserte la Contrasena')
        self.passw.setClearButtonEnabled(True)
        self.passw.setGeometry(int(500/2)-175,100,350,30)
        self.passw.setEchoMode(QLineEdit.Password)
        self.passw.setStyleSheet("background-color: rgba(100, 255, 255, 10);color:#FFFFFF;border-bottom: 1px solid blue; border-left: 1px solid blue;border-radius: 5px")
        self.colocarSombra(self.passw)


        """Check Box"""
        self.remenber = QCheckBox(self)
        self.remenber.setText('Recordar Usuario')
        self.remenber.setGeometry(int(500/2)-170,130,500,30)
        self.remenber.setStyleSheet('color:#E90505')
        self.remenber.setToolTip('Registrar Usuario en el Almacen')
        self.colocarSombra(self.remenber)

        """Boton"""
        self.btn = hoverButton(self)
        self.btn.setText('Iniciar Sesion')
        self.btn.setGeometry(int(500/2)-50,160,100,30)
        self.btn.setToolTip('Inciar Sesion en Etecsa')
        self.btn.setStyleSheet('border-style: solid;border-width: 1px;border-color: rgb(0, 51, 102);background-color: rgb(0, 51, 102);color: rgb(255, 255, 255);border-radius: 5px;')
        self.colocarSombra(self.btn)
        
        self.llenar(event='')
        """Disparadores"""
        self.passw.returnPressed.connect(self.iniciar)
        self.btn.clicked.connect(self.iniciar)
        self.conbo.currentIndexChanged.connect(self.llenar)
        self.labe_config_icon.mousePressEvent = self.config

    def listarRegistros(self):
        for key in Usuarios.keys():
            self.conbo.addItem(key)

    def llenar(self,event):
        if Usuarios:
            for key in Usuarios.keys():
                if key == self.conbo.currentText():
                    self.passw.setText(Usuarios[key])

    def config(self,event):
        self.config = ConfigApp()
        self.config.show()
        self.hide()
    """======Metodo Iniciar Sesion======"""
    def iniciar(self):
        if self.conbo.currentText() == '' or self.passw.text() == '':
            self.conbo.currentText()
            self.passw.setText('')
        else:
            conex = Conexion(self.conbo.currentText(),self.passw.text())                
            try:
                values = conex.login()
            except requests.exceptions.Timeout or requests.exceptions.ConnectionError:
                error = DialogError(error= 'Error de Conexion con Etecsa')
                error.exec()
                print('Error de Etecsa')
                return
            if not values['error']:
                print('Conectado Correctamente')
                """==============Guardado en Archivo Externo============"""
                if self.remenber.isChecked():
                    global Usuarios
                    cont = 0
                    for f in Usuarios.keys():
                        if f == self.conbo.currentText():
                            cont += 1
                    if cont < 1:
                        self.conbo.addItem(self.conbo.currentText())
                    Usuarios[self.conbo.currentText()]=self.passw.text()
                    pickle_file = open('data.pickle', 'wb')
                    pickle.dump(Usuarios, pickle_file)
                self.passw.setText('')
                self.time = TimeApp(conex=conex)
                """Enviando Tiempo"""
                listime= values['time'].split(':')
                vallist = ['h','m','s']
                num_of_secs = {}
                for t,n in zip(vallist,listime):
                    num_of_secs[t]=int(n)

                self.time.set_num_seg(num_of_secs)
                self.time.show()
                self.hide()
            else:
                error = DialogError(error= values['valerr'])
                error.exec()
                print(values['valerr'])
    """========Definiendo Sombra==========="""
    def colocarSombra(self,shadow):
        self.Sombra = QGraphicsDropShadowEffect(self)
        self.Sombra.setXOffset(5)
        self.Sombra.setYOffset(5)
        self.Sombra.setBlurRadius(10)
        self.Sombra.setColor(QColor(31,31,31,255))
        shadow.setGraphicsEffect(self.Sombra)

    def get_size(self):
        for m in get_monitors():
            if m.is_primary:
                self.resolucion_ancho = m.width
                self.resolucion_alto = m.height


"""====================Error Dialog========================"""
class DialogError(QDialog):
    
    def __init__(self,parent = None ,error=''):
        super(DialogError, self).__init__(parent)
        self.setStyleSheet("DialogError{background-image: url(./images/image.jpg)}")
        self.setWindowIcon(QIcon('./images/internet.png'))
        self.setFixedSize(350,100)
        self.resolucion_ancho = 0
        self.resolucion_alto = 0
        self.get_size()
        left = (self.resolucion_ancho /2) - (self.frameSize().width() / 2)
        top = (self.resolucion_alto /2) - (self.frameSize().height() / 2)
        self.move(int(left), int(top))

        self.setWindowTitle("Error")
        self.message = QLabel('',self)
        self.message.setGeometry(int(350/2)-150,20,300,30)
        self.message.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.message.setStyleSheet('color:#FFFFFF')
        self.message.setText(error)
        self.colocarSombra(self.message)
        
        self.buttonBox = ButtonDialog(self)
        self.buttonBox.setText('Aceptar')
        self.buttonBox.setGeometry(int(350/2)-35,60,70,25)
        self.buttonBox.clicked.connect(self.accept)
        self.buttonBox.setStyleSheet('border-style: solid;border-width: 1px;border-color: rgb(0, 51, 102);background-color: rgb(0, 51, 102);color: rgb(255, 255, 255);border-radius: 5px;')
        self.colocarSombra(self.buttonBox)
    
    def accept(self):
        self.hide()

    def get_size(self):
        for m in get_monitors():
            if m.is_primary:
                self.resolucion_ancho = m.width
                self.resolucion_alto = m.height

    """========Definiendo Sombra==========="""
    def colocarSombra(self,shadow):
        self.Sombra = QGraphicsDropShadowEffect(self)
        self.Sombra.setXOffset(5)
        self.Sombra.setYOffset(5)
        self.Sombra.setBlurRadius(10)
        self.Sombra.setColor(QColor(31,31,31,255))
        shadow.setGraphicsEffect(self.Sombra)

    

"""==============================Definiendo la Clase TIEMPO==================================="""
class TimeApp(QMainWindow):
    
    def __init__(self,parent = None ,conex = None):
        super(TimeApp, self).__init__(parent)

        """Tamano de la Pantalla --setMiniumSize() --setMaximumSize() --setFixedSize()"""
        self.setFixedSize(500,200)
        self.setStyleSheet("TimeApp{background-image: url(./images/image.jpg)}")

        """Definiendo Titulo de la ventana"""
        self.setWindowTitle('Mi Cuenta Nauta')
        self.setWindowIcon(QIcon('./images/internet.png'))

        self.valor = 500
        self.resolucion_ancho = 0
        self.resolucion_alto = 0
        self.get_size()
        self.move(int(self.resolucion_ancho), int(self.resolucion_alto))

        """Variales de el Tiempo"""
        self.cone = conex
        self.num_of_secs = {
            'h':00,
            'm':00,
            's':00
        }
        self.current_time = {
            'h':'00',
            'm':'00',
            's':'00'
        }
        self.s=0
        self.h=0
        self.m=0
        
        """Definiendo Labels"""
        self.labe_text = QLabel(self.cone.username,self)
        self.labe_text.setFont(QFont('FreeSans', 15,QFont.Black))
        self.labe_text.setGeometry(int(500/2)-200,20,400,30)
        self.labe_text.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.labe_text.setStyleSheet('color:#D7EC00')
        self.colocarSombra(self.labe_text)


        self.transcu = QLabel('Tiempo Total:',self)
        self.transcu.setFont(QFont('FreeSans', 15,QFont.Black))
        self.transcu.setGeometry(int(300/2)-125,60,250,30)
        self.transcu.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.transcu.setStyleSheet('color:#D7EC00')
        self.colocarSombra(self.transcu)


        self.restant = QLabel('Tiempo Transcurrido:',self)
        self.restant.setFont(QFont('FreeSans', 15,QFont.Black))
        self.restant.setGeometry(int(300/2)-125,110,250,30)
        self.restant.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.restant.setStyleSheet('color:#D7EC00')
        self.colocarSombra(self.restant)


        self.labe_total = QLabel(str(self.num_of_secs['h'])+':'+str(self.num_of_secs['m'])+':'+str(self.num_of_secs['s']),self)
        self.labe_total.setFont(QFont('Arial', 18,QFont.Black))
        self.labe_total.setGeometry(int(400/2)+75,60,150,30)
        self.labe_total.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.labe_total.setStyleSheet('color:#FFFFFF')
        self.colocarSombra(self.labe_total)

        self.labe_act = QLabel('00:00:00',self)
        self.labe_act.setFont(QFont('Arial', 18,QFont.Bold))
        self.labe_act.setGeometry(int(400/2)+75,110,150,30)
        self.labe_act.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.labe_act.setStyleSheet('color:#FFFFFF')
        self.colocarSombra(self.labe_act)

        self.act = QLabel(self)
        self.act.setPixmap(QPixmap('./images/total.png'))
        self.act.setGeometry(int(400/2)+210,91,50,60)
        self.colocarSombra(self.act)

        self.tot = QLabel(self)
        self.tot.setPixmap(QPixmap('./images/trans.png'))
        self.tot.setGeometry(int(400/2)+210,44,50,60)
        self.colocarSombra(self.tot)

        

        """Boton"""
        self.btn = hoverButton(self)
        self.btn.setText('Cerrar Sesion')
        self.btn.setGeometry(int(500/2)-50,160,100,30)
        self.btn.setStyleSheet('border-style: solid;border-width: 1px;border-color: rgb(0, 51, 102);background-color: rgb(0, 51, 102);color: rgb(255, 255, 255);border-radius: 5px;')
        self.colocarSombra(self.btn)

        self.seguir = hoverLabel(self)
        self.seguir.setPixmap(QPixmap('./images/delante.png'))
        self.seguir.setGeometry(10,2,100,40)
        self.colocarSombra(self.seguir)



        """Disparadores"""
        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.countdown)
        self.timer.start(1000)
        self.btn.clicked.connect(self.logout)
        self.seguir.mousePressEvent = self.minim

    def countdown(self):
        self.s += 1
        if self.s >= 60:
            if self.s > 60:
                self.s = self.s
                -60
                self.m=self.m+1
            else:
                self.s=0
                self.m=self.m+1
            if self.m >= 60:
                self.m=0
                self.h=self.h+1
                if self.h >= 24:
                    self.h=0
            
        min_sec_format = '{:02d}:{:02d}:{:02d}'.format(self.h,self.m, self.s)
        self.current_time['h'] = str(self.h)
        self.current_time['m'] = str(self.m)
        self.current_time['s'] = str(self.s)
        self.labe_act.setText(min_sec_format)
        if self.current_time['h'] == self.num_of_secs['h'] and self.current_time['m'] == self.num_of_secs['m']:
            self.logout()

    def minim(self,event):
        self.window = VerticalApp(ini=self.current_time,conex=self.cone,total=self.num_of_secs)
        self.window.show()
        self.hide()

    def takeTime(self):
        self.h = int(self.current_time['h'])
        self.m = int(self.current_time['m'])
        self.s = int(self.current_time['s'])

    def get_size(self):
        for m in get_monitors():
            if m.is_primary:
                self.resolucion_ancho = m.width
                self.resolucion_alto = m.height

    def logout(self):
        try:
            if self.cone.logout():
                print('Desconectado Correctamente....'+'\n')
                log = MainApp()
                log.show()
                self.hide()
            else:
                print('Error al Desconectar')
                error = DialogError(error= 'Error al Desconectar')
                error.exec()
        except requests.exceptions.Timeout or requests.exceptions.ConnectionError:
            self.s += 10
            error = DialogError(error= 'Error de Conexion con Etecsa')
            error.exec()
            print('Error de Etecsa')

    def set_current(self,current):
        self.current_time = current
        self.takeTime()

    def set_num_seg(self,val):
        self.num_of_secs = val
        if self.num_of_secs['h'] < 10:
            self.num_of_secs['h']= f'0{self.num_of_secs["h"]}'
        if self.num_of_secs['m'] < 10:
            self.num_of_secs['m']= f'0{self.num_of_secs["m"]}'
        if self.num_of_secs['s'] < 10:
            self.num_of_secs['s']= f'0{self.num_of_secs["s"]}'
        self.labe_total.setText(str(self.num_of_secs['h'])+':'+str(self.num_of_secs['m'])+':'+str(self.num_of_secs['s']))

    """========Definiendo Sombra==========="""
    def colocarSombra(self,shadow):
        self.Sombra = QGraphicsDropShadowEffect(self)
        self.Sombra.setXOffset(5)
        self.Sombra.setYOffset(5)
        self.Sombra.setBlurRadius(10)
        self.Sombra.setColor(QColor(31,31,31,255))
        shadow.setGraphicsEffect(self.Sombra)

""""===============================Vista Configuracion==============================="""
class ConfigApp(QMainWindow):
    
    def __init__(self,parent = None ,*args, **kwargs):
        super(ConfigApp, self).__init__(parent)

        """Tamano de la Pantalla --setMiniumSize() --setMaximumSize() --setFixedSize()"""
        self.setFixedSize(500,500)
        self.setStyleSheet("ConfigApp{background-image: url(./images/image.jpg)}")

        """Definiendo Titulo de la ventana"""
        self.setWindowTitle('Mi Cuenta Nauta')
        self.setWindowIcon(QIcon('./images/internet.png'))
        
        
        self.resolucion_ancho = 0
        self.resolucion_alto = 0
        self.get_size()
        left = (self.resolucion_ancho /2) - (self.frameSize().width() / 2)
        top = (self.resolucion_alto /2) - (self.frameSize().height() / 2)
        self.move(int(left), int(top))

        """Label"""
        self.labe_user = QLabel('USUARIOS REGISTRADOS\n-------------------------------------------------------------------------------------------------',self)
        self.labe_user.setGeometry(int(500/2)-250,20,500,30)
        self.labe_user.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.labe_user.setStyleSheet('color:#FFFFFF')
        


        # self.widget = QTabWidget(self)
        # self.widget.setGeometry(0,0,350,500)
        # self.widget.move(150,0)
        

    def get_size(self):
        for m in get_monitors():
            if m.is_primary:
                self.resolucion_ancho = m.width
                self.resolucion_alto = m.height


"""========================Definiendo APP Vertical==============================="""    
class VerticalApp(QMainWindow):
    
    def __init__(self,parent = None,ini={},total={},conex = None):
        super(VerticalApp, self).__init__(parent)

        """Tamano de la Pantalla --setMiniumSize() --setMaximumSize() --setFixedSize()"""
        self.setFixedSize(60,200)
        self.setStyleSheet("VerticalApp{background-image: url(./images/image.jpg)}")

        """Definiendo Titulo de la ventana"""
        self.setWindowIcon(QIcon('./images/internet.png'))
        self.valor = 500
        self.resolucion_ancho = 0
        self.resolucion_alto = 0
        self.get_size()
        self.move(int(self.resolucion_ancho), int(self.resolucion_alto))

        self.conex = conex 

        self.total = total
        self.current_time = ini
        self.h = 0
        self.m = 0
        self.s = 0

        self.takeTime()

        self.label = VerticalLabel('00:00:00',self)
        self.label.setFont(QFont('Arial', 20,QFont.Black))
        self.label.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.label.setStyleSheet('color:#FFFFFF')
        self.label.setGeometry(0,0,60,220)
        self.colocarSombra(self.label)

        self.icon = QLabel('',self)
        self.icon.setPixmap(QPixmap('./images/transv.png'))
        self.icon.setGeometry(20,158,60,50)
        self.colocarSombra(self.icon)

        self.btn = hoverLabel(self)
        self.btn.setPixmap(QPixmap('./images/Atras.png'))
        self.btn.setGeometry(15,4,55,35)
        self.colocarSombra(self.btn)
        

        """Disparadores"""
        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.countdown)
        self.timer.start(1000)
        self.btn.mousePressEvent = self.back
        
    def back(self,event):
        self.time = TimeApp(conex=self.conex)
        self.time.set_current(self.current_time)

        self.total['h'] = int(self.total['h'])
        self.total['m'] = int(self.total['m'])
        self.total['s'] = int(self.total['s'])

        self.time.set_num_seg(self.total)
        self.time.show()
        self.hide()

    def get_size(self):
        for m in get_monitors():
            if m.is_primary:
                self.resolucion_ancho = m.width
                self.resolucion_alto = m.height

    def takeTime(self):
        self.h = int(self.current_time['h'])
        self.m = int(self.current_time['m'])
        self.s = int(self.current_time['s'])
    
    def logout(self):
        try:
            if self.conex.logout():
                print('Desconectado Correctamente....'+'\n')
                log = MainApp()
                log.show()
                self.hide()
            else:
                print('Error al Desconectar')
                error = DialogError(error= 'Error al Desconectar')
        except requests.exceptions.Timeout or requests.exceptions.ConnectionError:
            self.s += 10
            error = DialogError(error= 'Error de Conexion con Etecsa')
            error.exec()
            print('Error de Etecsa')

    def countdown(self):
        self.s += 1
        if self.s >= 60:
            self.s=0
            self.m=self.m+1
            if self.m >= 60:
                self.m=0
                self.h=self.h+1
                if self.h >= 24:
                    self.h=0
        min_sec_format = '{:02d}:{:02d}:{:02d}'.format(self.h,self.m, self.s)
        self.current_time['h'] = str(self.h)
        self.current_time['m'] = str(self.m)
        self.current_time['s'] = str(self.s)
        self.label.setText(min_sec_format)  
        if self.current_time['h'] == int(self.total['h']) and self.current_time['m'] == int(self.total['m']):
            self.logout()

    """========Definiendo Sombra==========="""
    def colocarSombra(self,shadow):
        self.Sombra = QGraphicsDropShadowEffect(self)
        self.Sombra.setXOffset(5)
        self.Sombra.setYOffset(5)
        self.Sombra.setBlurRadius(10)
        self.Sombra.setColor(QColor(31,31,31,255))
        shadow.setGraphicsEffect(self.Sombra)

    


if __name__ == '__main__':
    """Iniciando Aplicacion"""
    app = QApplication(['Mi Cuenta Nauta'])

    """Creando y Mostrando la Ventana"""
    window = MainApp()
    window.show()
    app.exec_()