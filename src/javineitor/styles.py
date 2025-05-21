"""
Configuración de estilos para la interfaz gráfica de Javineitor.
"""

# Colores
COLOR_FONDO = "#f0f0f0"
COLOR_BOTONES = "#4a90e2"
COLOR_TEXTO = "#2c3e50"
COLOR_BOTON_ACTIVO = "#357abd"

# Fuentes
FUENTE_NORMAL = ("Arial", 10)
FUENTE_TITULO = ("Arial", 11, "bold")
FUENTE_ENCABEZADO = ("Arial", 16)

# Configuración de botones
BUTTON_CONFIG = {
    "bg": COLOR_BOTONES,
    "fg": "white",
    "font": FUENTE_NORMAL,
    "relief": "flat",
    "activebackground": COLOR_BOTON_ACTIVO,
    "activeforeground": "white",
    "cursor": "hand2"
}

# Configuración de etiquetas
LABEL_CONFIG = {
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO,
    "font": FUENTE_TITULO
}

# Configuración de checkbuttons
CHECKBUTTON_CONFIG = {
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO,
    "font": FUENTE_NORMAL,
    "selectcolor": COLOR_FONDO
}

# Configuración del encabezado
HEADER_CONFIG = {
    "font": FUENTE_ENCABEZADO,
    "fg": "blue"
} 