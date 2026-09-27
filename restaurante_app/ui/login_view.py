import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk  #  Esto soluciona el problema


class LoginView(tk.Frame):
    def __init__(self, master, restaurante_servicio, al_iniciar_sesion):
        super().__init__(master, bg="#ffffff")
        self.servicio = restaurante_servicio
        self.al_iniciar_sesion = al_iniciar_sesion

        self.logo_imagen = None  #  Referencia obligatoria
        self.construir_interfaz()

    def cargar_logo(self):
        #  Usa el NUEVO nombre que le pusiste
        ruta = Path(__file__).resolve().parent.parent / "assets" / "logo_imagen.png"
        # O si lo pusiste como jpg:
        # ruta = Path(__file__).resolve().parent.parent / "assets" / "logo.jpg"

        print(f" Buscando: {ruta}")
        print(f" Existe: {ruta.exists()}")

        if not ruta.exists():
            return None

        try:
            #  Pillow lee la imagen sin problemas de permisos
            img = Image.open(ruta)
            # Ajusta el tamaño (ancho, alto) como quieras verlo
            img = img.resize((180, 100), Image.Resampling.LANCZOS)
            self.logo_imagen = ImageTk.PhotoImage(img)
            print(" Logo cargado con éxito")
            return self.logo_imagen
        except Exception as e:
            print(f" Error: {e}")
            return None

    def construir_interfaz(self):
        centro = tk.Frame(self, bg="#ffffff", padx=40, pady=35)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        #  LOGO ARRIBA DEL TÍTULO
        self.cargar_logo()
        if self.logo_imagen:
            tk.Label(
                centro,
                image=self.logo_imagen,
                bg="#ffffff"
            ).pack(pady=(0, 5))  # Espacio entre logo y título

        # TÍTULO RESTAURANTE
        tk.Label(
            centro,
            text="RESTAURANTE",
            font=("Arial", 22, "bold"),
            bg="#ffffff",
            fg="#00d3c8"
        ).pack(pady=(0, 8))

        tk.Label(
            centro,
            text="Inicio de Sesión",
            font=("Arial", 12),
            bg="#ffffff",
            fg="#666666"
        ).pack(pady=(0, 20))

        tk.Label(centro, text="Usuario", bg="#ffffff", anchor="w").pack(fill="x")
        self.entrada_usuario = tk.Entry(centro, font=("Arial", 11))
        self.entrada_usuario.pack(fill="x", pady=(0, 15))

        tk.Label(centro, text="Contraseña", bg="#ffffff", anchor="w").pack(fill="x")
        self.entrada_contrasena = tk.Entry(centro, font=("Arial", 11), show="*")
        self.entrada_contrasena.pack(fill="x", pady=(0, 20))

        tk.Button(
            centro,
            text="Ingresar",
            command=self._al_pulsar_ingresar,
            bg="#d35400",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=6
        ).pack()

        self.etiqueta_error = tk.Label(centro, text="", fg="red", bg="#ffffff")
        self.etiqueta_error.pack(pady=(10, 0))

    def _al_pulsar_ingresar(self):
        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not usuario or not contrasena:
            self.etiqueta_error.config(text="Completa todos los campos")
            return

        resultado = self.servicio.validar_acceso(usuario, contrasena)
        if resultado:
            self.etiqueta_error.config(text="")
            self.al_iniciar_sesion(resultado)
        else:
            self.etiqueta_error.config(text="Usuario o contraseña incorrectos")