import tkinter as tk
from pathlib import Path
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class AplicacionRestaurante:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante - Sistema de Ventas")
        self.root.geometry("950x600")
        self.root.minsize(800, 500)

        ruta_base = Path(__file__).resolve().parent
        carpeta_datos = ruta_base / "datos"

        # Cargar icono/logo de ventana
        ruta_icono = ruta_base / "assets" / "logo_imagen.png"
        if ruta_icono.exists():
            try:
                self.icono = tk.PhotoImage(file=str(ruta_icono))
                self.root.iconphoto(True, self.icono)
            except: pass

        # Inicializar servicios
        archivo_serv = ArchivoServicio(carpeta_datos)
        self.servicio = RestauranteServicio(archivo_serv)

        self.vista_actual = None
        self.mostrar_login()

    def cambiar_vista(self, nueva):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.vista_actual = nueva
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self):
        vista = LoginView(self.root, self.servicio, self.mostrar_principal)
        self.cambiar_vista(vista)

    def mostrar_principal(self, usuario):
        vista = MainView(self.root, self.servicio, usuario, self.mostrar_login)
        self.cambiar_vista(vista)

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplicacionRestaurante()
    app.ejecutar()