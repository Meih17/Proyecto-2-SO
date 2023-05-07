# ===========================================================================
# Josué Gerardo Gutiérrez Mora y Susana Cen Xu
# Curso de Sistemas Operativos
# Sede San José
# Primer semestre el 2023
# ===========================================================================

# Para dibujar cosas bonitas
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from tkinter import *
import tkinter as tk
from tkinter import filedialog

# Matemáticas y otros
from math import ceil
import random
import copy
from computadora.Queue import Queue

# Algoritmos de paginación
from algoritmos.Random import Random
from algoritmos.SecondChance import SecondChance
from algoritmos.FIFO import FIFO
from algoritmos.MRU import MRU

# Ayudantes de memoria
from computadora.MmuAlg import MmuAlg
from computadora.MmuOpt import MmuOpt   # Este archivo ya aplica dentro de sí el algoritmo optimo


# Tablero de control
# ============================================================================
tablaProcesos = {}   # {key:pid, value: ptr} 
tablaProcesosQuitados = {}  # lo mismo que el anterior
tablaPTR = {}    # {key:ptr, value: size}
callMemoria = Queue()       # cola de llamadas
# ============================================================================



# Variables globales =========================================================
global nombre_archivo
global semilla
global llaveAlgoritmo
global paginaAlgoritmo
global llaveOptimo
global paginaOptimo
global mmuAlg
global mmuOpt


global archivo_csv
algoritmo_seleccionado = ""
global num_procesos
global num_operaciones

#=============================================================================




# colores de las filas
coloress = ["#FFFFFF","#C6EFCE","#FFEB9C","#FFC7CE","#B4C6E7","#F4B084"]
colores = [color for _ in range(100) for color in coloress]





# FUNCIONES ===================================================================

def crearProcesos(todosLosProcesos):
    tempcallMemoria = []
    for proceso in todosLosProcesos:
        tablaPTR[str(proceso[1])] = int(proceso[2])
        tempcallMemoria.append(proceso[1])
        if proceso[0] in tablaProcesos:
            fila_proceso = tablaProcesos[proceso[0]]
            fila_proceso.append(proceso[1])
            tablaProcesos[proceso[0]] = fila_proceso
        else:
            tablaProcesos[proceso[0]] = [proceso[1]]
    tempcallMemoria.extend(random.choices(tempcallMemoria, k=len(tempcallMemoria)*3))
    random.shuffle(tempcallMemoria)
    callMemoria.setQueue(tempcallMemoria)

def get_datos(mmuAlg):
    datos = []
    proceso = []
    cargados = []
    sin_cargar = []
    dic = mmuAlg.getState()
    for pag in dic: 
        list = dic[pag] 
        if list[1] not in proceso:
            proceso.append(list[1])
        
        if list[2] == True:
            cargados.append(pag)
        else:
            sin_cargar.append(pag)
    
    datos.append(len( proceso))
    datos.append(mmuAlg.getAlgorithm().getExecTime())
    datos.append(len(cargados)*4)
    datos.append(len(cargados)*4*100/400)
    datos.append(len(sin_cargar)*4)
    datos.append(len(sin_cargar)*4*100/1000)
    datos.append(len(cargados))
    datos.append(len(sin_cargar))
    datos.append(mmuAlg.getAlgorithm().getThrashingTime())
    datos.append(round((mmuAlg.getAlgorithm().getThrashingTime()/mmuAlg.getAlgorithm().getExecTime())*100, 2))
    datos.append(mmuAlg.getTotalFrag())
    return datos

def get_IDP(ptr):
    for IDP in tablaProcesos:
        if ptr in tablaProcesos[IDP]:
            return IDP
    return 0

