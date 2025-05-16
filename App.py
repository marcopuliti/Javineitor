import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Defino la operacion de guardar archivo.
def cambiar_grillado():
    global GRID_SIZE  # Actualizamos la variable global

    try:
        GRID_SIZE = float(entrada_valor.get())
        
        # Limpiar el gráfico
        ax.clear()

        # Reconfigurar el gráfico con la nueva grilla
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title(f"Haz clic para añadir puntos (Grilla: {GRID_SIZE} unidades)")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Actualizar las líneas de la grilla más marcadas
        ax.set_xticks([GRID_SIZE*i for i in range(0, int(10/GRID_SIZE +1), 1)])
        ax.set_yticks([GRID_SIZE*i for i in range(0, int(10/GRID_SIZE +1), 1)])

        # Redibujar el canvas actualizado
        canvas.draw()

    except ValueError:
        print("Por favor, ingrese un valor numérico válido.")
def guardar_archivo():
    
    # Abrir ventana para elegir ruta de guardado
    archivo_path = filedialog.asksaveasfilename(
        title="Guardar archivo como...",
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )

    # Si el usuario eligió una ubicación:
    if archivo_path:
        with open(archivo_path, 'w', encoding='utf-8') as f:
        
            f.write("\\begin{tikzpicture}[commutative diagrams/every diagram,thick] \n\n    % Vertices\n")
            
            # Vertices
            if etiquetado_var.get():
                for (x, y) in puntos.keys():
                    f.write(f"    \\node[draw,circle] ({puntos[(x,y)]}) at ({x},{y}) {{\(v_{{ {puntos[(x,y)]} }}\)}};\n")  # Formato: x,y en cada línea
            else:
                for (x, y) in puntos.keys():
                    f.write(f"    \\node[draw,circle,fill] ({puntos[(x,y)]}) at ({x},{y}) {{ }};\n")  # Formato: x,y en cada línea
                    
            # Aristas
            if len(aristas)>0:
                f.write("\n    %Aristas\n")
                string = "    \\foreach \\from/\\to in {"
                for arista in aristas:
                    string += f" {{{puntos[arista[0]]}/{puntos[arista[1]]}}},"
                string = string[:-1]+"} {\n        \\path[draw] (\\from) -- (\\to);}\n"
                f.write(string)
                    
            # Matching
            if len(matching)>0:
                f.write("\n    %Matching\n")
                string = "    \\foreach \\from/\\to in {"
                for arista in matching:
                    string += f" {{{puntos[arista[0]]}/{puntos[arista[1]]}}},"
                string = string[:-1]+"} {\n        \\path[decorate, decoration={snake,amplitude=2mm, segment length=4mm},draw=red] (\\from) -- (\\to);}\n"
                f.write(string)
        
            f.write("\end{tikzpicture}")
        
        print(f"Archivo guardado en: {archivo_path}")
    else:
        print("El usuario canceló la operación.")
def snap_to_grid(x, y, grid_size):
    """Ajusta las coordenadas (x, y) a la grilla más cercana."""
    x_snapped = round(x / grid_size) * grid_size
    y_snapped = round(y / grid_size) * grid_size
    return x_snapped, y_snapped
def onclick(event):
    global Media_arista
    global aristas
    global extremo1
    global extremo2
    global etiqueta
    global matching
    global combo_opciones
    
    Etapa = combo_opciones.get()
           
    if event.button == 1: # Click izquierdo
        if Etapa == "vertices":
    
            if event.xdata is not None and event.ydata is not None:
                # Ajustar a la grilla
                x, y = snap_to_grid(event.xdata, event.ydata, GRID_SIZE)
                puntos[(x, y)] = etiqueta
                etiqueta += 1
                # Dibujar punto
                plt.scatter(x, y, color='black', s=50)
#                plt.draw()
    
        elif Etapa == "aristas":
        
            if event.xdata is not None and event.ydata is not None:
                # Ajustar a la grilla
                x, y = snap_to_grid(event.xdata, event.ydata, GRID_SIZE)
                if not Media_arista:
                    extremo1 = (x, y)
                    Media_arista = True
                else:
                    extremo2 = (x,y)
                    aristas.append((extremo1,extremo2))
                    Media_arista = False
                # Dibujar linea
                if len(aristas)>0:
                    for arista in aristas:
                        ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='blue', linestyle='-', linewidth=2, label='Línea entre puntos')
#                plt.draw()
        
        elif Etapa == "matching":
            
            if event.xdata is not None and event.ydata is not None:
                # Ajustar a la grilla
                x, y = snap_to_grid(event.xdata, event.ydata, GRID_SIZE)
                if not Media_arista:
                    extremo1 = (x, y)
                    Media_arista = True
                else:
                    extremo2 = (x,y)
                    matching.append((extremo1,extremo2))
                    Media_arista = False
                # Dibujar linea
                if len(matching)>0:
                    for arista in matching:
                        ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='red', linestyle='-', linewidth=2, label='Línea entre puntos')
        plt.draw()

# Crear la ventana principal
root = tk.Tk()
root.title("Javineitor")
root.geometry("600x400")

# Frame lateral para los botones (a la izquierda)
frame_botones = tk.Frame(root)
frame_botones.pack(side="left", fill="y", padx=10, pady=10)

# Etiqueta para el cuadro de texto
lbl_valor = tk.Label(frame_botones, text="Ingrese un valor de grilla:")
lbl_valor.pack(pady=(20,5))  # Separado de los botones

# Cuadro de texto (Entry)
entrada_valor = tk.Entry(frame_botones, width=15)
entrada_valor.pack(pady=5)

# Botón para cambiar el grillado
btn_leer = tk.Button(frame_botones, text="Cambiar grilla", command=cambiar_grillado)
btn_leer.pack(pady=10)

# Desplegable de accion
opciones = ["vertices", "aristas", "matching"]
combo_opciones = ttk.Combobox(frame_botones, values=opciones, state="readonly")
combo_opciones.current(0)  # Seleccionar la primera por defecto
combo_opciones.pack(pady=20)

# Checkbutton Etiquetado
# Crear variable booleana asociada al checkbox
etiquetado_var = tk.BooleanVar()
btn_etiquetado = tk.Checkbutton(frame_botones, text="Etiquetado", variable=etiquetado_var)
btn_etiquetado.pack(pady=5)

# Botón de guardar en el panel lateral
btn_guardar = tk.Button(frame_botones, text="Guardar codigo tikz", command=guardar_archivo)
btn_guardar.pack(pady=10)



# Configuración de la grilla
GRID_SIZE = 1  # Tamaño de la grilla (ej: 1.0 para coordenadas enteras, 0.5 para medias unidades)
puntos = {}  # Diccionario para guardar coordenadas (x, y) como clave con su etiqueta
aristas = [] # 
etiqueta = 0
Media_arista = False
extremo1, extremo2 = (0,0), (0,0)
matching = []
        
        
# Configuración del gráfico
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title(f"Haz clic para añadir puntos (Grilla: {GRID_SIZE} unidades)")
ax.set_xlabel("Eje X")
ax.set_ylabel("Eje Y")
ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # Grilla visible

# Líneas de la grilla más marcadas
ax.set_xticks([GRID_SIZE*i for i in range(0, int(10/GRID_SIZE +1), 1)])
ax.set_yticks([GRID_SIZE*i for i in range(0, int(10/GRID_SIZE +1), 1)])


# Canvas de matplotlib embebido en Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

# Conectar evento de click
fig.canvas.mpl_connect('button_press_event', onclick)

# Ejecutar la ventana
root.mainloop()    
