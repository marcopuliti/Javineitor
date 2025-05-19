from tkinter import filedialog
from matplotlib import pyplot as plt


class EstadoGraficador:
    def __init__(self):
        self.grid_size = 1
        self.puntos = {}
        self.aristas = []
        self.matching = []
        self.media_arista = False
        self.extremo1 = None
        self.extremo2 = None

def cambiar_grillado(estado, ancho_grilla, canvas, ax):
    try:
        estado.grid_size = float(ancho_grilla.get())
    except:  # noqa: E722
        estado.grid_size = 1
    ax.set_title(f"Haz clic para añadir puntos (Grilla: {estado.grid_size} unidades)")
    ax.set_xticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
    ax.set_yticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
    canvas.draw()

def guardar_archivo(etiquetado, estado):
    
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
            if etiquetado.get():
                for (x, y) in estado.puntos.keys():
                    f.write(f"    \\node[draw,circle] ({estado.puntos[(x,y)]}) at ({x},{y}) {{\\(v_{{ {estado.puntos[(x,y)]} }}\\)}};\n")  # Formato: x,y en cada línea
            else:
                for (x, y) in estado.puntos.keys():
                    f.write(f"    \\node[draw,circle,fill] ({estado.puntos[(x,y)]}) at ({x},{y}) {{ }};\n")  # Formato: x,y en cada línea

            # Aristas
            if len(estado.aristas)>0:
                f.write("\n    %Aristas\n")
                string = "    \\foreach \\from/\\to in {"
                for arista in estado.aristas:
                    string += f" {{{estado.puntos[arista[0]]}/{estado.puntos[arista[1]]}}},"
                string = string[:-1]+"} {\n        \\path[draw] (\\from) -- (\\to);}\n"
                f.write(string)
                    
            # Matching
            if len(estado.matching)>0:
                f.write("\n    %Matching\n")
                string = "    \\foreach \\from/\\to in {"
                for arista in estado.matching:
                    string += f" {{{estado.puntos[arista[0]]}/{estado.puntos[arista[1]]}}},"
                string = string[:-1]+"} {\n        \\path[decorate, decoration={snake,amplitude=2mm, segment length=4mm},draw=red] (\\from) -- (\\to);}\n"
                f.write(string)
        
            f.write("\\end{tikzpicture}")
        
        print(f"Archivo guardado en: {archivo_path}")
    else:
        print("El usuario canceló la operación.")

def limpiar(estado, ax, canvas, ancho_grilla):

    # Limpiar el gráfico
    ax.cla()  # Limpiar el gráfico actual
    
    # Limpiar los puntos y aristas
    estado.puntos = {}
    estado.aristas = []
    estado.matching = []

    try:
        estado.grid_size = float(ancho_grilla.get())
    except:  # noqa: E722
        estado.grid_size = 1  # Valor por defecto si no se ingresa nada

    # Reconfigurar el gráfico con la nueva grilla
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title(f"Haz clic para añadir puntos (Grilla: {estado.grid_size} unidades)")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Actualizar las líneas de la grilla más marcadas
    ax.set_xticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
    ax.set_yticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])

    # Redibujar el canvas actualizado
    canvas.draw()


def snap_to_grid(x, y, grid_size):
    """
    Ajusta las coordenadas (x, y) a la grilla más cercana.
    """
    x = round(x / grid_size) * grid_size
    y = round(y / grid_size) * grid_size
    return x, y

def onclick(event, estado, accion, ax, canvas):
    Etapa = accion.get()
    if event.button == 1: # Click izquierdo
        if Etapa == "vertices":
            if event.xdata is not None and event.ydata is not None:
                # Ajustar a la grilla
                x, y = snap_to_grid(event.xdata, event.ydata, estado.grid_size)
                # Verificar si el punto ya existe
                if (x, y) in estado.puntos.keys():
                    pass
                else:
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta
                    # Dibujar punto
                    ax.scatter(x, y, color='black', s=50)
        elif Etapa == "aristas":
            if event.xdata is not None and event.ydata is not None:
                # Ajustar a la grilla
                x, y = snap_to_grid(event.xdata, event.ydata, estado.grid_size)
                # Verificar si el punto ya existe
                if (x, y) in estado.puntos.keys():
                    pass
                else:
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta
                    # Dibujar punto
                    plt.scatter(x, y, color='black', s=50)
                if not estado.media_arista:
                    estado.extremo1 = (x, y)
                    estado.media_arista = True
                else:
                    estado.extremo2 = (x,y)
                    estado.aristas.append((estado.extremo1,estado.extremo2))
                    estado.media_arista = False
                # Dibujar linea
                if len(estado.aristas)>0:
                    for arista in estado.aristas:
                        plt.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='blue', linestyle='-', linewidth=2, label='Línea entre puntos')
        elif Etapa == "matching":
            if event.xdata is not None and event.ydata is not None:
                # Ajustar a la grilla
                x, y = snap_to_grid(event.xdata, event.ydata, estado.grid_size)

                # Verificar si el punto ya existe
                if (x, y) in estado.puntos.keys():
                    pass
                else:
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta
                    # Dibujar punto
                    plt.scatter(x, y, color='black', s=50)
                    plt.draw()

                if not estado.media_arista:
                    estado.extremo1 = (x, y)
                    estado.media_arista = True
                else:
                    estado.extremo2 = (x,y)
                    estado.matching.append((estado.extremo1,estado.extremo2))
                    estado.media_arista = False
                # Dibujar linea
                if len(estado.matching)>0:
                    for arista in estado.matching:
                        plt.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='red', linestyle='-', linewidth=2, label='Línea entre puntos')
        plt.draw()
    elif event.button == 3: # Click derecho
        # Eliminar punto
        if event.xdata is not None and event.ydata is not None:
            # Ajustar a la grilla
            x, y = snap_to_grid(event.xdata, event.ydata, estado.grid_size)

            # Verificar si el punto ya existe
            if (x, y) in estado.puntos.keys():
                # Eliminar el punto
                del estado.puntos[(x, y)]
                # Reetiquetar los puntos restantes
                for i, (punto, etiqueta) in enumerate(estado.puntos.items()):
                    estado.puntos[punto] = i
                # Eliminar aristas asociadas
                estado.aristas = [arista for arista in estado.aristas if arista[0] != (x, y) and arista[1] != (x, y)]
                estado.matching = [arista for arista in estado.matching if arista[0] != (x, y) and arista[1] != (x, y)]

                # Redibujar el gráfico
                ax.cla()  # Limpiar el gráfico actual
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 10)
                ax.set_title(f"Haz clic para añadir puntos (Grilla: {1} unidades)")
                ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # Grilla visible
                # Líneas de la grilla más marcadas
                ax.set_xticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
                ax.set_yticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
                for (x, y) in estado.puntos.keys():
                    ax.scatter(x, y, color='black', s=50)
                # Redibujar aristas
                if len(estado.aristas) > 0:
                    for arista in estado.aristas:
                        ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='blue', linestyle='-', linewidth=2, label='Línea entre puntos')
                # Redibujar matching
                if len(estado.matching) > 0:
                    for arista in estado.matching:
                        ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='red', linestyle='-', linewidth=2, label='Línea entre puntos')
                canvas.draw()