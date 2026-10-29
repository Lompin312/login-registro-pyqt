from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QLineEdit, QWidget

RUTA_UI = Path(__file__).parent / "login.ui"


class VentanaLogin(QWidget):
    """Controla la pantalla de inicio de sesión. El diseño vive en login.ui."""

    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        self._preferencias = QSettings("UTN-TUP", "LoginRegistroPyQt")
        uic.loadUi(RUTA_UI, self)
        self._conectar_eventos()
        self._cargar_usuario_recordado()

    def _conectar_eventos(self):
        self.btn_login.clicked.connect(self.iniciar_sesion)
        self.input_password.returnPressed.connect(self.iniciar_sesion)
        self.chk_mostrar_password.toggled.connect(self.alternar_password)

    def _cargar_usuario_recordado(self):
        usuario_guardado = self._preferencias.value("usuario_recordado", "", type=str)
        if usuario_guardado:
            self.input_usuario.setText(usuario_guardado)
            self.chk_recordar_usuario.setChecked(True)

    def _actualizar_usuario_recordado(self, usuario):
        if self.chk_recordar_usuario.isChecked():
            self._preferencias.setValue("usuario_recordado", usuario)
        else:
            self._preferencias.remove("usuario_recordado")

    def alternar_password(self, visible):
        if visible:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

    def iniciar_sesion(self):
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text()

        error = self._validar(usuario, password)
        if error:
            self._mostrar_mensaje(error, "error")
            return

        if self.servicio.autenticar(usuario, password):
            self._actualizar_usuario_recordado(usuario)
            self._mostrar_mensaje(
                f"Sesión iniciada como {usuario} (simulación).", "exito"
            )
        else:
            self._mostrar_mensaje("Usuario o contraseña incorrectos.", "error")

    def _validar(self, usuario, password):
        self._marcar_campo_invalido(self.input_usuario, not bool(usuario))
        self._marcar_campo_invalido(self.input_password, bool(usuario) and not bool(password))

        if not usuario:
            return "Ingresá tu usuario o correo electrónico."
        if not password:
            return "Ingresá tu contraseña."
        return None

    def _marcar_campo_invalido(self, campo, es_invalido):
        campo.setProperty("invalido", "true" if es_invalido else "false")
        campo.style().unpolish(campo)
        campo.style().polish(campo)

    def _mostrar_mensaje(self, texto, tipo="info"):
        self.label_mensaje.setText(texto)
        self.label_mensaje.setProperty("tipo", tipo)
        self.label_mensaje.style().unpolish(self.label_mensaje)
        self.label_mensaje.style().polish(self.label_mensaje)

    def preparar_pantalla(self):
        """Limpia mensajes y estados al cambiar de pantalla y ubica el foco."""
        self.input_password.clear()
        self._marcar_campo_invalido(self.input_usuario, False)
        self._marcar_campo_invalido(self.input_password, False)
        self._mostrar_mensaje("", "info")
        if self.input_usuario.text().strip():
            self.input_password.setFocus()
        else:
            self.input_usuario.setFocus()