def killproceso(ptr, mmuOpt, mmuAlg):
    del tablaPTR[ptr]
    key = [i for i in tablaProcesosQuitados if ptr in tablaProcesosQuitados[i]]
    key = key[0]
    fila_proceso = tablaProcesosQuitados[key]
    if len(fila_proceso) == 1:
        mmuAlg.killproceso(tablaProcesos[key])
        mmuOpt.killproceso(tablaProcesos[key])
        del tablaProcesosQuitados[key]
        del tablaProcesos[key]
    else:
        fila_proceso.remove(ptr)
        tablaProcesosQuitados[key] = fila_proceso


def finish(mmuOpt, mmuAlg):
    tablaProcesos.clear()
    tablaProcesosQuitados.clear()
    tablaPTR.clear()
    mmuAlg.finish()
    mmuOpt.finish()

def updateOptSlider(val):
    plt.pause(0.1)
    dicLen = len(mmuOpt.getState())
    pages = ceil(dicLen/20)
    global paginaOptimo
    if pages > 1:
        r = val * 10
        for x in range(pages):
            if r >= 10/pages*x and r < 10/pages*(x+1):
                paginaOptimo = x
    else:
            paginaOptimo = 0

def updateAlgSlider(val):
    plt.pause(0.1)
    dicLen = len(mmuAlg.getState())
    pages = ceil(dicLen/20)
    global paginaAlgoritmo
    if pages > 1:
        r = val * 10
        for x in range(pages):
            if r >= 10/pages*x and r < 10/pages*(x+1):
                paginaAlgoritmo = x
    else:
            paginaAlgoritmo = 0



def abrir_archivo_csv(fileName):
    allProcesses = []
    file = open(fileName, "r")
    for line in file:
        tempList = []
        for e in line.split(','):
            tempList.append(e.lstrip().rstrip())
        allProcesses.append(tempList)
    file.close()
    return allProcesses[1:]


# Funcion para abrir el CSV
def abrir_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if archivo:
        if archivo.endswith(".csv"):
            global archivo_csv
            archivo_csv = abrir_archivo_csv(archivo)
            if input_semilla.get() != "":
                csv_button.config(bg="green", fg="white")
                csv_go_button.config(bg="green", fg="white")
                msj_error.set("")

                # algoritmo = algoritmo_variable.get()
                # semilla = input_semilla.get()
                # print(algoritmo+" - "+semilla+" - "+str(archivo_csv))

            else:
                csv_button.config(bg="red", fg="white")
                csv_go_button.config(bg="red", fg="white")
                msj_error.set("Le faltó la semilla")
        else:
            csv_button.config(bg="red", fg="white")
            csv_go_button.config(bg="red", fg="white")
            msj_error.set("Error, verifique el archivo")


# Funcion para ver si todos los campos estan llenos en caso de
def generar_verificar_campos():
    if input_semilla.get() != "" and procesos_input.get() != "" and operaciones_input.get() != "":
        generar_button.config(bg="green", fg="white")
        msj_error.set("")

        # ENVIAR A  LA OTRA VENTANA
        global algoritmo_seleccionado
        algoritmo_seleccionado = algoritmo_variable.get()
        semilla = input_semilla.get()
        num_procesos = procesos_input.get()
        num_operaciones = operaciones_input.get()
        # print(algoritmo_seleccionado+" - "+semilla+" - "+num_procesos+" - "+num_operaciones)

    else:
        generar_button.config(bg="red", fg="white")
        msj_error.set("Error, algún campo vacío")


def paginacion_secondChance():
    global mmuAlg
    mmuAlg = MmuAlg(SecondChance())
    global semilla
    semilla = int(input_semilla.get())
    ventana.destroy()


def paginacion_random():
    global mmuAlg
    mmuAlg = MmuAlg(Random())
    global semilla
    semilla = int(input_semilla.get())
    ventana.destroy()


def paginacion_FIFO():
    global mmuAlg
    mmuAlg = MmuAlg(FIFO())
    global semilla
    semilla = int(input_semilla.get())
    ventana.destroy()

