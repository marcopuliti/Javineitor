# src/ui.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys

from .logica import (
    cambiar_grillado,
    guardar_archivo,
    limpiar,
    onclick
)
from .styles import (
    COLOR_FONDO,
    BUTTON_CONFIG,
    LABEL_CONFIG,
    CHECKBUTTON_CONFIG,
    HEADER_CONFIG
)

# Función para construir la interfaz gráfica
def construir_interfaz(ventana, estado):
    """
    Construye la interfaz gráfica principal de la aplicación.
    
    Args:
        ventana: Ventana principal de Tkinter
        estado: Objeto que mantiene el estado de la aplicación
    """
    def on_enter_press(event):
        """Maneja el evento de presionar Enter en el campo de entrada de grilla."""
        btn_cambiar_grilla.invoke()

    # Configuración del gráfico
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title(f"Haz clic para añadir puntos (Grilla: {1} unidades)")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # Grilla visible

    # Líneas de la grilla más marcadas
    ax.set_xticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
    ax.set_yticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])

    etiqueta = tk.Label(ventana, text="Bienvenido a Javineitor!")
    etiqueta.configure(**HEADER_CONFIG)
    etiqueta.pack()

    # Frame superior para los controles
    frame_controles = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_controles.pack(fill="x", padx=10, pady=5)

    # Frame izquierdo para el control de grilla
    frame_grilla = tk.Frame(frame_controles, bg=COLOR_FONDO)
    frame_grilla.pack(side="left", padx=10)

    # Etiqueta para el cuadro de texto
    lbl_grilla = tk.Label(frame_grilla, text="Grilla:")
    lbl_grilla.configure(**LABEL_CONFIG)
    lbl_grilla.pack(side="left", padx=5)

    # Cuadro de texto (ancho de grilla)
    entrada_grilla = tk.Entry(frame_grilla, width=5)
    entrada_grilla.pack(side="left", padx=5)

    # Botón para cambiar el grillado
    btn_cambiar_grilla = tk.Button(frame_grilla, text="Cambiar", command=lambda: cambiar_grillado(estado, entrada_grilla, canvas, ax))
    btn_cambiar_grilla.configure(**BUTTON_CONFIG)
    btn_cambiar_grilla.pack(side="left", padx=5)

    # Vincular la tecla Enter al botón de cambiar grilla
    entrada_grilla.bind('<Return>', on_enter_press)

    # Frame central para las acciones principales
    frame_acciones = tk.Frame(frame_controles, bg=COLOR_FONDO)
    frame_acciones.pack(side="left", padx=10)

    # Desplegable de accion
    opciones = ["vertices", "aristas", "matching", "set"]
    accion = ttk.Combobox(frame_acciones, values=opciones, state="readonly", width=10)
    accion.current(0)  # Seleccionar la primera por defecto
    accion.pack(side="left", padx=5)

    # Checkbutton Etiquetado
    etiquetado = tk.BooleanVar()
    btn_etiquetado = tk.Checkbutton(frame_acciones, text="Etiquetado", variable=etiquetado)
    btn_etiquetado.configure(**CHECKBUTTON_CONFIG)
    btn_etiquetado.pack(side="left", padx=5)

    # Frame derecho para los botones de acción
    frame_botones = tk.Frame(frame_controles, bg=COLOR_FONDO)
    frame_botones.pack(side="right", padx=10)

    # Botón de guardar
    btn_guardar = tk.Button(frame_botones, text="Guardar tikz", command=lambda: guardar_archivo(etiquetado, estado))
    btn_guardar.configure(**BUTTON_CONFIG)
    btn_guardar.pack(side="left", padx=5)

    # Botón para generar diccionario
    btn_diccionario = tk.Button(frame_botones, text="Copiar dict", command=lambda: estado.copiar_diccionario(ventana))
    btn_diccionario.configure(**BUTTON_CONFIG)
    btn_diccionario.pack(side="left", padx=5)

    # Botón de limpiar
    btn_limpiar = tk.Button(frame_botones, text="Borrar", command=lambda: limpiar(estado, ax, canvas, entrada_grilla))
    btn_limpiar.configure(**BUTTON_CONFIG)
    btn_limpiar.pack(side="left", padx=5)

    # Botón de salir
    btn_salir = tk.Button(frame_botones, text="Salir", command=ventana.quit)
    btn_salir.configure(**BUTTON_CONFIG)
    btn_salir.pack(side="left", padx=5)

    # Canvas de matplotlib embebido en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

    # Conectar evento de click
    fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, estado, accion, ax, canvas))
    
    # Configurar estilo de la ventana
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    style.configure("TCombobox", padding=6)
    
    # Aplicar color de fondo a la ventana principal
    ventana.configure(bg=COLOR_FONDO)

# Función para crear la ventana principal
def crear_ventana(estado):
    ventana = tk.Tk()
    ventana.title("Javineitor")
    ventana.state('zoomed')

    # Crear la interfaz gráfica
    construir_interfaz(ventana, estado)

    # Asegura que al cerrar la ventana se termine el programa completamente
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), sys.exit()))

    return ventana
