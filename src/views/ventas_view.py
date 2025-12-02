# src/views/ventas_view.py
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import datetime
import os
from reportlab.pdfgen import canvas

from src.controllers.producto_controller import ProductoController
from src.controllers.factura_controller import FacturaController


class VentasView(tk.Frame):
    def __init__(self, parent, producto_ctrl: ProductoController, factura_ctrl: FacturaController):
        super().__init__(parent, bg="#F5F5F5")
        self.producto_ctrl = producto_ctrl
        self.factura_ctrl = factura_ctrl
        self.items = []
        self.lista_productos = []  # necesario para autocompletado
        self._build()

    def actualizar(self):
        self._cargar_productos()

    def _build(self):
        tk.Label(self, text="Ventas", font="sans 18 bold", bg="#b3afaf").pack(fill="x")

        frame = tk.Frame(self, bg="#AFDBC7")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = tk.LabelFrame(frame, text="Información de Venta", bg="#AFDBC7")
        top_frame.pack(fill="x", padx=5, pady=5)

        fila1 = tk.Frame(top_frame, bg="#AFDBC7")
        fila1.pack(fill="x", pady=5)

        # ---------- PRODUCTO ----------
        tk.Label(fila1, text="Producto:", bg="#AFDBC7").pack(side="left", padx=5)

        self.comboproducto = ttk.Combobox(fila1, state="normal")
        self.comboproducto.pack(side="left", padx=5)

        # Autocompletar estilo Google
        self.comboproducto.bind("<KeyRelease>", self._filtrar_productos)
        self.comboproducto.bind("<<ComboboxSelected>>", self._actualizar_precio)
        self.comboproducto.bind("<FocusOut>", self._actualizar_precio)
        self.comboproducto.bind("<Tab>", self._tab_autocomplete)

        # ---------- PRECIO ----------
        tk.Label(fila1, text="Precio:", bg="#AFDBC7").pack(side="left", padx=5)
        self.entry_precio = ttk.Entry(fila1, state="readonly")
        self.entry_precio.pack(side="left", padx=5)

        # ---------- CANTIDAD ----------
        tk.Label(fila1, text="Cantidad:", bg="#AFDBC7").pack(side="left", padx=5)
        self.entry_cantidad = ttk.Entry(fila1)
        self.entry_cantidad.pack(side="left", padx=5)

        # ---------- STOCK ----------
        self.label_stock = tk.Label(fila1, text="Stock disponible: 0", bg="#AFDBC7")
        self.label_stock.pack(side="left", padx=5)

        tk.Button(fila1, text="Agregar Artículo", command=self.agregar_articulo).pack(side="left", padx=10)

        # ---------- TABLA ----------
        tabla_frame = tk.Frame(frame, bg="#AFDBC7")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tabla_frame, columns=("Producto", "Precio", "Cantidad", "Subtotal"), show="headings")
        for col in ("Producto", "Precio", "Cantidad", "Subtotal"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)

        tk.Button(tabla_frame, text="Eliminar artículo", command=self.eliminar_articulo).pack(pady=5)

        # ---------- TOTAL ----------
        bottom = tk.Frame(frame, bg="#AFDBC7")
        bottom.pack(fill="x", padx=5, pady=5)

        self.label_total = tk.Label(bottom, text="Total a Pagar: $ 0", font="sans 18 bold", bg="#AFDBC7")
        self.label_total.pack(side="left", padx=10)

        tk.Button(bottom, text="Pagar", command=self.abrir_ventana_pago).pack(side="right", padx=10)

        self._cargar_productos()

    # ============================================================
    #        AUTOCOMPLETADO ESTILO GOOGLE (REAL)
    # ============================================================
    def _filtrar_productos(self, event):
        texto = self.comboproducto.get().lower()

        coincidencias = [p for p in self.lista_productos if texto in p.lower()]

        if coincidencias:
            self.comboproducto["values"] = coincidencias
            self.comboproducto.event_generate("<Down>")  # abre lista
        else:
            self.comboproducto["values"] = self.lista_productos

        self._actualizar_precio()

    def _tab_autocomplete(self, event):
        texto = self.comboproducto.get().lower()
        coincidencias = [p for p in self.lista_productos if texto in p.lower()]

        if coincidencias:
            self.comboproducto.delete(0, "end")
            self.comboproducto.insert(0, coincidencias[0])
            self._actualizar_precio()

        return "break"

    # ============================================================
    #                   CARGA DE PRODUCTOS
    # ============================================================
    def _cargar_productos(self):
        productos = self.producto_ctrl.listar_todos()
        self.lista_productos = [p.nombre for p in productos]
        self.comboproducto["values"] = self.lista_productos

    # ============================================================
    #              ACTUALIZAR PRECIO Y STOCK
    # ============================================================
    def _actualizar_precio(self, event=None):
        nombre = self.comboproducto.get()
        p = self.producto_ctrl.obtener_por_nombre(nombre)

        if p:
            self.entry_precio.config(state="normal")
            self.entry_precio.delete(0, "end")
            self.entry_precio.insert(0, p.precio)
            self.entry_precio.config(state="readonly")
            self.label_stock.config(text=f"Stock disponible: {p.stock}")

    # ============================================================
    #                     AGREGAR ARTÍCULO
    # ============================================================
    def agregar_articulo(self):
        nombre = self.comboproducto.get()
        precio = self.entry_precio.get()
        cantidad = self.entry_cantidad.get()

        if not (nombre and precio and cantidad):
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
            prod = self.producto_ctrl.obtener_por_nombre(nombre)
            if not prod or prod.stock < cantidad:
                messagebox.showerror("Error", "Sin stock suficiente")
                return

            subtotal = precio * cantidad
            self.tree.insert("", "end", values=(nombre, precio, cantidad, subtotal))
            self.entry_cantidad.delete(0, "end")
            self._actualizar_total()

        except:
            messagebox.showerror("Error", "Cantidad inválida")

    # ============================================================
    #                     ELIMINAR ARTÍCULO
    # ============================================================
    def eliminar_articulo(self):
        sel = self.tree.selection()
        if sel:
            for s in sel:
                self.tree.delete(s)
            self._actualizar_total()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un artículo a eliminar")

    # ============================================================
    #                     ACTUALIZAR TOTAL
    # ============================================================
    def _actualizar_total(self):
        total = sum(float(self.tree.item(i, "values")[3]) for i in self.tree.get_children())
        self.label_total.config(text=f"Total a Pagar: $ {total:.2f}")

    # ============================================================
    #                     VENTANA DE PAGO
    # ============================================================
    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay artículos cargados")
            return

        ventana = Toplevel(self)
        ventana.title("Realizar pago")
        ventana.geometry("400x250")

        tk.Label(ventana, text=self.label_total.cget("text"), font="sans 14 bold").pack(pady=10)
        tk.Label(ventana, text="Cantidad Pagada").pack()
        entry_pago = ttk.Entry(ventana)
        entry_pago.pack(pady=10)

        def calcular_y_guardar():
            try:
                pagado = float(entry_pago.get())
                carrito = []
                total = 0

                for ch in self.tree.get_children():
                    prod, precio, cant, sub = self.tree.item(ch, "values")
                    carrito.append({"producto": prod, "precio": float(precio), "cantidad": int(cant)})
                    total += float(sub)

                if pagado < total:
                    messagebox.showerror("Error", "Pago insuficiente")
                    return

                factura_id = self.factura_ctrl.crear_factura(carrito)

                # Actualizar stock
                for item in carrito:
                    p = self.producto_ctrl.obtener_por_nombre(item["producto"])
                    p.stock -= item["cantidad"]
                    self.producto_ctrl.editar_producto(p)

                try:
                    self.master.master.frames["Facturas"].refrescar()
                except:
                    pass

                ventana.destroy()
                self._mostrar_ticket(factura_id, carrito, total, pagado)

                for ch in self.tree.get_children():
                    self.tree.delete(ch)
                self._actualizar_total()

            except:
                messagebox.showerror("Error", "Valor inválido")

        tk.Button(ventana, text="Pagar", command=calcular_y_guardar).pack(pady=20)

    # ============================================================
    #                           TICKET
    # ============================================================
    def _mostrar_ticket(self, factura_id, carrito, total, pagado):
        win = Toplevel(self)
        win.title("Ticket")
        win.geometry("350x450")
        win.config(bg="white")

        texto = tk.Text(win, width=40, height=22, font=("Courier", 10))
        texto.pack(fill="both", expand=True)
        texto.insert(tk.END, "        KIOSCO EL AMIGO\n")
        texto.insert(tk.END, "    -------------------------\n")
        texto.insert(tk.END, f"  Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        texto.insert(tk.END, f"  Factura N° {factura_id}\n")
        texto.insert(tk.END, "    -------------------------\n\n")
        for item in carrito:
            prod = item["producto"]
            cant = item["cantidad"]
            precio = item["precio"]
            subtotal = cant * precio
            texto.insert(tk.END, f"{prod}\n")
            texto.insert(tk.END, f"  x{cant}  ${precio:.2f}  Sub: ${subtotal:.2f}\n\n")
        texto.insert(tk.END, "------------------------------\n")
        texto.insert(tk.END, f"TOTAL: ${total:.2f}\n")
        texto.insert(tk.END, f"PAGADO: ${pagado:.2f}\n")
        texto.insert(tk.END, f"VUELTO: ${pagado-total:.2f}\n")
        texto.insert(tk.END, "------------------------------\n\n")
        texto.insert(tk.END, "   ¡Gracias por su compra!\n")
        texto.config(state="disabled")

        botones = tk.Frame(win, bg="white")
        botones.pack(pady=10)
        tk.Button(botones, text="Cerrar", command=win.destroy).pack(side="left", padx=10)
        tk.Button(botones, text="Imprimir Ticket (PDF)",
                  command=lambda: self._generar_pdf(factura_id, carrito, total, pagado)).pack(side="left", padx=10)

    # ============================================================
    #                        PDF DEL TICKET
    # ============================================================
    def _generar_pdf(self, factura_id, carrito, total, pagado):
        if not os.path.exists("tickets"):
            os.makedirs("tickets")

        ruta = f"tickets/ticket_{factura_id}.pdf"
        pdf = canvas.Canvas(ruta)
        pdf.setFont("Courier", 10)

        y = 800
        pdf.drawString(200, y, "KIOSCO EL AMIGO")
        y -= 40
        pdf.drawString(50, y, f"Factura N° {factura_id}")
        y -= 20
        pdf.drawString(50, y, f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

        y -= 40
        for item in carrito:
            prod = item["producto"]
            cant = item["cantidad"]
            precio = item["precio"]
            subtotal = cant * precio
            pdf.drawString(50, y, prod)
            y -= 15
            pdf.drawString(50, y, f"x{cant}  ${precio:.2f}   Subtotal: ${subtotal:.2f}")
            y -= 25

        pdf.drawString(50, y, "----------------------------------------")
        y -= 20
        pdf.drawString(50, y, f"TOTAL: ${total:.2f}")
        y -= 20
        pdf.drawString(50, y, f"PAGADO: ${pagado:.2f}")
        y -= 20
        pdf.drawString(50, y, f"VUELTO: ${pagado-total:.2f}")
        y -= 30
        pdf.drawString(50, y, "Gracias por su compra!")
        pdf.save()

        messagebox.showinfo("PDF generado", f"Ticket guardado en:\n{ruta}")
