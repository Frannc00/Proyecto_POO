import tkinter as tk
from tkinter import ttk, messagebox

class RegisterWindow(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Registrar Usuario")
        self.geometry("400x350")
        self.config(bg="#F5F5F5")

        self.centrar_ventana(400, 350)

        tk.Label(self, text="Registrar nuevo usuario",
                 font=("Arial", 14, "bold"), bg="#F5F5F5").pack(pady=10)

        # USUARIO
        tk.Label(self, text="Usuario:", bg="#F5F5F5").pack()
        self.entry_user = tk.Entry(self)
        self.entry_user.pack(pady=5)

        # CONTRASEÑA
        tk.Label(self, text="Contraseña:", bg="#F5F5F5").pack()
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack(pady=5)

        # MOSTRAR CONTRASEÑA
        self.var_ver = tk.IntVar()
        tk.Checkbutton(self, text="Mostrar contraseña", bg="#F5F5F5",
                       variable=self.var_ver, command=self.toggle_password
        ).pack()

        # ROL
        tk.Label(self, text="Rol:", bg="#F5F5F5").pack(pady=5)
        self.combo_rol = ttk.Combobox(
            self, state="readonly",
            values=["admin", "empleado"]
        )
        self.combo_rol.current(1)  # Predeterminado en "empleado"
        self.combo_rol.pack()

        # CÓDIGO DE AUTORIZACIÓN PARA ADMIN
        self.code_label = tk.Label(self, text="Código de Autorización (admin only)", bg="#F5F5F5")
        self.code_label.pack(pady=5)
        self.entry_code = tk.Entry(self)
        self.entry_code.pack(pady=5)

        # Inicialmente ocultamos el código de autorización
        self.code_label.pack_forget()
        self.entry_code.pack_forget()

        # Mostramos el código de autorización solo si el rol es "admin"
        self.combo_rol.bind("<<ComboboxSelected>>", self.toggle_code_field)

        # BOTÓN GUARDAR
        tk.Button(self, text="Registrar", bg="#D0E0FF",
                  command=self.registrar).pack(pady=15)

    def toggle_code_field(self, event):
        # Si el rol es "admin", mostramos el campo de código
        if self.combo_rol.get() == "admin":
            self.code_label.pack(pady=5)
            self.entry_code.pack(pady=5)
        else:
            # Si no es "admin", ocultamos el campo de código
            self.code_label.pack_forget()
            self.entry_code.pack_forget()

    def centrar_ventana(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def toggle_password(self):
        if self.var_ver.get():
            self.entry_pass.config(show="")
        else:
            self.entry_pass.config(show="*")

    def registrar(self):
        usuario = self.entry_user.get().strip()
        contraseña = self.entry_pass.get().strip()
        rol = self.combo_rol.get()

        if not usuario or not contraseña:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        # Si el rol es "admin", validamos el código de autorización
        if rol == "admin":
            codigo = self.entry_code.get().strip()
            if codigo != "tu_codigo_secreto":  # Cambia este código por el que desees
                messagebox.showerror("Error", "Código de autorización incorrecto")
                return

        # Llamamos al controlador para registrar el usuario
        exito = self.controller.registrar_usuario(usuario, contraseña, rol, codigo_secreto=codigo)

        if exito:
            messagebox.showinfo("OK", "Usuario registrado correctamente")
            self.destroy()
        else:
            messagebox.showerror("Error", "Hubo un problema al registrar el usuario")
