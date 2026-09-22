import numpy as np
import matplotlib.pyplot as plt
from downloadValues import download_values
from datetime import datetime, timedelta

# Asumimos que el archivo de la primera versión se guardó como 'descargas.py'
# from descargas import download_values

# --------- Obtención de los datos ---------
# Cálculo dinámico de fechas: hoy y hace 2 años (365 * 2)
hoy = datetime.today().strftime('%Y-%m-%d') #
inicio = (datetime.today() - timedelta(days=2*365)).strftime('%Y-%m-%d') #

# Llamada a la función (usando la versión con Pandas)
data = download_values('IVVPESO.MX', inicio, hoy, 'd', 'history') #

# Convertir la columna de precios de cierre a un arreglo de NumPy para cálculo vectorizado
precios = data['Close'].to_numpy()  

# --------- Algoritmo de trading basado en media móvil ---------
npm = 10 # Número de días para la media móvil  
n_dias = len(precios)

# Se inicializan con +1 para alojar la actualización del día siguiente dentro del ciclo
cap = np.ones(n_dias + 1) * 1000000 # Capital inicial de $1,000,000  
nac = np.zeros(n_dias + 1) # Número de acciones disponibles al inicio  
com = 0.0025 # Comisión por operación (0.25%)  

# Matriz para almacenar la media móvil (se rellena con NaN para los primeros días)
pm = np.full(n_dias, np.nan)

# Simulación del algoritmo
for t in range(n_dias - npm + 1):  
    # Índice actual (0-based) ajustado para la ventana de días
    idx = npm + t - 1 
    
    # Calculando la media móvil del periodo de 25 días
    pm[idx] = np.mean(precios[t : t + npm])  
    
    if pm[idx] < precios[idx]:  
        # Comprar, si la media móvil es menor que el precio actual  
        u = np.floor(cap[idx] / ((1 + com) * precios[idx]))  
    else:
        # Vender, si la media móvil es mayor que el precio actual  
        u = -nac[idx]  
        
    # Actualización para el día siguiente
    nac[idx + 1] = nac[idx] + u  
    cap[idx + 1] = cap[idx] - precios[idx] * u - com * precios[idx] * abs(u)  

# --------- Visualización de resultados ---------
T = np.arange(1, n_dias + 1)  

plt.figure(figsize=(10, 12))

# Gráfica 1: Precios y Media Móvil
plt.subplot(4, 1, 1)  
plt.plot(T, precios, 'b-', label='Precio')  
plt.plot(T, pm, 'r--', label='Media')  
plt.title(f'Media móvil a {npm} días')  
plt.xlabel('# días')  
plt.ylabel('precio')  
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') # Equivalente a NorthEastOutside  
plt.grid(True)  

# Gráfica 2: Número de acciones
plt.subplot(4, 1, 2)  
# Usamos [:-1] para cortar el elemento extra y cuadrar el tamaño con T
plt.plot(T, nac[:-1], 'b-', label='# acciones')  
plt.xlabel('# días')  
plt.ylabel('# acciones')  
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Gráfica 3: Capital disponible
plt.subplot(4, 1, 3)  
plt.plot(T, cap[:-1], 'b-', label='capital')  
plt.xlabel('# días')  
plt.ylabel('$')  
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Gráfica 4: Rendimiento total (%)
plt.subplot(4, 1, 4)  
# Cálculo vectorizado idéntico a precios.*nac
rendimiento = 100 * (cap[:-1] + precios * nac[:-1] - cap[0]) / cap[0]  
plt.plot(T, rendimiento, 'b-', label='Total')  
plt.xlabel('# días')  
plt.ylabel('rendimiento (%)')  
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

plt.tight_layout()
plt.show()