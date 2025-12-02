# src/models/producto.py
from src.models.item import Item

class Producto(Item):
    def __init__(self, nombre, proveedor="", precio=0.0, costo=0.0, stock=0, id=None):
        super().__init__(nombre)
        self._proveedor = proveedor
        self._precio = float(precio)
        self._costo = float(costo)
        self._stock = int(stock)
        self._id = id

    # === getters / setters ===

    @property
    def id(self):
        return self._id

    @property
    def proveedor(self):
        return self._proveedor

    @proveedor.setter
    def proveedor(self, value):
        self._proveedor = value

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, value):
        self._precio = float(value)

    @property
    def costo(self):
        return self._costo

    @costo.setter
    def costo(self, value):
        self._costo = float(value)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = int(value)

    def to_tuple(self):
        return (self.nombre, self.proveedor, self.precio, self.costo, self.stock)

    def __repr__(self):
        return f"Producto(id={self._id}, nombre={self.nombre}, precio={self.precio}, stock={self.stock})"
