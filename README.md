# Login y registro con PyQt6

Aplicación de escritorio con dos pantallas diseñadas en Qt Designer y controladas con clases de Python. Trabajo práctico de Programación Orientada a Objetos (Tecnicatura Universitaria en Programación - UTN).

> **Importante:** la autenticación es una **SIMULACIÓN**. Los usuarios viven en memoria y se pierden al cerrar la aplicación. No limita intentos de inicio de sesión, no gestiona sesiones persistentes y no es un sistema seguro ni apto para datos reales en producción.

## Capturas

### Pantallas principales
| Inicio de sesión (`login.ui`) | Creación de cuenta (`registro.ui`) |
| :---: | :---: |
| ![Login](capturas/login.png) | ![Registro](capturas/registro.png) |

### Validación de errores y comparación Antes / Después de QSS
| Validación de campo obligatorio | Antes de `estilos.qss` | Después de `estilos.qss` |
| :---: | :---: | :---: |
| ![Error en Login](capturas/login_error.png) | ![Antes de estilos](capturas/antes_estilos.png) | ![Después de estilos](capturas/despues_estilos.png) |

## Requisitos

* Python 3.10 o más nuevo.
* Librería `PyQt6` (especificada en `requirements.txt`).

## Instalación y Ejecución

    py -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python main.py

## Funcionalidades

- [x] Login y registro diseñados en Qt Designer (`ventanas/login.ui` y `ventanas/registro.ui`) con layouts y nombres de la convención.
- [x] Carga dinámica desde `.ui` mediante `uic.loadUi(RUTA_UI, self)` y rutas con `Path(__file__).parent`.
- [x] Una clase propia por pantalla (`VentanaLogin` y `VentanaRegistro`) y contenedor `VentanaPrincipal(QStackedWidget)`.
- [x] Mostrar u ocultar contraseñas (`toggled`) y envío con `Enter` (`returnPressed`).
- [x] Validación completa con cláusulas de guarda y mensajes honestos.
- [x] Servicio compartido `ServicioAutenticacion` con hash PBKDF2-HMAC-SHA256 (600.000 iteraciones) y sal aleatoria (`os.urandom(16)`).
- [x] Mejoras visuales en `ventanas/estilos.qss` con propiedades dinámicas (`tipo` e `invalido`).
- [x] Desafíos Nivel 3: **Recordar mi usuario (`QSettings`)** y **Medidor de fortaleza de contraseña en tiempo real (`textChanged`)**.

## Decisiones de diseño

| # | Mejora implementada | Por qué la elegimos | Dónde se aplicó | Capturas |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Paleta de colores y jerarquía tipográfica** | Diferencia fondo, tarjeta, títulos y acción principal, previniendo conflictos con el modo oscuro del sistema. | `ventanas/estilos.qss` | `capturas/antes_estilos.png` y `capturas/despues_estilos.png` |
| **2** | **Estados interactivos (`:hover`, `:pressed`, `:focus`, `:disabled`)** | Retroalimentación visual inmediata al navegar con mouse o `Tab`. | `ventanas/estilos.qss` | `capturas/login.png` |
| **3** | **Mensajes de error y éxito con propiedades dinámicas** | Python define el estado (`error` / `exito`) y QSS decide el color, manteniendo textos claros. | `estilos.qss`, `ventana_login.py`, `ventana_registro.py` | `capturas/login_error.png` y `capturas/registro_exito.png` |
| **4** | **Resaltado de campos inválidos (`[invalido="true"]`)** | Marca en rojo suave el campo puntual que debe corregirse. | `estilos.qss`, `ventana_login.py`, `ventana_registro.py` | `capturas/login_error.png` |

## Limitaciones conocidas

* **Sin persistencia de cuentas:** Los usuarios viven en un diccionario en memoria (`self._usuarios`) y se borran al cerrar la aplicación.
* **Sin límite de intentos ni sesiones reales:** Es una simulación académica preparatoria para la integración con MySQL.

## Autores

* **Emanuel Olmos (`Lompin312`)** — Tecnicatura Universitaria en Programación (UTN)
* **Repositorio:** https://github.com/Lompin312/login-registro-pyqt
