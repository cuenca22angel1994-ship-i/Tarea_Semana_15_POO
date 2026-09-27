# Tarea_Semana_15_POO
Conceptos fundamentales de manejo de eventos en restaurante_app
# Alumno:
Angel R. Cuenca T.

# Objetivo
Comprender los fundamentos del manejo de eventos mediante el registro de ventas:
- `command=` → enlaza un botón con una función callback
- El callback obtiene los datos de la interfaz
- Delega la lógica al servicio `RestauranteServicio`
- Persiste en `ventas.json`
- Refresca la tabla para mostrar el resultado

# Estructura
 
restaurante_app/
├── datos/            # Archivos JSON
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/          # Clases de datos
├── servicios/        # Lógica y persistencia
├── ui/               # Interfaz gráfica
├── assets/           # Logo e iconos
└── main.py           # Ejecutar aquí
   

# Flujo de la Venta
1. Usuario inicia sesión
2. Selecciona **Ventas** en el menú
3. Elige un usuario y un producto de las listas desplegables
4. Pulsa **"Registrar Venta"** → `command=registrar_venta`
5. El callback valida → llama a `servicio.registrar_venta()`
6. Se guarda en `ventas.json`
7. La tabla se actualiza automáticamente
