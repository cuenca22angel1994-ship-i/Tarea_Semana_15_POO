from datetime import date
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [
            Usuario(
                datos.get("identificador", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contraseña", datos.get("contrasena", "")),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", ""),
                datos.get("nombre", ""),
                datos.get("precio", 0),
            )
            for datos in productos_json
        ]

        self.ventas = [
            Venta(
                datos.get("identificador", ""),
                datos.get("usuario_id", ""),
                datos.get("producto_codigo", ""),
                datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def validar_acceso(self, usuario, contraseña):
        for u in self.usuarios:
            if u.usuario == usuario and u.contraseña == contraseña:
                return u
        return None

    def cantidad_usuarios(self): return len(self.usuarios)
    def cantidad_productos(self): return len(self.productos)
    def cantidad_ventas(self): return len(self.ventas)

    def listar_usuarios(self): return self.usuarios
    def listar_productos(self): return self.productos
    def listar_ventas(self): return self.ventas

    def buscar_producto_por_codigo(self, codigo):
        codigo = codigo.strip()
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    def buscar_usuario_por_id(self, identificador):
        identificador = identificador.strip()
        for u in self.usuarios:
            if u.identificador == identificador:
                return u
        return None

    def guardar_productos(self):
        datos = [{"codigo": p.codigo, "nombre": p.nombre, "precio": p.precio} for p in self.productos]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def guardar_ventas(self):
        datos = [
            {
                "identificador": v.identificador,
                "usuario_id": v.usuario_id,
                "producto_codigo": v.producto_codigo,
                "fecha": v.fecha,
            }
            for v in self.ventas
        ]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    def generar_id_venta(self):
        return f"V{len(self.ventas)+1:03d}"

    def registrar_venta(self, usuario_id, producto_codigo):
        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")
        if not self.buscar_usuario_por_id(usuario_id):
            raise ValueError("El usuario no existe.")
        if not self.buscar_producto_por_codigo(producto_codigo):
            raise ValueError("El producto no existe.")

        nueva_venta = Venta(
            self.generar_id_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat()
        )
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta

    # CRUD de productos
    def registrar_producto(self, codigo, nombre, precio):
        if self.buscar_producto_por_codigo(codigo):
            raise ValueError("Ya existe un producto con ese código.")
        self.productos.append(Producto(codigo, nombre, precio))
        self.guardar_productos()

    def actualizar_producto(self, codigo, nombre, precio):
        p = self.buscar_producto_por_codigo(codigo)
        if not p: raise ValueError("Producto no encontrado.")
        p.nombre = nombre
        p.precio = precio
        self.guardar_productos()

    def eliminar_producto(self, codigo):
        p = self.buscar_producto_por_codigo(codigo)
        if not p: raise ValueError("Producto no encontrado.")
        self.productos.remove(p)
        self.guardar_productos()