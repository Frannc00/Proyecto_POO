import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from reportlab.pdfgen import canvas
import os
import datetime

class FacturaView(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        super().__init__(parent, bg="#F5F5F5")
        self.controller = controller
        self.rol_usuario = rol_usuario

        tk.Label(
            self,
            text="FACTURAS",
            font=("Arial", 18, "bold"),
            bg="#b3afaf"
        ).pack(fill="x", pady=5)

        main = tk.Frame(self, bg="#AFDBC7")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # ============================
        # BUSCADOR
        # ============================
        search_frame = tk.Frame(main, bg="#AFDBC7")
        search_frame.pack(fill="x", pady=5)

        tk.Label(search_frame, text="Buscar:", font=("Arial", 11), bg="#AFDBC7").pack(side="left", padx=5)
        self.busqueda = ttk.Entry(search_frame, width=30)
        self.busqueda.pack(side="left", padx=5)

        ttk.Button(search_frame, text="Buscar", command=self.buscar).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Mostrar Todo", command=self.refrescar).pack(side="left", padx=5)

        # ============================
        # TABLA
        # ============================
        tabla_frame = tk.Frame(main, bg="#AFDBC7")
        tabla_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("id", "fecha", "total", "items", "pago"),
            show="headings",
            height=10
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("total", text="Total")
        self.tree.heading("items", text="Cant. Productos")
        self.tree.heading("pago", text="Forma de Pago")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("fecha", width=180, anchor="center")
        self.tree.column("total", width=100, anchor="center")
        self.tree.column("items", width=80, anchor="center")
        self.tree.column("pago", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # ============================
        # BOTONES
        # ============================
        btn_frame = tk.Frame(main, bg="#AFDBC7")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Ver detalles", command=self.ver_detalle).pack(side="left", padx=10)

        # 🔥 BOTÓN ELIMINAR FACTURA (solo admin)
        if self.rol_usuario == "admin":
            tk.Button(
                btn_frame,
                text="Eliminar Factura",
                bg="#ff4d4d",
                fg="white",
                command=self.eliminar_factura
            ).pack(side="left", padx=10)

        self.refrescar()

    # ================================================================
    # RECARGAR TABLA
    # ================================================================
    def refrescar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for factura in self.controller.listar_facturas():
            factura_id = factura[0]
            detalles = self.controller.detalle_factura(factura_id)
            cantidad_items = sum([d[3] for d in detalles]) if detalles else 0
            forma_pago = "Efectivo"  # TEMPORAL
            self.tree.insert(
                "",
                tk.END,
                values=(factura[0], factura[1], factura[2], cantidad_items, forma_pago)
            )

    # ================================================================
    # BUSCAR FACTURA
    # ================================================================
    def buscar(self):
        termino = self.busqueda.get().strip()
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese texto para buscar")
            return

        for i in self.tree.get_children():
            self.tree.delete(i)

        resultados = self.controller.buscar_facturas(termino)
        for factura in resultados:
            factura_id = factura[0]
            detalles = self.controller.detalle_factura(factura_id)
            cantidad_items = sum([d[3] for d in detalles]) if detalles else 0
            forma_pago = "Efectivo"
            self.tree.insert(
                "",
                tk.END,
                values=(factura[0], factura[1], factura[2], cantidad_items, forma_pago)
            )

    # ================================================================
    # ELIMINAR FACTURA (solo admin)
    # ================================================================
    def eliminar_factura(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una factura para eliminar")
            return

        factura_id = self.tree.item(sel[0], "values")[0]
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que desea eliminar la factura #{factura_id}?"
        )
        if not confirmar:
            return

        try:
            self.controller.eliminar_factura(factura_id)
            messagebox.showinfo("Éxito", "Factura eliminada correctamente")
            self.refrescar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la factura:\n{e}")

    # ================================================================
    # DETALLE FACTURA
    # ================================================================
    def ver_detalle(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una factura")
            return

        factura_id = self.tree.item(sel[0], "values")[0]
        detalles = self.controller.detalle_factura(factura_id)

        if not detalles:
            messagebox.showinfo("Detalle", "No hay detalles para esta factura")
            return

        win = Toplevel(self)
        win.title(f"Factura #{factura_id}")
        win.geometry("350x450")
        win.config(bg="white")

        tk.Label(win, text=f"TICKET FACTURA #{factura_id}", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        frame_texto = tk.Frame(win, bg="white")
        frame_texto.pack(fill="both", expand=True)

        texto = tk.Text(frame_texto, width=40, height=20, font=("Courier", 10))
        texto.pack(fill="both", expand=True)

        texto.insert(tk.END, "        KIOSCO EL AMIGO\n")
        texto.insert(tk.END, "    -------------------------\n")
        texto.insert(tk.END, f"  Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        texto.insert(tk.END, f"  Factura N° {factura_id}\n")
        texto.insert(tk.END, "    -------------------------\n\n")

        total = 0
        for d in detalles:
            prod = d[2]
            cant = d[3]
            precio = d[4]
            subtotal = d[5]
            total += subtotal
            texto.insert(tk.END, f"{prod}\n")
            texto.insert(tk.END, f"  x{cant}  ${precio:.2f}   Sub: ${subtotal:.2f}\n\n")

        texto.insert(tk.END, "------------------------------\n")
        texto.insert(tk.END, f"TOTAL: ${total:.2f}\n")
        texto.insert(tk.END, "------------------------------\n")
        texto.insert(tk.END, "\n   ¡Gracias por su compra!\n")

        texto.config(state="disabled")

        boton_frame = tk.Frame(win, bg="white")
        boton_frame.pack(pady=10)

        tk.Button(boton_frame, text="Cerrar", command=win.destroy).pack(side="left", padx=10)
        tk.Button(
            boton_frame,
            text="Imprimir Ticket (PDF)",
            command=lambda: self.generar_pdf(factura_id, detalles)
        ).pack(side="left", padx=10)

    # ================================================================
    # GENERAR PDF
    # ================================================================
    def generar_pdf(self, factura_id, detalles):
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

        total = 0
        pdf.drawString(50, y, "----------------------------------------")
        y -= 20

        for d in detalles:
            prod = d[2]
            cant = d[3]
            precio = d[4]
            subtotal = d[5]
            total += subtotal
            pdf.drawString(50, y, prod)
            y -= 15
            pdf.drawString(50, y, f"x{cant}  ${precio:.2f}   Subtotal: ${subtotal:.2f}")
            y -= 25

        pdf.drawString(50, y, "----------------------------------------")
        y -= 20
        pdf.drawString(50, y, f"TOTAL: ${total:.2f}")
        y -= 40
        pdf.drawString(50, y, "Gracias por su compra!")
        pdf.save()

        messagebox.showinfo("PDF generado", f"Ticket guardado en:\n{ruta}")
