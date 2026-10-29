from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QLineEdit, QWidget
from controladores.autenticacion import LONGITUD_MINIMA_PASSWORD

RUTA_UI = Path(__file__).parent / "registro.ui"


class VentanaRegistro(QWidget):
    """Controla la pantalla de creación de cuenta. El diseño vive en registro.ui."""

    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        uic.loadUi(RUTA_UI, self)
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.btn_registrar.clicked.connect(self.registrar)
        self.chk_mostrar_password.toggled.connect(self.alternar_password)
        self.input_password.textChanged.connect(self.actualizar_fortaleza)

    def alternar_password(self, visible):
        modo = QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password
        self.input_password.setEchoMode(modo)
        self.input_confirmar_password.setEchoMode(modo)

    def actualizar_fortaleza(self, texto):
        nivel, descripcion = self.servicio.evaluar_fortaleza(texto)
        self.label_fortaleza.setText(descripcion)
        self.label_fortaleza.setProperty("nivel", nivel)
        self.label_fortaleza.style().unpolish(self.label_fortaleza)
        self.label_fortaleza.style().polish(self.label_fortaleza)

    def registrar(self):
        datos = self._leer_formulario()
        error = self._validar(datos)
        if error:
            self._mostrar_mensaje(error, "error")
            return

        try:
            self.servicio.registrar(
                datos["nombre"],
                datos["apellido"],
                datos["usuario"],
                datos["password"],
            )
        except ValueError as error_servicio:
            self._mostrar_mensaje(str(error_servicio), "error")
            return

        self._mostrar_mensaje(
            "Cuenta creada. Ya podés volver e iniciar sesión.", "exito"
        )

    def _leer_formulario(self):
        return {
            "nombre": self.input_nombre.text().strip(),
            "apellido": self.input_apellido.text().strip(),
            "usuario": self.input_usuario.text().strip(),
            "password": self.input_password.text(),
            "confirmacion": self.input_confirmar_password.text(),
        }

    def _validar(self, datos):
        self._limpiar_bordes_invalidos()

        if not datos["nombre"]:
            self._marcar_campo_invalido(self.input_nombre, True)
            return "Completá tu nombre."
        if not datos["apellido"]:
            self._marcar_campo_invalido(self.input_apellido, True)
            return "Completá tu apellido."
        if not datos["usuario"]:
            self._marcar_campo_invalido(self.input_usuario, True)
            return "Completá tu usuario o correo electrónico."
        if len(datos["password"]) < LONGITUD_MINIMA_PASSWORD:
            self._marcar_campo_invalido(self.input_password, True)
            return f"La contraseña necesita al menos {LONGITUD_MINIMA_PASSWORD} caracteres."
        if datos["password"] != datos["confirmacion"]:
            self._marcar_campo_invalido(self.input_confirmar_password, True)
            return "Las contraseñas no coinciden."
        return None

    def _marcar_campo_invalido(self, campo, es_invalido):
        campo.setProperty("invalido", "true" if es_invalido else "false")
        campo.style().unpolish(campo)
        campo.style().polish(campo)

    def _limpiar_bordes_invalidos(self):
        for campo in (
            self.input_nombre,
            self.input_apellido,
            self.input_usuario,
            self.input_password,
            self.input_confirmar_password,
        ):
            self._marcar_campo_invalido(campo, False)

    def _mostrar_mensaje(self, texto, tipo="info"):
        self.label_mensaje.setText(texto)
        self.label_mensaje.setProperty("tipo", tipo)
        self.label_mensaje.style().unpolish(self.label_mensaje)
        self.label_mensaje.style().polish(self.label_mensaje)

    def preparar_pantalla(self):
        """Limpia mensajes y bordes al abrir la pantalla y da foco al primer campo."""
        self._limpiar_bordes_invalidos()
        self._mostrar_mensaje("", "info")
        self.input_nombre.setFocus()