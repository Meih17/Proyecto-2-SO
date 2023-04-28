import random
import csv

def matriz_a_csv(matriz, nombre_archivo):
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor_csv = csv.writer(archivo, delimiter=',')
        for fila in matriz:
            escritor_csv.writerow(fila)


def generar_operaciones(n=16, P=10):
    full_instructions = []
    for i in range(P):
        instructions = []
        num_news  = int(n*0.2)+1
        news = [f'new({i},{random.randint(100,4096)})' for i in range(1,num_news)]
        kills = list(f'kill({i})' for i in range(1,num_news))
        uses = [f'use({random.randint(1,num_news-1)})' for i in range(int(n*0.5))]
        deletes = [f'delete({random.randint(1,num_news-1)})' for i in range(int(n*0.1))]

        # Fusionar las listas
        instructions.extend(news)
        uses.extend(deletes)
        random.shuffle(uses)
        instructions.extend(uses)
        instructions.extend(kills)
        full_instructions.append(instructions)

    # Crear el archivo CSV 
    matriz_a_csv(full_instructions, "pruebas-generadas.csv")

generar_operaciones(20, 5)
