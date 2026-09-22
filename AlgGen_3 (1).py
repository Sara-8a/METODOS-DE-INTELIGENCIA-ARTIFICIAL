# ----- ALGORITMO GENÉTICO 3 ----- #
import numpy as np
import matplotlib.pyplot as plt

# --------- Inicialización de la población ---------
# Definición de límites y tamaño de paso para ambas variables
xmin1, xmax1, tpaso1 = -5.12, 5.12, 0.01  
xmin2, xmax2, tpaso2 = -5.12, 5.12, 0.01  

# Cálculo de elementos y número de bits
elementos1 = (xmax1 - xmin1) / tpaso1 + 1  
elementos2 = (xmax2 - xmin2) / tpaso2 + 1  

nbits1 = int(np.ceil(np.log2(elementos1)))  
nbits2 = int(np.ceil(np.log2(elementos2)))  

# Número de población
num_poblacion = 256  

# Generar población inicial de enteros aleatorios
x1 = np.random.randint(0, 2**nbits1, num_poblacion)  
x2 = np.random.randint(0, 2**nbits2, num_poblacion)  

# Transformar enteros a reales
x1real = (xmax1 - xmin1) * x1 / (2**nbits1 - 1) + xmin1  
x2real = (xmax2 - xmin2) * x2 / (2**nbits2 - 1) + xmin2  

# Matriz para almacenar el promedio
yprom = np.zeros(100)  

# --------- Iniciar número de generaciones ---------
for i in range(100):  
    
    # Evaluar la función de Rastrigin
    y = 20 + x1real**2 + x2real**2 - 10*np.cos(2*np.pi*x1real) - 10*np.cos(2*np.pi*x2real)  
    yprom[i] = np.mean(y)  
    
    # Ordenar de forma ascendente y tomar la mejor mitad
    indices_ordenados = np.argsort(y)  
    
    mejores_x1 = x1[indices_ordenados][num_poblacion // 2 :]  
    mejores_x1real = x1real[indices_ordenados][num_poblacion // 2 :]  
    
    mejores_x2 = x2[indices_ordenados][num_poblacion // 2 :]  
    mejores_x2real = x2real[indices_ordenados][num_poblacion // 2 :]  
    
    # Convertir a binario
    padresbin1 = np.zeros((num_poblacion // 2, nbits1), dtype=int)  
    padresbin2 = np.zeros((num_poblacion // 2, nbits2), dtype=int)  
    
    for idx in range(num_poblacion // 2):
        for j in range(nbits1):
            padresbin1[idx, j] = (int(mejores_x1[idx]) >> j) & 1  
        for j in range(nbits2):
            padresbin2[idx, j] = (int(mejores_x2[idx]) >> j) & 1  

    # --------- Cruzamiento ---------
    hijobin1 = np.zeros_like(padresbin1)  
    hijobin2 = np.zeros_like(padresbin2)  
    
    for k in range(num_poblacion // 4):  
        # Cruce para la variable 1
        n1 = np.random.randint(1, nbits1 - 1)  
        p1_v1, p2_v1 = padresbin1[2*k], padresbin1[2*k + 1]  
        hijobin1[2*k] = np.concatenate((p1_v1[:n1], p2_v1[n1:]))  
        hijobin1[2*k + 1] = np.concatenate((p2_v1[:n1], p1_v1[n1:]))  
        
        # Cruce para la variable 2
        n2 = np.random.randint(1, nbits2 - 1)  
        p1_v2, p2_v2 = padresbin2[2*k], padresbin2[2*k + 1]  
        hijobin2[2*k] = np.concatenate((p1_v2[:n2], p2_v2[n2:]))  
        hijobin2[2*k + 1] = np.concatenate((p2_v2[:n2], p1_v2[n2:]))  

    # --------- Mutación ---------
    # Mutación variable 1
    if np.random.rand() > 0.90:  
        nhijo = np.random.randint(0, num_poblacion // 2)  
        bit = np.random.randint(0, nbits1)  
        hijobin1[nhijo, bit] = 1 - hijobin1[nhijo, bit]  

    # Mutación variable 2
    if np.random.rand() > 0.90:  
        nhijo = np.random.randint(0, num_poblacion // 2)  
        bit = np.random.randint(0, nbits2)  
        hijobin2[nhijo, bit] = 1 - hijobin2[nhijo, bit]  

    # --------- Reiniciar proceso (Decodificación) ---------
    hijoent1 = np.zeros(num_poblacion // 2)  
    hijoent2 = np.zeros(num_poblacion // 2)  
    
    for idx in range(num_poblacion // 2):
        val1 = val2 = 0
        for j in range(nbits1):
            val1 += hijobin1[idx, j] * (2 ** j)  
        for j in range(nbits2):
            val2 += hijobin2[idx, j] * (2 ** j)  
        hijoent1[idx], hijoent2[idx] = val1, val2  
        
    hijoreal1 = (xmax1 - xmin1) * hijoent1 / (2**nbits1 - 1) + xmin1  
    hijoreal2 = (xmax2 - xmin2) * hijoent2 / (2**nbits2 - 1) + xmin2  
    
    # Actualizar matrices
    x1 = np.concatenate((mejores_x1, hijoent1))  
    x1real = np.concatenate((mejores_x1real, hijoreal1))  
    x2 = np.concatenate((mejores_x2, hijoent2))  
    x2real = np.concatenate((mejores_x2real, hijoreal2))  

# --------- Mostrar resultado ---------
plt.plot(yprom, linewidth=2)
plt.xlabel("Generaciones")
plt.ylabel("Desempeño promedio")
plt.title("GA Multivariable - Función Rastrigin")
plt.grid(True)
plt.show()

# Evaluar función final y encontrar máximo
y = 20 + x1real**2 + x2real**2 - 10*np.cos(2*np.pi*x1real) - 10*np.cos(2*np.pi*x2real)  
val = np.max(y)  
ind = np.argmax(y)  

print(f"Results: x1= {x1real[ind]:.4f} x2= {x2real[ind]:.4f}  y= {val:.4f}")  

