"""Servicio de autenticación SIMULADO, en memoria.

No es un sistema de producción: los usuarios se pierden al cerrar la app,
no hay límite de intentos, ni sesiones, ni base de datos.
Lo que sí hace bien desde ahora: nunca guarda la contraseña, solo su hash con sal.
"""

import hashlib
import hmac
import os

LONGITUD_MINIMA_PASSWORD = 8
ITERACIONES = 600_000


class ServicioAutenticacion:
    """Gestiona el registro y la verificación de usuarios en memoria."""

    def __init__(self):
        # "ana@correo.com" -> {"nombre": ..., "apellido": ..., "sal": ..., "hash": ...}
        self._usuarios = {}

    def registrar(self, nombre, apellido, usuario, password):
        nombre_limpio = nombre.strip()
        apellido_limpio = apellido.strip()
        clave = usuario.strip().lower()
        minimo = LONGITUD_MINIMA_PASSWORD

        if not nombre_limpio:
            raise ValueError("Completá tu nombre.")
        if not apellido_limpio:
            raise ValueError("Completá tu apellido.")
        if not clave:
            raise ValueError("Completá tu usuario o correo electrónico.")
        if len(password) < minimo:
            raise ValueError(f"La contraseña necesita al menos {minimo} caracteres.")
        if clave in self._usuarios:
            raise ValueError("Ese usuario ya está registrado.")

        sal = os.urandom(16)
        self._usuarios[clave] = {
            "nombre": nombre_limpio,
            "apellido": apellido_limpio,
            "sal": sal,
            "hash": self._calcular_hash(password, sal),
        }

    def autenticar(self, usuario, password):
        clave = usuario.strip().lower()
        datos_usuario = self._usuarios.get(clave)
        if not datos_usuario or not password:
            return False

        hash_intento = self._calcular_hash(password, datos_usuario["sal"])
        return hmac.compare_digest(hash_intento, datos_usuario["hash"])

    @staticmethod
    def evaluar_fortaleza(password):
        """Calcula el nivel de fortaleza de una contraseña (Desafío Nivel 3)."""
        if not password:
            return "vacia", ""

        puntaje = 0
        if len(password) >= LONGITUD_MINIMA_PASSWORD:
            puntaje += 1
        if len(password) >= 12:
            puntaje += 1
        if any(c.isdigit() for c in password):
            puntaje += 1
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            puntaje += 1
        if any(not c.isalnum() for c in password):
            puntaje += 1

        if len(password) < LONGITUD_MINIMA_PASSWORD or puntaje <= 2:
            return "debil", "Fortaleza de la contraseña: Débil"
        if puntaje <= 3:
            return "aceptable", "Fortaleza de la contraseña: Aceptable"
        return "fuerte", "Fortaleza de la contraseña: Fuerte"

    @staticmethod
    def _calcular_hash(password, sal):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), sal, ITERACIONES
        )