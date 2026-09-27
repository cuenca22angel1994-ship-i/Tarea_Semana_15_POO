import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar):
        super().__init__(master, bg="#fef6e9")
        self.servicio = restaurante_servicio
        self.usuario = usuario_actual
        self.al_cerrar = al_cerrar
        self.opciones_usuarios = {}
        self.opciones_productos = {}
        self.construir_interfaz()

    def construir_interfaz(self):
        # Barra lateral
        sidebar = tk.Frame(self, bg="#d35400", width=200, padx=15, pady=20)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="RESTAURANTE", font=("Arial", 16, "bold"),
                 bg="#00c5d3", fg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(sidebar, text=self.usuario.nombre, font=("Arial", 10),
                 bg="#d35400", fg="#ffedd5").pack(anchor="w", pady=(0, 25))

        self.botones = {}
        self.crear_boton_menu(sidebar, "Inicio", self.mostrar_inicio)
        self.crear_boton_menu(sidebar, "Usuarios", self.mostrar_usuarios)
        self.crear_boton_menu(sidebar, "Productos", self.mostrar_productos)
        self.crear_boton_menu(sidebar, "Ventas", self.mostrar_ventas)

        tk.Frame(sidebar, bg="#d35400").pack(fill="both", expand=True)
        ttk.Button(sidebar, text="Cerrar Sesión", command=self.al_cerrar).pack(fill="x", pady=(15, 0))

        # Área principal
        self.contenido = tk.Frame(self, bg="#fef6e9", padx=25, pady=20)
        self.contenido.pack(side="right", fill="both", expand=True)

        self.mostrar_inicio()

    def crear_boton_menu(self, padre, texto, comando):
        btn = tk.Button(padre, text=texto, command=comando,
                        bg="#e67e22", fg="white", font=("Arial", 10, "bold"),
                        relief="flat", padx=10, pady=8, anchor="w")
        btn.pack(fill="x", pady=4)
        self.botones[texto] = btn

    def marcar_activo(self, actual):
        for txt, btn in self.botones.items():
            btn.config(bg="#e67e22" if txt != actual else "#f39c12")

    def limpiar_contenido(self):
        for w in self.contenido.winfo_children():
            w.destroy()

    def etiqueta_titulo(self, texto):
        tk.Label(self.contenido, text=texto, font=("Arial", 20, "bold"),
                 bg="#fef6e9", fg="#d35400").pack(anchor="w", pady=(0, 15))

    # --- Sección: Inicio ---
    def mostrar_inicio(self):
        self.marcar_activo("Inicio")
        self.limpiar_contenido()
        self.etiqueta_titulo("Panel Principal")
        tk.Label(self.contenido, text=f"Bienvenido/a, {self.usuario.nombre}",
                 font=("Arial", 12), bg="#fef6e9").pack(anchor="w", pady=(0, 20))

        resumen = [
            ("Usuarios", self.servicio.cantidad_usuarios()),
            ("Productos", self.servicio.cantidad_productos()),
            ("Ventas", self.servicio.cantidad_ventas())
        ]
        for tit, val in resumen:
            f = tk.Frame(self.contenido, bg="white", padx=20, pady=15)
            f.pack(side="left", padx=(0, 15))
            tk.Label(f, text=tit, bg="white", font=("Arial", 10, "bold")).pack()
            tk.Label(f, text=str(val), bg="white", font=("Arial", 24, "bold"), fg="#d35400").pack()

    # --- Sección: Usuarios ---
    def mostrar_usuarios(self):
        self.marcar_activo("Usuarios")
        self.limpiar_contenido()
        self.etiqueta_titulo("Usuarios Registrados")
        self.tabla_simple(("ID", "Nombre", "Usuario"),
                          [(u.identificador, u.nombre, u.usuario) for u in self.servicio.listar_usuarios()])

    # --- Sección: Productos ---
    def mostrar_productos(self):
        self.marcar_activo("Productos")
        self.limpiar_contenido()
        self.etiqueta_titulo("Gestión de Productos")

        form = tk.LabelFrame(self.contenido, text="Datos del Producto", padx=15, pady=15, bg="white")
        form.pack(fill="x", pady=(0, 15))

        tk.Label(form, text="Código:", bg="white").grid(row=0, column=0, sticky="w")
        self.cod_prod = tk.Entry(form)
        self.cod_prod.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Nombre:", bg="white").grid(row=1, column=0, sticky="w")
        self.nom_prod = tk.Entry(form)
        self.nom_prod.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Precio:", bg="white").grid(row=2, column=0, sticky="w")
        self.pre_prod = tk.Entry(form)
        self.pre_prod.grid(row=2, column=1, pady=5)

        acc = tk.Frame(form, bg="white")
        acc.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(acc, text="Guardar", command=self.guardar_producto, bg="#27ae60", fg="white").pack(side="left", padx=5)
        tk.Button(acc, text="Limpiar", command=lambda: self.limpiar_form_prod(), bg="#95a5a6", fg="white").pack(side="left", padx=5)

        self.tabla_prod = self.tabla_simple(("Código", "Nombre", "Precio"), [])
        self.refrescar_productos()

    def guardar_producto(self):
        try:
            self.servicio.registrar_producto(self.cod_prod.get(), self.nom_prod.get(), self.pre_prod.get())
            messagebox.showinfo("OK", "Producto registrado")
            self.limpiar_form_prod()
            self.refrescar_productos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def limpiar_form_prod(self):
        self.cod_prod.delete(0, tk.END)
        self.nom_prod.delete(0, tk.END)
        self.pre_prod.delete(0, tk.END)

    def refrescar_productos(self):
        self.tabla_prod.delete(*self.tabla_prod.get_children())
        for p in self.servicio.listar_productos():
            self.tabla_prod.insert("", tk.END, values=(p.codigo, p.nombre, f"${p.precio:.2f}"))

    # --- Sección: Ventas ← NUEVA ---
    def mostrar_ventas(self):
        self.marcar_activo("Ventas")
        self.limpiar_contenido()
        self.etiqueta_titulo("Registro de Ventas")

        # Formulario de venta
        form = tk.LabelFrame(self.contenido, text="Nueva Venta", padx=15, pady=15, bg="white")
        form.pack(fill="x", pady=(0, 15))

        # Seleccionar Usuario
        tk.Label(form, text="Usuario:", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.opciones_usuarios = {f"{u.identificador} - {u.nombre}": u.identificador
                                  for u in self.servicio.listar_usuarios()}
        self.cmb_usuario = ttk.Combobox(form, values=list(self.opciones_usuarios.keys()), state="readonly", width=40)
        self.cmb_usuario.grid(row=0, column=1, pady=5, padx=10)

        # Seleccionar Producto
        tk.Label(form, text="Producto:", bg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.opciones_productos = {f"{p.codigo} - {p.nombre}": p.codigo
                                   for p in self.servicio.listar_productos()}
        self.cmb_producto = ttk.Combobox(form, values=list(self.opciones_productos.keys()), state="readonly", width=40)
        self.cmb_producto.grid(row=1, column=1, pady=5, padx=10)

        # Botón con command= → callback
        tk.Button(form, text=" Registrar Venta",
                  command=self.registrar_venta,  # ← callback, NO escribir registrar_venta()
                  bg="#d37000", fg="white", font=("Arial", 11, "bold"), padx=15, pady=8).grid(row=2, column=0, columnspan=2, pady=12)

        # Tabla de ventas
        tk.Label(self.contenido, text="Ventas Realizadas", font=("Arial", 12, "bold"), bg="#fef6e9").pack(anchor="w", pady=(10, 5))
        self.tabla_ventas = self.tabla_simple(("ID Venta", "Usuario", "Producto", "Fecha"), [])
        self.refrescar_ventas()

    def registrar_venta(self):
        """Callback: obtiene datos de la interfaz y delega al servicio"""
        sel_usuario = self.cmb_usuario.get()
        sel_producto = self.cmb_producto.get()

        usuario_id = self.opciones_usuarios.get(sel_usuario, "")
        producto_cod = self.opciones_productos.get(sel_producto, "")

        try:
            self.servicio.registrar_venta(usuario_id, producto_cod)
            messagebox.showinfo(" Venta Registrada", "La venta se guardó correctamente.")
            self.cmb_usuario.set("")
            self.cmb_producto.set("")
            self.refrescar_ventas()  # Actualizar vista inmediatamente
        except ValueError as e:
            messagebox.showerror("Error en Venta", str(e))

    def refrescar_ventas(self):
        self.tabla_ventas.delete(*self.tabla_ventas.get_children())
        for v in self.servicio.listar_ventas():
            u = self.servicio.buscar_usuario_por_id(v.usuario_id)
            p = self.servicio.buscar_producto_por_codigo(v.producto_codigo)
            nom_usuario = f"{u.identificador} - {u.nombre}" if u else v.usuario_id
            nom_producto = f"{p.codigo} - {p.nombre}" if p else v.producto_codigo
            self.tabla_ventas.insert("", tk.END, values=(v.identificador, nom_usuario, nom_producto, v.fecha))

    # Utilidad: tabla genérica
    def tabla_simple(self, columnas, filas):
        tabla = ttk.Treeview(self.contenido, columns=columnas, show="headings", height=8)
        for c in columnas:
            tabla.heading(c, text=c)
            tabla.column(c, width=150)
        tabla.pack(fill="both", expand=True)
        for f in filas:
            tabla.insert("", tk.END, values=f)
        return tabla