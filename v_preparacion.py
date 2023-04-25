import tkinter as tk

ventana = tk.Tk()
ventana.title("Preparación de procesos")

# Semilla
semilla_label = tk.Label(ventana, text="Semilla")
semilla_label.grid(row=0, column=0, pady=20, padx=20)
semilla_input = tk.Entry(ventana, width=10)
semilla_input.grid(row=0, column=1, padx=(0,20))

# Seleccione algoritmo
algoritmo_label = tk.Label(ventana, text="Seleccione algoritmo")
algoritmo_label.grid(row=1, column=0, pady=20, padx=20)
algoritmos = ["FIFO", "Second Chance", "LRU", "MRU", "Random"]
algoritmo_variable = tk.StringVar(ventana)
algoritmo_variable.set(algoritmos[0])
algoritmo_dropdown = tk.OptionMenu(ventana, algoritmo_variable, *algoritmos)
algoritmo_dropdown.grid(row=1, column=1, padx=(0,20))

# Cargar CSV
csv_button = tk.Button(ventana, text="Cargar CSV")
csv_button.grid(row=2, column=0, columnspan=2, pady=20, padx=20)

# Numero de procesos
procesos_label = tk.Label(ventana, text="Número de procesos")
procesos_label.grid(row=3, column=0, pady=20, padx=20)
procesos_input = tk.Entry(ventana, width=10)
procesos_input.grid(row=3, column=1, padx=(0,20))

# Cantidad de operaciones
operaciones_label = tk.Label(ventana, text="Cantidad de operaciones")
operaciones_label.grid(row=4, column=0, pady=20, padx=20)
operaciones_input = tk.Entry(ventana, width=10)
operaciones_input.grid(row=4, column=1, padx=(0,20))

# Ir a la siguiente ventana y enviar la informacion
listo = tk.Button(ventana, text="Listo!")
listo.grid(row=5, column=0, columnspan=2, pady=30)




ventana.mainloop()