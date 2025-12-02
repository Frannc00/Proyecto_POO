# src/models/venta.py
class Venta:
    def __init__(self, factura, nombre_articulo, valor_articulo, cantidad, subtotal, id=None):
        self.id = id
        self.factura = factura
        self.nombre_articulo = nombre_articulo
        self.valor_articulo = float(valor_articulo)
        self.cantidad = int(cantidad)
        self.subtotal = float(subtotal)

    def to_tuple(self):
        return (self.factura, self.nombre_articulo, self.valor_articulo, self.cantidad, self.subtotal)
