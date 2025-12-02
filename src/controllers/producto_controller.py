# src/controllers/producto_controller.py
from src.models.conexion import Conexion
from src.models.producto import Producto
from mysql.connector import Error

class ProductoController:
    def __init__(self):
        self.db = Conexion()

    def agregar_producto(self, producto: Producto):
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO inventario (nombre, proveedor, precio, costo, stock)
                VALUES (%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, producto.to_tuple())
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.cerrar()

    def editar_producto(self, producto: Producto):
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            sql = """
                UPDATE inventario 
                SET proveedor=%s, precio=%s, costo=%s, stock=%s 
                WHERE nombre=%s
            """
            cursor.execute(sql, (
                producto.proveedor,
                producto.precio,
                producto.costo,
                producto.stock,
                producto.nombre
            ))
            conn.commit()
            return cursor.rowcount
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.cerrar()

    def eliminar_producto(self, nombre):
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventario WHERE nombre=%s", (nombre,))
            conn.commit()
            return cursor.rowcount
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.cerrar()

    def listar_todos(self):
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, proveedor, precio, costo, stock FROM inventario")
            filas = cursor.fetchall()

            productos = []
            for f in filas:
                p = Producto(
                    id=f[0],
                    nombre=f[1],
                    proveedor=f[2],
                    precio=f[3],
                    costo=f[4],
                    stock=f[5]
                )
                productos.append(p)

            return productos
        finally:
            cursor.close()
            self.db.cerrar()

    def obtener_por_nombre(self, nombre):
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, proveedor, precio, costo, stock 
                FROM inventario 
                WHERE nombre=%s
            """, (nombre,))
            fila = cursor.fetchone()

            if fila:
                return Producto(
                    id=fila[0],
                    nombre=fila[1],
                    proveedor=fila[2],
                    precio=fila[3],
                    costo=fila[4],
                    stock=fila[5]
                )
            return None
        finally:
            cursor.close()
            self.db.cerrar()
    
    def buscar_producto(self, termino):
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            sql = """
                SELECT id, nombre, proveedor, precio, costo, stock
                FROM inventario
                WHERE nombre LIKE %s OR proveedor LIKE %s
            """
            criterio = f"%{termino}%"
            cursor.execute(sql, (criterio, criterio))
            filas = cursor.fetchall()

            resultados = []
            for f in filas:
                p = Producto(
                    id=f[0],
                    nombre=f[1],
                    proveedor=f[2],
                    precio=f[3],
                    costo=f[4],
                    stock=f[5]
                )
                resultados.append(p)

            return resultados
        finally:
            cursor.close()
            self.db.cerrar()
