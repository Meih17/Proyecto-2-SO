import tkinter as tk
from tkinter import filedialog
import csv



# Variables que vamos a necesitar tirar en la otra ventana 
archivo_csv = None
semilla = None
algoritmo = None
num_procesos = None
num_operaciones = None


# ================================================================
# FUNCIONES DE APOYO
# ================================================================

# Funcion para leer los archivos 
def cargar_datos(nombre_archivo):
    with open(nombre_archivo) as archivo_csv:
        return csv.reader(archivo_csv)
        # for fila in lector_csv:
        #     print(fila)


# Funcion para abrir el CSV
def abrir_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if archivo:
        if archivo.endswith(".csv"):
            archivo_csv = cargar_datos(archivo)
            if semilla_input.get() != "":
                csv_button.config(bg="green", fg="white")
                msj_error.set("")

                # ENVIAR A LA OTRA VENTANA
                #archivo_csv
                algoritmo = algoritmo_variable.get()
                semilla = semilla_input.get()
                print(algoritmo+" - "+semilla+" - "+str(archivo_csv))

            else:
                csv_button.config(bg="red", fg="white")
                msj_error.set("Le faltó la semilla")
        else:
            csv_button.config(bg="red", fg="white")
            msj_error.set("Error, verifique el archivo")


# Funcion para ver si todos los campos estan llenos en caso de
def generar_verificar_campos():
    if semilla_input.get() != "" and procesos_input.get() != "" and operaciones_input.get() != "":
        generar_button.config(bg="green", fg="white")
        msj_error.set("")

        # ENVIAR A  LA OTRA VENTANA
        algoritmo = algoritmo_variable.get()
        semilla = semilla_input.get()
        num_procesos = procesos_input.get()
        num_operaciones = operaciones_input.get()
        print(algoritmo+" - "+semilla+" - "+num_procesos+" - "+num_operaciones)

    else:
        generar_button.config(bg="red", fg="white")
        msj_error.set("Error, algún campo vacío")




# ==================================================================
# CREACION DE LA VENTANA
# ==================================================================

ventana = tk.Tk()
ventana.title("Preparación de procesos")


#Texto para errores
msj_error = tk.StringVar()
msj_error.set("")


# Semilla
semilla_label = tk.Label(ventana, text="Semilla")
semilla_label.grid(row=0, column=0, pady=20, padx=20)
semilla_input = tk.Entry(ventana, justify="center", width=10)
semilla_input.insert(0, 2)
semilla_input.grid(row=0, column=1, padx=(0,20))


# Seleccione algoritmo
algoritmo_label = tk.Label(ventana, text="Seleccione algoritmo")
algoritmo_label.grid(row=1, column=0, pady=20, padx=20)
algoritmos = ["FIFO", "Second Chance", "LRU", "MRU", "Random"]
algoritmo_variable = tk.StringVar(ventana)
algoritmo_variable.set(algoritmos[0])
algoritmo_dropdown = tk.OptionMenu(ventana, algoritmo_variable, *algoritmos)
algoritmo_dropdown.grid(row=1, column=1, padx=(0,20))


# Numero de procesos
procesos_label = tk.Label(ventana, text="Número de procesos")
procesos_label.grid(row=3, column=0, pady=20, padx=20)
procesos_input = tk.Entry(ventana, justify="center", width=10)
procesos_input.insert(0,3)
procesos_input.grid(row=3, column=1, padx=(0,20))


# Cantidad de operaciones
operaciones_label = tk.Label(ventana, text="Cantidad de operaciones")
operaciones_label.grid(row=4, column=0, pady=20, padx=20)
operaciones_input = tk.Entry(ventana, justify="center", width=10)
operaciones_input.insert(0,16)
operaciones_input.grid(row=4, column=1, padx=(0,20))


# Ir a la siguiente ventana con el CSV
csv_button = tk.Button(ventana, text="Cargar CSV!", command=abrir_archivo)
csv_button.grid(row=5, column=0, columnspan=1, pady=30)


# Ir a la siguiente ventana usando los datos
generar_button = tk.Button(ventana, text="Generar!", command=generar_verificar_campos)
generar_button.grid(row=5, column=1, columnspan=1, pady=30, padx=(0,30))

mensaje_error = tk.Label(ventana, textvariable=msj_error)
mensaje_error.grid(row=6, column=0, pady=10, padx=20)

# para mantener abierta la ventana
ventana.mainloop()