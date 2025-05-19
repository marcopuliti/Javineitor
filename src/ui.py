# src/ui.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from .logica import (
    cambiar_grillado,
    guardar_archivo,
    limpiar,
    onclick
)

# Función para construir la interfaz gráfica
def construir_interfaz(ventana, estado):
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
    etiqueta.config(font=("Arial", 16), fg="blue")
    etiqueta.pack()

    # Frame lateral para los botones (a la izquierda)
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(side="left", fill="y", padx=10, pady=10)

    # Etiqueta para el cuadro de texto
    lbl_valor = tk.Label(frame_botones, text="Ingrese un valor de grilla:")
    lbl_valor.pack(pady=(20,5))  # Separado de los botones

    # Cuadro de texto (ancho de grilla)
    ancho_grilla = tk.Entry(frame_botones, width=15)
    ancho_grilla.pack(pady=5)

    # Botón para cambiar el grillado
    btn_leer = tk.Button(frame_botones, text="Cambiar grilla", command=lambda: cambiar_grillado(estado, ancho_grilla, canvas, ax))
    btn_leer.pack(pady=10)

    # Desplegable de accion
    opciones = ["vertices", "aristas", "matching"]
    accion = ttk.Combobox(frame_botones, values=opciones, state="readonly")
    accion.current(0)  # Seleccionar la primera por defecto
    accion.pack(pady=20)

    # Checkbutton Etiquetado
    # Crear variable booleana asociada al checkbox
    etiquetado = tk.BooleanVar()
    btn_etiquetado = tk.Checkbutton(frame_botones, text="Etiquetado", variable=etiquetado)
    btn_etiquetado.pack(pady=5)

    # Botón de guardar en el panel lateral
    btn_guardar = tk.Button(frame_botones, text="Guardar codigo tikz", command=lambda: guardar_archivo(etiquetado, estado))
    btn_guardar.pack(pady=10)

    # Botón de limpiar
    btn_limpiar = tk.Button(frame_botones, text="Borrar todo", command=lambda: limpiar(estado, ax, canvas, ancho_grilla))
    btn_limpiar.pack(pady=10)

    # Botón de salir
    btn_salir = tk.Button(frame_botones, text="Salir", command=ventana.quit)
    btn_salir.pack(pady=10)

    # Canvas de matplotlib embebido en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

    # Conectar evento de click
    fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, estado, accion))


# Función para crear la ventana principal
def crear_ventana(estado):
    ventana = tk.Tk()
    ventana.title("Javineitor")
    ventana.state('zoomed')

    # Crear la interfaz gráfica
    construir_interfaz(ventana, estado)

    return ventana
