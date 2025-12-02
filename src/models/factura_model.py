# src/models/factura_model.py
from src.models.conexion import Conexion

class FacturaModel:
    def __init__(self):
        self.conexion = Conexion()

    def crear_factura(self, total):
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO facturas (fecha, total) VALUES (NOW(), %s)",
                (total,)
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            self.conexion.cerrar()

    def agregar_detalle(self, factura_id, producto, cantidad, precio):
        subtotal = cantidad * precio
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO factura_detalle 
                (factura_id, producto, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (factura_id, producto, cantidad, precio, subtotal))
            conn.commit()
        finally:
            cur.close()
            self.conexion.cerrar()

    def obtener_facturas(self):
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, fecha, total FROM facturas ORDER BY id DESC")
            return cur.fetchall()
        finally:
            cur.close()
            self.conexion.cerrar()

    def buscar_facturas(self, termino):
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()

            # Buscar por ID, fecha o total (coincidencia parcial)
            query = """
                SELECT id, fecha, total
                FROM facturas
                WHERE id LIKE %s
                OR fecha LIKE %s
                OR total LIKE %s
                ORDER BY id DESC
            """

            like = f"%{termino}%"
            cur.execute(query, (like, like, like))
            return cur.fetchall()

        finally:
            cur.close()
            self.conexion.cerrar()


    def obtener_detalle(self, factura_id):
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, factura_id, producto, cantidad, precio_unitario, subtotal
                FROM factura_detalle
                WHERE factura_id = %s
            """, (factura_id,))
            return cur.fetchall()
        finally:
            cur.close()
            self.conexion.cerrar()

    # ====================================================
    # 🔥 NUEVO: ELIMINAR FACTURA + DETALLES
    # ====================================================
    def eliminar_factura(self, factura_id):
        conn = self.conexion.conectar()
        try:
            cur = conn.cursor()

            # Primero se borran los detalles
            cur.execute("DELETE FROM factura_detalle WHERE factura_id = %s", (factura_id,))

            # Luego se borra la factura
            cur.execute("DELETE FROM facturas WHERE id = %s", (factura_id,))

            conn.commit()
        finally:
            cur.close()
            self.conexion.cerrar()
