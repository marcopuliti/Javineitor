from tkinter import filedialog
from matplotlib import pyplot as plt


class EstadoGraficador:
    def __init__(self):
        self.grid_size = 1
        self.puntos = {}
        self.aristas = []
        self.matching = []
        self.sets = []  # Lista de conjuntos de vértices
        self.current_set = set()  # Set temporal para almacenar vértices seleccionados
        self.media_arista = False
        self.extremo1 = None
        self.extremo2 = None
    
    def __str__(self):
        return f"EstadoGraficador(grid_size={self.grid_size}, puntos={self.puntos}, aristas={self.aristas}, matching={self.matching}, sets={self.sets})"
    def __repr__(self):
        return f"EstadoGraficador(grid_size={self.grid_size}, puntos={self.puntos}, aristas={self.aristas}, matching={self.matching}, sets={self.sets})"
    def finalizar_set_actual(self):
        """Finaliza el set actual y lo agrega a la lista de sets si no está vacío."""
        if self.current_set:
            self.sets.append(list(self.current_set))
            self.current_set = set()
            return True
        return False
    def copiar_diccionario(self, ventana):
        """
        Genera un diccionario de adyacencias a partir del estado actual.
        """
        diccionario = {self.puntos[(x, y)]: [] for (x, y) in self.puntos.keys()}
        for (x1, y1), (x2, y2) in self.aristas:
            diccionario[self.puntos[(x1, y1)]].append(self.puntos[(x2, y2)])
        ventana.clipboard_clear()
        ventana.clipboard_append(str(diccionario))

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

            # Sets
            if len(estado.sets) > 0:

                f.write("\n    %Sets\n")
                for set_vertices in estado.sets:
                    string = "    \\node[draw,circle, inner sep = .5 cm ,fit="
                    for x, y in set_vertices:
                        string += f"({estado.puntos[(x,y)]}) "
                    string = string+"] {};\n"
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
    Etapa = accion.get() # Obtener el valor del desplegable
    if event.xdata is not None and event.ydata is not None: # Verificar que el clic fue dentro de los límites
        x, y = snap_to_grid(event.xdata, event.ydata, estado.grid_size) # Ajustar a la grilla
        if event.button == 1: # Click izquierdo
            if Etapa == "vertices":
                if (x, y) in estado.puntos.keys(): # Verificar si el punto ya existe
                     pass
                else:
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta 
                    ax.scatter(x, y, color='black', s=50) # Dibujar punto
            elif Etapa == "set":
                if (x, y) in estado.puntos.keys():
                    # Agregar el punto al set actual
                    estado.current_set.add((x, y))
                    # Redibujar el punto en rojo para mostrar que está seleccionado
                    ax.scatter(x, y, color='red', s=50)
                else:
                    # Si el punto no existe, crearlo y agregarlo al set
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta
                    estado.current_set.add((x, y))
                    ax.scatter(x, y, color='red', s=50)
            elif Etapa == "aristas":
                if (x, y) in estado.puntos.keys(): # Verificar si el punto ya existe
                    pass
                else:
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta
                    plt.scatter(x, y, color='black', s=50) # Dibujar punto
                if not estado.media_arista:
                    estado.extremo1 = (x, y)
                    estado.media_arista = True
                else:
                    estado.extremo2 = (x,y)
                    if (estado.extremo1,estado.extremo2) in estado.aristas or (estado.extremo2,estado.extremo1) in estado.aristas:
                        pass
                    else:
                        estado.aristas.append((estado.extremo1,estado.extremo2))
                    estado.media_arista = False
                for arista in estado.aristas: # Dibujar aristas
                    plt.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='blue', linestyle='-', linewidth=2, label='Línea entre puntos')
            elif Etapa == "matching":
                if (x, y) in estado.puntos.keys(): # Verificar si el punto ya existe
                    pass
                else:
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta
                    plt.scatter(x, y, color='black', s=50) # Dibujar punto
                if not estado.media_arista:
                    estado.extremo1 = (x, y)
                    estado.media_arista = True
                else:
                    estado.extremo2 = (x,y)
                    if (estado.extremo1,estado.extremo2) in estado.matching or (estado.extremo2,estado.extremo1) in estado.matching:
                        pass
                    else:
                        estado.matching.append((estado.extremo1,estado.extremo2))
                    estado.media_arista = False
                for arista in estado.matching:
                    plt.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], color='red', linestyle='-', linewidth=2, label='Línea entre puntos')
            elif Etapa == "set":
                if (x, y) in estado.puntos.keys():
                    # Agregar el punto al set actual
                    estado.current_set.add((x, y))
                    # Redibujar el punto en rojo para mostrar que está seleccionado
                    ax.scatter(x, y, color='red', s=50)
                else:
                    # Si el punto no existe, crearlo y agregarlo al set
                    etiqueta = len(estado.puntos)
                    estado.puntos[(x, y)] = etiqueta
                    estado.current_set.add((x, y))
                    ax.scatter(x, y, color='red', s=50)
            plt.draw()
        elif event.button == 3: # Click derecho
            if Etapa == "set":
                # Finalizar el set actual y agregarlo a la lista de sets
                if estado.finalizar_set_actual():
                    # Redibujar todos los puntos en negro
                    ax.cla()  # Limpiar el gráfico actual
                    ax.set_xlim(0, 10)
                    ax.set_ylim(0, 10)
                    ax.set_title(f"Haz clic para añadir puntos (Grilla: {estado.grid_size} unidades)")
                    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
                    ax.set_xticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
                    ax.set_yticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
                    
                    # Redibujar todos los puntos
                    for (x, y) in estado.puntos.keys():
                        ax.scatter(x, y, color='black', s=50)
                    
                    # Redibujar aristas
                    for arista in estado.aristas:
                        ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], 
                               color='blue', linestyle='-', linewidth=2)
                    
                    # Redibujar matching
                    for arista in estado.matching:
                        ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], 
                               color='red', linestyle='-', linewidth=2)
                    
                    # Dibujar los sets anteriores con diferentes colores
                    colores_sets = ['green', 'purple', 'orange', 'brown', 'pink']
                    for i, set_vertices in enumerate(estado.sets):
                        color = colores_sets[i % len(colores_sets)]
                        for x, y in set_vertices:
                            ax.scatter(x, y, color=color, s=50)
            else:
                # Eliminar punto
                if (x, y) in estado.puntos.keys(): # Verificar si el punto ya existe
                    del estado.puntos[(x, y)]
                    for i, (punto, etiqueta) in enumerate(estado.puntos.items()): # Reetiquetar los puntos restantes
                        estado.puntos[punto] = i
                    # Eliminar aristas asociadas
                    estado.aristas = [arista for arista in estado.aristas if arista[0] != (x, y) and arista[1] != (x, y)]
                    estado.matching = [arista for arista in estado.matching if arista[0] != (x, y) and arista[1] != (x, y)]
                    # Redibujar el gráfico
                    ax.cla()  # Limpiar el gráfico actual
                    ax.set_xlim(0, 10)
                    ax.set_ylim(0, 10)
                    ax.set_title(f"Haz clic para añadir puntos (Grilla: {estado.grid_size} unidades)")
                    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
                    ax.set_xticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
                    ax.set_yticks([estado.grid_size*i for i in range(0, int(10/estado.grid_size +1), 1)])
                    for (x, y) in estado.puntos.keys():
                        ax.scatter(x, y, color='black', s=50)
                    # Redibujar aristas
                    if len(estado.aristas) > 0:
                        for arista in estado.aristas:
                            ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], 
                                   color='blue', linestyle='-', linewidth=2)
                    # Redibujar matching
                    if len(estado.matching) > 0:
                        for arista in estado.matching:
                            ax.plot([arista[0][0], arista[1][0]], [arista[0][1], arista[1][1]], 
                                   color='red', linestyle='-', linewidth=2)
                    # Redibujar sets
                    colores_sets = ['green', 'purple', 'orange', 'brown', 'pink']
                    for i, set_vertices in enumerate(estado.sets):
                        color = colores_sets[i % len(colores_sets)]
                        for x, y in set_vertices:
                            ax.scatter(x, y, color=color, s=50)
            canvas.draw()