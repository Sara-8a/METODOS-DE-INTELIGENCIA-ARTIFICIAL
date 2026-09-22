# ----- ALGORITMO GENÉTICO 2 ----- #
import numpy as np
import matplotlib.pyplot as plt

# Limpieza de entorno manejada por la sesión de Python

# --------- Inicialización de la población ---------
# Definición de límites y tamaño de paso
xmin = -100 # límite inferior
xmax = 100 # límite superior
tpaso = 0.01 # tamaño de paso

# Cálculo de elementos y número de bits
elementos = (xmax - xmin) / tpaso + 1 # número de elementos
nbits = int(np.ceil(np.log2(elementos))) # número de bits
num_poblacion = 512 # tamaño de la población

# Padres enteros a padres reales
# Generar población inicial de enteros
x1 = np.random.randint(0, 2**nbits, num_poblacion)
# Transformar enteros a reales
x1real = (xmax - xmin) * x1 / (2**nbits - 1) + xmin

# Matriz para almacenar el promedio del desempeño
yprom = np.zeros(100)

# --------- Iniciar número de generaciones ---------
# Número de generaciones: 100
for i in range(100):
    
    # Evaluar los padres en la función objetivo
    y = -(x1real + 41.125)**2 + 200 # Función de fitness
    yprom[i] = np.mean(y)
    
    # Ordenar los cromosomas (de menor a mayor desempeño)
    indices_ordenados = np.argsort(y)
    x1_ordenado = x1[indices_ordenados]
    x1real_ordenado = x1real[indices_ordenados]
    
    # Seleccionar la mitad superior (los mejores)
    mejores_x1 = x1_ordenado[num_poblacion // 2 :]
    mejores_x1real = x1real_ordenado[num_poblacion // 2 :]
    
    # Convertir padres enteros seleccionados a binario
    padresbin = np.zeros((num_poblacion // 2, nbits), dtype=int)
    for idx, val in enumerate(mejores_x1):
        for j in range(nbits):
            padresbin[idx, j] = (int(val) >> j) & 1

    # --------- Cruzamiento ---------
    hijobin = np.zeros_like(padresbin)
    
    for k in range(num_poblacion // 4):
        # Elegir un punto de cruce aleatorio
        n = np.random.randint(1, nbits - 1)
        
        padre1 = padresbin[2*k]
        padre2 = padresbin[2*k + 1]
        
        # Intercambiar información para crear hijos binarios
        hijobin[2*k] = np.concatenate((padre1[:n], padre2[n:]))
        hijobin[2*k + 1] = np.concatenate((padre2[:n], padre1[n:]))

    # --------- Mutación ---------
    p = np.random.rand() # definimos un número aleatorio entre 0 y 1
    if p > 0.90: # Condición para mutación (10%)
        # Seleccionar aleatoriamente una posición y un bit
        nhijo = np.random.randint(0, num_poblacion // 2)
        nbit = np.random.randint(0, nbits)
        
        # Invertir el valor del bit
        hijobin[nhijo, nbit] = 1 - hijobin[nhijo, nbit]

    # --------- Reiniciar proceso (Decodificación) ---------
    # Convertir hijo binario a entero
    hijoent = np.zeros(num_poblacion // 2)
    for idx in range(num_poblacion // 2):
        val = 0
        for j in range(nbits):
            val += hijobin[idx, j] * (2 ** j)
        hijoent[idx] = val
        
    # Convertir hijo entero a real usando la función de conversión
    hijoreal = (xmax - xmin) * hijoent / (2**nbits - 1) + xmin #
    
    # Actualizar matrices pasándolo de hijo a padre
    x1 = np.concatenate((mejores_x1, hijoent))
    x1real = np.concatenate((mejores_x1real, hijoreal))

# --------- Mostrar resultado en pantalla ---------
# Graficar el promedio
plt.plot(yprom, linewidth=2)
plt.xlabel("Generaciones") 
plt.ylabel("Desempeño promedio (y)")
plt.title("Evolución del algoritmo genético")
plt.grid(True)
plt.show()

# Evaluar la función final para encontrar el máximo
y = -(x1real + 41.125)**2 + 200 #
val = np.max(y)
ind = np.argmax(y)

print(f"Resultado: x1= {x1real[ind]:.4f},  y= {val:.4f}")