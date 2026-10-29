from PyQt6.QtWidgets import QStackedWidget
from controladores.autenticacion import ServicioAutenticacion
from ventanas.ventana_login import VentanaLogin
from ventanas.ventana_registro import VentanaRegistro


class VentanaPrincipal(QStackedWidget):
    """La ventana de la aplicación: muestra una pantalla por vez."""

    def __init__(self):
        super().__init__()
        servicio = ServicioAutenticacion()
        self.login = VentanaLogin(servicio)
        self.registro = VentanaRegistro(servicio)

        self.addWidget(self.login)
        self.addWidget(self.registro)

        self.login.btn_ir_registro.clicked.connect(self.mostrar_registro)
        self.registro.btn_volver_login.clicked.connect(self.mostrar_login)

        self.resize(640, 620)
        self.mostrar_login()

    def mostrar_login(self):
        self.setCurrentWidget(self.login)
        self.setWindowTitle("Iniciar sesión")
        self.login.preparar_pantalla()

    def mostrar_registro(self):
        self.setCurrentWidget(self.registro)
        self.setWindowTitle("Crear cuenta")
        self.registro.preparar_pantalla()