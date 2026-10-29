import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from ventanas.ventana_principal import VentanaPrincipal

RUTA_ESTILOS = Path(__file__).parent / "ventanas" / "estilos.qss"


def cargar_estilos(app):
    try:
        app.setStyleSheet(RUTA_ESTILOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Aviso: no encontré {RUTA_ESTILOS}. Sigo con el estilo por defecto.")


def main():
    app = QApplication(sys.argv)
    cargar_estilos(app)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()