import tkinter as tk
from src.views.inventario_view import InventarioView
from src.views.ventas_view import VentasView
from src.views.factura_view import FacturaView

from src.controllers.producto_controller import ProductoController
from src.controllers.ventas_controller import VentasController
from src.controllers.factura_controller import FacturaController

# ==============================
# FUNCIÓN PARA CENTRAR VENTANA
# ==============================
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


class Contenedor(tk.Tk):
    def __init__(self, login_controller=None):
        super().__init__()
        self.login_controller = login_controller
        self.rol_usuario = None
        self.usuario_actual = None

        if login_controller:
            self.rol_usuario = login_controller.rol_actual
            self.usuario_actual = login_controller.usuario_actual

        self.title("Gestión Ventas - POO")
        ancho, alto = 1000, 715
        centrar_ventana(self, ancho, alto)
        self.resizable(False, False)
        self.config(bg="#AFDBC7")

        # Frames principales
        self.menu_frame = tk.Frame(self, bg="#AFDBC7")
        self.menu_frame.pack(side="top", fill="x")

        self.content_frame = tk.Frame(self, bg="#F5F5F5")
        self.content_frame.pack(fill="both", expand=True)

        # Controladores
        self.producto_ctrl = ProductoController()
        self.ventas_ctrl = VentasController()
        self.factura_ctrl = FacturaController()

        # Diccionario de frames
        self.frames = {}

        # Construir menú y vistas
        self._build_menu()
        self._build_frames()

        # Mostrar mensaje de bienvenida
        if self.usuario_actual:
            tk.Label(
                self.menu_frame,
                text=f"Bienvenido {self.usuario_actual} ({self.rol_usuario})",
                font=("Arial", 12),
                bg="#AFDBC7"
            ).pack(side="right", padx=10)

        # Vista inicial según rol
        if self.rol_usuario == "admin":
            self.show_frame("Inventario")
        else:
            self.show_frame("Ventas")

    # ==========================
    # Construir menú
    # ==========================
    def _build_menu(self):
        if self.rol_usuario == "admin":
            tk.Button(self.menu_frame, text="Inventario",
                      command=lambda: self.show_frame("Inventario")).pack(side="left", padx=8, pady=6)
            tk.Button(self.menu_frame, text="Ventas",
                      command=lambda: self.show_frame("Ventas")).pack(side="left", padx=8, pady=6)
            tk.Button(self.menu_frame, text="Facturas",
                      command=lambda: self.show_frame("Facturas")).pack(side="left", padx=8, pady=6)
        else:  # Vendedores, root, etc.
            tk.Button(self.menu_frame, text="Ventas",
                      command=lambda: self.show_frame("Ventas")).pack(side="left", padx=8, pady=6)
            tk.Button(self.menu_frame, text="Facturas",
                      command=lambda: self.show_frame("Facturas")).pack(side="left", padx=8, pady=6)

    # ==========================
    # Construir frames
    # ==========================
    def _build_frames(self):
        self.frames["Inventario"] = InventarioView(self.content_frame, self.producto_ctrl)
        self.frames["Ventas"] = VentasView(self.content_frame, self.producto_ctrl, self.factura_ctrl)
        self.frames["Facturas"] = FacturaView(self.content_frame, self.factura_ctrl, self.rol_usuario)

        for frame in self.frames.values():
            frame.pack_forget()

    # ==========================
    # Mostrar frame por nombre
    # ==========================
    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames.get(name)
        if frame:
            if hasattr(frame, "actualizar"):
                frame.actualizar()
            elif hasattr(frame, "refrescar"):
                frame.refrescar()
            frame.pack(fill="both", expand=True)


# ==========================
# TEST rápido
# ==========================
if __name__ == "__main__":
    from src.controllers.login_controller import LoginController

    controller = LoginController()
    controller.usuario_actual = "admin"
    controller.rol_actual = "admin"

    app = Contenedor(controller)
    app.mainloop()
