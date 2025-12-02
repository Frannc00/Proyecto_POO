import tkinter as tk
from tkinter import messagebox
from src.models.usuario_model import UsuarioModel
from src.views.register_view import RegisterWindow
from src.views.contenedor import Contenedor

class LoginController:
    def __init__(self):
        self.usuario_model = UsuarioModel()
        self.usuario_actual = None
        self.rol_actual = None

        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.config(bg="#F5F5F5")

        self._build()
        self._centrar_ventana(400, 300)
        self.root.mainloop()

    def _build(self):
        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="#F5F5F5").pack(pady=20)

        # Usuario
        tk.Label(self.root, text="Usuario:", bg="#F5F5F5").pack()
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady=5)

        # Contraseña
        tk.Label(self.root, text="Contraseña:", bg="#F5F5F5").pack()
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.pack(pady=5)

        # Mostrar contraseña
        self.var_ver = tk.IntVar()
        tk.Checkbutton(self.root, text="Mostrar contraseña", bg="#F5F5F5",
                       variable=self.var_ver, command=self._toggle_password).pack()

        # Botones
        tk.Button(self.root, text="Ingresar", width=15, command=self.login).pack(pady=15)
        tk.Button(self.root, text="Registrar usuario", width=15, command=self.registrar).pack()

    def _centrar_ventana(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _toggle_password(self):
        self.entry_pass.config(show="" if self.var_ver.get() else "*")

    def login(self):
        usuario = self.entry_user.get().strip()
        contraseña = self.entry_pass.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return

        resultado = self.usuario_model.validar(usuario, contraseña)
        if resultado:
            self.usuario_actual, self.rol_actual = resultado
            messagebox.showinfo("Bienvenido", f"Hola {self.usuario_actual} ({self.rol_actual})")
            self.root.destroy()  # cerrar login
            # Abrir Contenedor como Tk
            app = Contenedor(self)
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar(self):
        # Siempre permitir registrar usuario, sin importar si ya existen otros
        RegisterWindow(self)

    def registrar_usuario(self, usuario, contraseña, rol, codigo_secreto=None):
        # Si el rol es "admin", verificamos el código secreto
        if rol == "admin" and codigo_secreto != "tu_codigo_secreto":  # Cambia por el código real
            messagebox.showerror("Error", "Código secreto incorrecto")
            return False

        # Crear el usuario, sin verificar existencia
        return self.usuario_model.crear_usuario(usuario, contraseña, rol, codigo_secreto)
