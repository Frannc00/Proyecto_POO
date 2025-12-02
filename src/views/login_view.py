import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from src.views.register_view import RegisterWindow  # <-- nueva ventana

class LoginWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Login")
        self.geometry("500x500")

        # === CENTRAR VENTANA ===
        self.centrar_ventana(500, 500)

        # === IMAGEN DE USUARIO ===
        ruta_img = os.path.join(os.path.dirname(__file__), "..", "assets", "user.png")
        ruta_img = os.path.abspath(ruta_img)

        try:
            imagen = Image.open(ruta_img)
            imagen = imagen.resize((180, 180))
            self.foto = ImageTk.PhotoImage(imagen)
            tk.Label(self, image=self.foto).pack(pady=10)
        except Exception as e:
            print("No se pudo cargar la imagen:", e)

        # === CAMPOS DE LOGIN ===
        tk.Label(self, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.pack()

        tk.Label(self, text="Contraseña:").pack(pady=5)

        # caja password
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack()

        # mostrar/ocultar contraseña
        self.ver_pass = tk.IntVar()
        tk.Checkbutton(self, text="Mostrar contraseña", variable=self.ver_pass,
                       command=self.toggle_password).pack(pady=5)

        # botón ingresar
        tk.Button(self, text="Ingresar", command=self.login).pack(pady=15)

        # botón registrar usuario
        tk.Button(self, text="Registrarse", bg="#d0d0d0",
                  command=self.abrir_registro).pack(pady=5)

    # ============================
    # MÉTODO PARA CENTRAR VENTANA
    # ============================
    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ============================
    # MOSTRAR/OCULTAR CONTRASEÑA
    # ============================
    def toggle_password(self):
        if self.ver_pass.get():
            self.entry_pass.config(show="")
        else:
            self.entry_pass.config(show="*")

    # ============================
    # LOGIN
    # ============================
    def login(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()

        datos_user = self.controller.validar_login(user, pwd)

        if datos_user:
            # datos_user = (id, usuario, rol)
            self.controller.usuario_logueado = datos_user
            self.destroy()
            self.controller.iniciar_app()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # ============================
    # ABRIR VENTANA DE REGISTRO
    # ============================
    def abrir_registro(self):
        # SOLO ADMIN PUEDE REGISTRAR
        try:
            if self.controller.usuario_logueado[2] != "admin":
                messagebox.showerror("Acceso denegado", "Solo un ADMIN puede crear usuarios.")
                return
        except:
            pass  # antes de loguearse no existe usuario_logueado

        RegisterWindow(self.controller)
