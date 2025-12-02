# src/views/inventario_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.producto_controller import ProductoController
from src.models.producto import Producto
from src.utils.validador import es_numero, es_entero

class InventarioView(tk.Frame):
    def __init__(self, parent, controller: ProductoController):
        super().__init__(parent, bg="#F5F5F5")
        self.controller = controller
        self._build()

    def _build(self):
        # Título
        tk.Label(self, text="Inventario", font="sans 24 bold", bg="#b3afaf").pack(fill="x")

        main = tk.Frame(self, bg="#AFDBC7")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Panel Izquierdo ---
        left = tk.LabelFrame(main, text="Productos", font="sans 14 bold", bg="#AFDBC7")
        left.pack(side="left", fill="y", padx=10, pady=10)

        def add_entry(label, row):
            tk.Label(left, text=label, bg="#AFDBC7").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            e = ttk.Entry(left)
            e.grid(row=row, column=1, padx=8, pady=5)
            return e

        self.nombre = add_entry("Nombre:", 0)
        self.proveedor = add_entry("Proveedor:", 1)
        self.precio = add_entry("Precio:", 2)
        self.costo = add_entry("Costo:", 3)

        # Botones
        tk.Button(left, text="Ingresar", command=self.ingresar_producto)\
            .grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        tk.Button(left, text="Editar", command=self.editar_producto)\
            .grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

        tk.Button(left, text="Modificar Stock", command=self.modificar_stock)\
            .grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Panel Derecho ---
        right = tk.Frame(main, bg="#AFDBC7")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        search_frame = tk.Frame(right, bg="#AFDBC7")
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="Buscar:", bg="#AFDBC7").pack(side="left", padx=5)
        self.busqueda = ttk.Entry(search_frame)
        self.busqueda.pack(side="left", padx=5)

        tk.Button(search_frame, text="Buscar", command=self.buscar_producto).pack(side="left", padx=5)
        tk.Button(search_frame, text="Mostrar Todo", command=self.refrescar).pack(side="left", padx=5)

        # ========== TABLA ARREGLADA ==========
        self.tre = ttk.Treeview(
            right,
            columns=("ID", "Producto", "Proveedor", "Precio", "Costo", "Stock"),
            show="headings"
        )

        # Encabezados
        self.tre.heading("ID", text="ID")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Proveedor", text="Proveedor")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Costo", text="Costo")
        self.tre.heading("Stock", text="Stock")

        # Alineación + ancho
        self.tre.column("ID", anchor="center", width=50)
        self.tre.column("Producto", anchor="center", width=150)
        self.tre.column("Proveedor", anchor="center", width=120)
        self.tre.column("Precio", anchor="center", width=80)
        self.tre.column("Costo", anchor="center", width=80)
        self.tre.column("Stock", anchor="center", width=80)

        self.tre.pack(fill="both", expand=True, pady=10)
        self.tre.bind("<<TreeviewSelect>>", self.on_select)

        self.refrescar()

    # ================= Métodos =================

    def refrescar(self):
        for r in self.tre.get_children():
            self.tre.delete(r)
        for p in self.controller.listar_todos():
            self.tre.insert("", "end",
                values=(p.id, p.nombre, p.proveedor, p.precio, p.costo, p.stock)
            )

    def buscar_producto(self):
        termino = self.busqueda.get().strip()
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese texto para buscar")
            return

        for r in self.tre.get_children():
            self.tre.delete(r)

        for p in self.controller.buscar_producto(termino):
            self.tre.insert("", "end",
                values=(p.id, p.nombre, p.proveedor, p.precio, p.costo, p.stock)
            )

    def ingresar_producto(self):
        nombre = self.nombre.get().strip()
        proveedor = self.proveedor.get().strip()
        precio = self.precio.get().strip()
        costo = self.costo.get().strip()

        if not (nombre and precio):
            messagebox.showwarning("Advertencia", "Nombre y precio son requeridos")
            return
        if not es_numero(precio) or (costo and not es_numero(costo)):
            messagebox.showwarning("Advertencia", "Valores numéricos inválidos")
            return

        # Crear producto con stock = 0 momentáneo
        p = Producto(
            nombre=nombre,
            proveedor=proveedor,
            precio=float(precio),
            costo=float(costo or 0),
            stock=0
        )

        try:
            self.controller.agregar_producto(p)
            self.refrescar()
            self.limpiar()
            self.popup_stock_inicial(p.nombre)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    # =================== STOCK INICIAL ===================
    def popup_stock_inicial(self, nombre):
        producto = self.controller.obtener_por_nombre(nombre)

        popup = tk.Toplevel(self)
        popup.title(f"Stock inicial — {nombre}")
        popup.geometry("300x160")
        popup.resizable(False, False)

        tk.Label(popup, text=f"Ingrese stock inicial:", font="sans 12").pack(pady=10)

        entry = ttk.Entry(popup)
        entry.pack(pady=5)

        def aplicar():
            try:
                cant = int(entry.get())
                if cant < 0:
                    messagebox.showerror("Error", "El stock no puede ser negativo")
                    return

                producto.stock = cant
                self.controller.editar_producto(producto)
                self.refrescar()
                popup.destroy()
                messagebox.showinfo("Éxito", f"Stock inicial registrado: {cant}")

            except:
                messagebox.showerror("Error", "Ingrese un número válido")

        tk.Button(popup, text="Aceptar", width=12, command=aplicar).pack(pady=10)

    # ================= EDITAR =================
    def editar_producto(self):
        sel = self.tre.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        vals = self.tre.item(sel[0], "values")
        nombre_original = vals[1]

        precio = self.precio.get().strip()
        costo = self.costo.get().strip()

        if not es_numero(precio) or not es_numero(costo):
            messagebox.showwarning("Advertencia", "Valores numéricos inválidos")
            return

        producto_actual = self.controller.obtener_por_nombre(nombre_original)
        if not producto_actual:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        prod = Producto(
            nombre=self.nombre.get(),
            proveedor=self.proveedor.get(),
            precio=float(precio),
            costo=float(costo),
            stock=producto_actual.stock  # stock se mantiene
        )

        try:
            self.controller.editar_producto(prod)
            messagebox.showinfo("Éxito", "Producto modificado")
            self.refrescar()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar: {e}")

    def on_select(self, event):
        sel = self.tre.selection()
        if sel:
            vals = self.tre.item(sel[0], "values")
            self.nombre.delete(0, "end"); self.nombre.insert(0, vals[1])
            self.proveedor.delete(0, "end"); self.proveedor.insert(0, vals[2])
            self.precio.delete(0, "end"); self.precio.insert(0, vals[3])
            self.costo.delete(0, "end"); self.costo.insert(0, vals[4])

    def limpiar(self):
        for w in (self.nombre, self.proveedor, self.precio, self.costo):
            w.delete(0, "end")

    # ================ MODIFICAR STOCK MANUAL ================
    def modificar_stock(self):
        sel = self.tre.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        nombre = self.tre.item(sel[0], "values")[1]
        producto = self.controller.obtener_por_nombre(nombre)

        popup = tk.Toplevel(self)
        popup.title(f"Modificar Stock: {nombre}")
        popup.geometry("300x150")
        popup.resizable(False, False)

        tk.Label(popup, text=f"Stock actual: {producto.stock}", font="sans 12").pack(pady=5)
        tk.Label(popup, text="Cantidad a modificar:").pack()

        entry_cantidad = ttk.Entry(popup)
        entry_cantidad.pack(pady=5)

        def aplicar_modificacion(signo=1):
            try:
                cantidad = int(entry_cantidad.get()) * signo
                if producto.stock + cantidad < 0:
                    messagebox.showerror("Error", f"No hay suficiente stock de {nombre}")
                    return
                producto.stock += cantidad
                self.controller.editar_producto(producto)
                self.refrescar()
                popup.destroy()
                messagebox.showinfo("Éxito", f"Nuevo stock: {producto.stock}")
            except:
                messagebox.showerror("Error", "Ingrese un número válido")

        frame_botones = tk.Frame(popup)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Sumar", width=10,
                  command=lambda: aplicar_modificacion(1)).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Restar", width=10,
                  command=lambda: aplicar_modificacion(-1)).pack(side="left", padx=5)
