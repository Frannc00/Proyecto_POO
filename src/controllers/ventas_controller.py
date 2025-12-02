# src/controllers/ventas_controller.py
from src.models.conexion import Conexion
from src.models.venta import Venta
from mysql.connector import Error

class VentasController:
    def __init__(self):
        self.db = Conexion()

    def next_factura(self):
        conn = self.db.conectar()
        try:
            cur = conn.cursor()
            cur.execute("SELECT MAX(factura) FROM ventas")
            r = cur.fetchone()[0]
            return int(r) + 1 if r else 1
        finally:
            cur.close()
            self.db.cerrar()

    def registrar_venta(self, venta: Venta):
        conn = self.db.conectar()
        try:
            cur = conn.cursor()
            sql = """INSERT INTO ventas 
                (factura, nombre_articulo, valor_articulo, cantidad, subtotal) 
                VALUES (%s,%s,%s,%s,%s)"""
            cur.execute(sql, venta.to_tuple())
            conn.commit()
            return cur.lastrowid
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            self.db.cerrar()

    def listar_ventas(self):
        conn = self.db.conectar()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, factura, nombre_articulo, valor_articulo, cantidad, subtotal, fecha 
                FROM ventas 
                ORDER BY fecha DESC
            """)
            return cur.fetchall()
        finally:
            cur.close()
            self.db.cerrar()
