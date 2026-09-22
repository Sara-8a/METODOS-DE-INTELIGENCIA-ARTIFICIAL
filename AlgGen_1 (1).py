# ----- ALGORITMO GENÉTICO 1 ----- #
import numpy as np
import matplotlib.pyplot as plt

# Inicialización de la población
nbits = 8
pobladores = 80

# Población inicial (numpy incluye el límite inferior pero excluye el superior, por eso usamos 256)
xpadres = np.random.randint(0, 256, pobladores)
yprom = np.zeros(20)

# Número de generaciones: 20
for n in range(20):
    
    # --------- Evaluar y ordenar y = f(x) ---------
    # Función de ajuste: y = -(x-20.373)^2+100 
    y = -(xpadres - 20.373)**2 + 100
    yprom[n] = np.mean(y)
    
    # Crear los cromosomas (ordenando de menor a mayor según y)
    indices_ordenados = np.argsort(y)
    xpadres_ordenados = xpadres[indices_ordenados]
    
    # Nos quedamos con la mitad superior (los mejores evaluados)
    mejores_padres = xpadres_ordenados[pobladores // 2 :] #aqui nos quedamos
    
    # --------- Decodificar a binario ---------
    # Convertimos los números decimales a binario (8 columnas)
    padresbin = np.zeros((pobladores // 2, nbits), dtype=int)
    for i, val in enumerate(mejores_padres):
        for j in range(nbits):
            padresbin[i, j] = (int(val) >> j) & 1

    # --------- Cruzamiento ---------
    hijobin = np.zeros_like(padresbin)
    
    for k in range(pobladores // 4):
        # m = valores aleatorios entre 1 y nbits-2
        m = np.random.randint(1, nbits - 1)
        
        # Cruzamiento intercalando partes de la cadena
        padre1 = padresbin[2*k]
        padre2 = padresbin[2*k + 1]
        
        hijobin[2*k] = np.concatenate((padre1[:m], padre2[m:]))
        hijobin[2*k + 1] = np.concatenate((padre2[:m], padre1[m:]))
        
    # --------- Mutación ---------
    p = np.random.rand()
    if p >= 0.8:
        # Seleccionar aleatoriamente una posición y un bit
        nhijo = np.random.randint(0, pobladores // 2)
        nbit = np.random.randint(0, nbits)
        
        # Invertir bit: si es 1 cambia a 0, y viceversa
        hijobin[nhijo, nbit] = 1 - hijobin[nhijo, nbit]

    # --------- Reiniciar proceso ---------
    # Cambiar de binario a decimal 
    hijodec = np.zeros(pobladores // 2)
    for i in range(pobladores // 2):
        val = 0
        for j in range(nbits):
            val += hijobin[i, j] * (2 ** j)
        hijodec[i] = val
        
    # Anexar el nuevo hijo decimal a los xpadres
    xpadres = np.concatenate((mejores_padres, hijodec))

# --------- Mostrar solución en pantalla ---------
# Evaluar la función final
y = -(xpadres - 20.373)**2 + 100

# Graficar el promedio
plt.plot(yprom,linewidth=2)
plt.title('Desempeño Promedio por Generación')
plt.xlabel('Generación')
plt.ylabel('Promedio y')

plt.grid(True)
plt.show()

# Ubicar el máximo
val = np.max(y)
ind = np.argmax(y)

print(f"Resultado: x={xpadres[ind]}, y={val:.4f}")
