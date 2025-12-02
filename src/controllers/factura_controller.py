# src/controllers/factura_controller.py
from src.models.factura_model import FacturaModel

class FacturaController:
    def __init__(self):
        self.model = FacturaModel()

    def crear_factura(self, carrito):
        total = sum(item["cantidad"] * item["precio"] for item in carrito)
        factura_id = self.model.crear_factura(total)

        for item in carrito:
            self.model.agregar_detalle(
                factura_id,
                item["producto"],
                item["cantidad"],
                item["precio"]
            )

        return factura_id

    def listar_facturas(self):
        return self.model.obtener_facturas()

    def detalle_factura(self, factura_id):
        return self.model.obtener_detalle(factura_id)

    # ============================================================
    # 🔥 NUEVO — ELIMINAR FACTURA
    # ============================================================
    def eliminar_factura(self, factura_id):
        return self.model.eliminar_factura(factura_id)

    def buscar_facturas(self, termino):
        return self.model.buscar_facturas(termino)
