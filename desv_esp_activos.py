import numpy as np
import matplotlib.pyplot as plt
from downloadValues import download_values
#from funPortafolio import fun_portafolio

# Descarga de datos utilizando la primera versión del script (Pandas)
act1 = download_values('KO', '2015-02-18', '2016-02-18', 'd', 'history')  
act2 = download_values('HD', '2015-02-18', '2016-02-18', 'd', 'history')  
act3 = download_values('CMG', '2015-02-18', '2016-02-18', 'd', 'history')  

# Extraer arreglos de precios de cierre
precio_act1 = act1['Close'].to_numpy()  
precio_act2 = act2['Close'].to_numpy()  
precio_act3 = act3['Close'].to_numpy()  

# Calcular el retorno diario logarítmico
retorno_act1 = np.log(precio_act1[1:] / precio_act1[:-1])  
retorno_act2 = np.log(precio_act2[1:] / precio_act2[:-1])  
retorno_act3 = np.log(precio_act3[1:] / precio_act3[:-1])  

# Rango de pesos para los activos (de 0 a 1 en pasos de 0.01)
rango_pesos = np.arange(0, 1.01, 0.01)  
n_pesos = len(rango_pesos)

desviacion_estandar_portafolio = np.zeros((n_pesos, n_pesos))  
esperanza_portafolio = np.zeros((n_pesos, n_pesos))  

# Calcular iterativamente para cada combinación
for i in range(n_pesos):  
    for j in range(n_pesos):  
        peso_act1 = rango_pesos[i]  
        peso_act2 = rango_pesos[j]  
        peso_act3 = 1 - (peso_act1 + peso_act2)  
        
        # Calcular retorno simplificado
        retorno_portafolio = peso_act1 * retorno_act1 + peso_act2 * retorno_act2 + peso_act3 * retorno_act3  
        
        # ddof=1 homologa el cálculo de la desviación estándar con MATLAB
        desviacion_estandar_portafolio[i, j] = np.std(retorno_portafolio, ddof=1)  
        esperanza_portafolio[i, j] = np.mean(retorno_portafolio)  

# Graficar la frontera de Markowitz
plt.figure()
plt.plot(desviacion_estandar_portafolio, esperanza_portafolio, 'b.')  
plt.title('Frontera de Markowitz con 3 Activos')  
plt.xlabel('Desviación Estándar')  
plt.ylabel('Esperanza (Retorno Esperado)')  
plt.show()

# Guardar matrices (descomentar en caso de desear guardar estos datos en un archivo para su posterior uso)
#np.savez('frontera_markowitz.npz', 
#         desviacion_estandar_portafolio=desviacion_estandar_portafolio, 
#         esperanza_portafolio=esperanza_portafolio)  