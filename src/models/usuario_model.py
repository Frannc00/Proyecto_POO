from src.models.conexion import Conexion

class UsuarioModel:
    def __init__(self):
        self.conexion = Conexion()

    # =========================================================
    # VALIDAR LOGIN
    # =========================================================
    def validar(self, usuario, contraseña):
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT usuario, rol FROM usuarios WHERE usuario=%s AND contraseña=%s",
                (usuario, contraseña)
            )
            result = cur.fetchone()  # Devuelve None o (usuario, rol)
            return result
        finally:
            cur.close()
            self.conexion.cerrar()

    # =========================================================
    # CREAR USUARIO
    # =========================================================
    def crear_usuario(self, usuario, contraseña, rol, codigo_secreto=None):
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()

            # Si el rol es "admin", validamos el código secreto
            if rol == "admin" and codigo_secreto != "tu_codigo_secreto":  # Cambiar por tu código real
                return False  # Código incorrecto para crear un admin

            # Insertar usuario sin comprobar existencia
            cur.execute(
                "INSERT INTO usuarios (usuario, contraseña, rol) VALUES (%s, %s, %s)",
                (usuario, contraseña, rol)
            )
            conn.commit()
            return True

        except Exception as e:
            print(f"Error al crear el usuario: {e}")
            return False
        finally:
            cur.close()
            self.conexion.cerrar()