def paginacion_MRU():
    global mmuAlg
    mmuAlg = MmuAlg(MRU())
    global semilla
    semilla = int(input_semilla.get())
    ventana.destroy()


def correr_algoritmo():
    global algoritmo_seleccionado
    algoritmo_seleccionado = algoritmo_variable.get()
    if archivo_csv == []:
        csv_go_button.config(bg="red", fg="white")
        msj_error.set("Error, archivo no cargado")

    elif algoritmo_variable.get() == "Random":
        paginacion_random()
    elif algoritmo_variable.get() == "Second Chance":
        paginacion_secondChance()
    elif algoritmo_variable.get() == "FIFO":
        paginacion_FIFO()
    elif algoritmo_variable.get() == "MRU":
        paginacion_MRU()
    else:
        msj_error.set("Error, algo pasó")




if __name__ == '__main__':

    # VENTANA INICIAL DE OPCIONES ==============================================================================


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
    input_semilla = tk.Entry(ventana, justify="center", width=10)
    input_semilla.insert(0, 2)
    input_semilla.grid(row=0, column=1, padx=(0,20))


    # Seleccione algoritmo
    algoritmo_label = tk.Label(ventana, text="Seleccione algoritmo")
    algoritmo_label.grid(row=1, column=0, pady=20, padx=20)
    algoritmos = ["Second Chance","Random","MRU", "FIFO"]
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


    # Cargar el archivo CSV
    csv_button = tk.Button(ventana, text="Cargar CSV!", command=abrir_archivo)
    csv_button.grid(row=5, column=0, columnspan=1, pady=30)

    #
    csv_go_button = tk.Button(ventana, text="Correr", command=correr_algoritmo, background='red')
    csv_go_button.grid(row=6, column=0, columnspan=1, pady=30)

    # Ir a la siguiente ventana usando los datos
    generar_button = tk.Button(ventana, text="Generar!", command=correr_algoritmo)
    generar_button.grid(row=5, column=1, columnspan=1, pady=30, padx=(0,30))

    # Mensaje de error 
    mensaje_error = tk.Label(ventana, textvariable=msj_error)
    mensaje_error.grid(row=7, column=0, pady=10, padx=20)


    tk.mainloop()

    # ==========================================================================================================



    
    # Abrir archivos de procesos y preparar todo para su proceso
    random.seed(semilla)
    crearProcesos(archivo_csv)
    tablaProcesosQuitados = copy.deepcopy(tablaProcesos)
    finished = False
    CopiaDeMemoria = Queue()
    CopiaDeMemoria.setQueue(list(reversed(callMemoria.getQueue())).copy())
    mmuOpt = MmuOpt(CopiaDeMemoria, tablaPTR, tablaProcesos)




    # VENTANA MATPLOT DONDE SE VEN LOS GRÁFICOS =================================================================



    # Dibujamos
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    plt.get_current_fig_manager().resize(3000,3000) # numeros grandes para que cubra toda la pantalla
    plt.subplots_adjust(left=0.01,right=0.99, bottom=0.15)
    
    
    # Dibujamos los gráficos pero los ocultamos 
    fig.patch.set_visible(False)
    ax1.axis('off')
    ax1.axis('tight')
    ax2.axis('off')
    ax2.axis('tight')
    ax3.axis('off')
    ax3.axis('tight')
    ax4.axis('off')
    ax4.axis('tight')


    # Columnas en las tablas de comparación
    columnas_MMU = ('PAGE ID', 'PID', 'LOADED', 'L-ADDR', 'M-ADDR', 'D-ADDR','LOADED-T','MARK')

    # Columnas en los cuadritos de información
    columnnas_info1 = [  "Processes",
                        "Sim-Time"]
    
    columnnas_info2 = [ "RAM KB",
                        "RAM %",
                        "V-RAM-KB",
                        "V-RAM %"]

    columnnas_info3 = [ "PAGES LOADED",
                        "PAGES UNLOADED",
                        "Thrashing Segundos",
                        "Thrashing %",
                        "Fragmentación"]

    # mmucolores = ['#a2cc00','#445f95','#a41e69','#e9ab70','#e393b8','#e8e52b']
    mmucolores = ["#FFFFFF","#C6EFCE","#FFEB9C","#FFC7CE","#B4C6E7","#F4B084"]

    ramcolores = [[mmucolores[random.randint(0,5)] for x in range(150)]]
    plt.pause(0.1)

    # Titulos de las barras de RAM
    plt.gcf().text(0.48, 0.93, "RAM - OPT", fontsize=10)
    plt.gcf().text(0.48, 0.85, f"RAM - {algoritmo_seleccionado}", fontsize=10)

    # Titulos de las Tablas
    plt.gcf().text(0.23, 0.73, "MMU - OPT", fontsize=10)
    plt.gcf().text(0.73, 0.73, f"MMU - {algoritmo_seleccionado}", fontsize=10)



    

    # Cosa de abajo para ver el slider
    axOpt = plt.axes([0.01, 0.05, 0.05, 0.04])
    sldrOpt = Slider(axOpt, '', 0.0, 1.0, 0.0)
    sldrOpt.on_changed(updateOptSlider)
    
    axAlg = plt.axes([0.55, 0.05, 0.05, 0.04])
    sldrAlg = Slider(axAlg, '', 0.0, 1.0, 0.0)
    sldrAlg.on_changed(updateAlgSlider)


    paginaAlgoritmo = 0
    paginaOptimo = 0    
    while(not finished):

        # INCIALIZACION DE ALGORITMOS A CORRER ======================================================================================
        ptr_actual = callMemoria.pop()
        mmuOpt.execute(get_IDP(ptr_actual))
        mmuAlg.execute(ptr_actual, tablaPTR[ptr_actual],get_IDP(ptr_actual))
        # Colorcito para los cuadros que va creciendo
        ramOptcolores = [colores[0 if x==0 else int(mmuOpt.getState().get(x)[1])] for x in mmuOpt.getAlgorithm().getRam().getMemory()]
        ramAlgcolores = [colores[0 if x==0 else int(mmuAlg.getState().get(x)[1])] for x in mmuAlg.getAlgorithm().getRam().getMemory()]


    

        # GRÁFICO -> Cargador de RAM ==================================================================================================
        #RAM OPT
        ramOptTable = ax1.table(cellLoc='center', bbox=[0.1, 1.06, 2, 0.05],cellColours=[ramOptcolores])
        #RAM ALG
        ramAlgTable = ax1.table(cellLoc='center', bbox=[0.1, 0.8, 2, 0.05],cellColours=[ramAlgcolores])

        
        
        # GRAFICO -> tabla OPT =======================================================================================================
        llaveOptimo = list(mmuOpt.getState().keys())
        llaveOptimo.sort()
        if paginaOptimo > 0:
            if (sldrOpt.val==1):
                llaveOptimo = llaveOptimo[-20:]
            elif len(llaveOptimo)>paginaOptimo*20:
                llaveOptimo = llaveOptimo[paginaOptimo*20:20*(paginaOptimo+1)]
            else:
                llaveOptimo = llaveOptimo[-20:]
        else:
            llaveOptimo = llaveOptimo[:20]

        cellsOptText = [mmuOpt.getState().get(x) for x in llaveOptimo]
        color_celda_opt = [[colores[0 if x==0 else int(mmuOpt.getState().get(x)[1])] for i in range(8)] for x in llaveOptimo]
        mmuOptTable = ax1.table(cellText=cellsOptText, colLabels=columnas_MMU, loc='bottom', bbox=[0.1, -0.7, 0.9, 1.2],cellColours=color_celda_opt)
        mmuOptTable.auto_set_font_size(False)
        mmuOptTable.set_fontsize(8)



        # GRAFICO -> tabla ALGoritmo ==================================================================================================
        llaveAlgoritmo = list(mmuAlg.getState().keys())
        llaveAlgoritmo.sort()
        if paginaAlgoritmo != 0:
            if (sldrAlg.val==1):
                llaveAlgoritmo = llaveAlgoritmo[-20:]
            elif len(llaveAlgoritmo)>paginaAlgoritmo*20:
                llaveAlgoritmo = llaveAlgoritmo[paginaAlgoritmo*20:20*(paginaAlgoritmo+1)]
            else:
                llaveAlgoritmo = llaveAlgoritmo[-20:]
        else:
            llaveAlgoritmo = llaveAlgoritmo[:20]

        cellsAlgText = [mmuAlg.getState().get(x) for x in llaveAlgoritmo]
        cellAlgColours = [[colores[0 if x==0 else int(mmuAlg.getState().get(x)[1])] for i in range(8)] for x in llaveAlgoritmo]
        mmuAlgTable = ax2.table(cellText=cellsAlgText, colLabels=columnas_MMU, loc='bottom',bbox=[0, -0.7, 0.9, 1.2], cellColours=cellAlgColours)
        mmuAlgTable.auto_set_font_size(False)
        mmuAlgTable.set_fontsize(8)



        # TABLAS DE INFORMACION ========================================================================================================
        
        # info OPT
        dataOptText = get_datos(mmuOpt)

        dataOptTable = ax3.table(cellText=[dataOptText[:2]], colLabels=columnnas_info1, loc='center', bbox=[0.25, 0.3, 0.5, 0.15], cellLoc='center')
        dataOptTable.auto_set_font_size(False)
        dataOptTable.set_fontsize(8)

        dataOptTable = ax3.table(cellText=[dataOptText[2:6]], colLabels=columnnas_info2, loc='center', bbox=[0.25, 0.1, 0.5, 0.15], cellLoc='center')
        dataOptTable.auto_set_font_size(False)
        dataOptTable.set_fontsize(8)

        dataOptTable = ax3.table(cellText=[dataOptText[6:]], colLabels=columnnas_info3, loc='center', bbox=[0.1, -0.1, 0.8, 0.15], cellLoc='center')
        dataOptTable.auto_set_font_size(False)
        dataOptTable.set_fontsize(7)

        # info ALG
        dataAlgText = get_datos(mmuAlg)

        dataAlgTable = ax4.table(cellText=[dataAlgText[:2]], colLabels=columnnas_info1, loc='center', bbox=[0.25, 0.3, 0.5, 0.15], cellLoc='center')
        dataAlgTable.auto_set_font_size(False)
        dataAlgTable.set_fontsize(8)

        dataAlgTable = ax4.table(cellText=[dataAlgText[2:6]], colLabels=columnnas_info2, loc='center', bbox=[0.25, 0.1, 0.5, 0.15], cellLoc='center')
        dataAlgTable.auto_set_font_size(False)
        dataAlgTable.set_fontsize(8)

        dataAlgTable = ax4.table(cellText=[dataAlgText[6:]], colLabels=columnnas_info3, loc='center', bbox=[0.1, -0.1, 0.8, 0.15], cellLoc='center')
        dataAlgTable.auto_set_font_size(False)
        dataAlgTable.set_fontsize(7)


        plt.pause(0.0000000001)
        

        if(not callMemoria.isEmpty()):
            # cargador ram
            ramOptTable.remove()
            ramAlgTable.remove()
            
            # tablas de procesos
            mmuOptTable.remove()
            mmuAlgTable.remove()

            # cajas de info
            dataOptTable.remove()    
            dataAlgTable.remove()    

        # proceso actual terminado?
        if(not callMemoria.isIn(ptr_actual)):
            killproceso(ptr_actual, mmuOpt, mmuAlg)

    
        # Se terminaron todos los procesos?
        if(callMemoria.isEmpty()):
            finish(mmuOpt, mmuAlg)
            finished = True


    plt.show()