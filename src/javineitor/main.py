from javineitor.logica import EstadoGraficador
from javineitor.ui import crear_ventana

def main():


    # Crear instancia del estado y la ventana
    estado = EstadoGraficador()
    ventana = crear_ventana(estado)

    # Iniciar el bucle principal de la ventana
    ventana.mainloop()

if __name__ == "__main__":
    main()
