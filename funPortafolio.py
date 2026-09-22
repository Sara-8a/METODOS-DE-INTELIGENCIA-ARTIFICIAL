import numpy as np

def fun_portafolio(Precios, part):
    # Precios: Matriz numpy de (n_dias, n_activos)
    # part: Matriz numpy de (n_particulas, n_activos) donde la suma de cada fila es 1
    
    # Cálculo de los retornos simples: (Pt - Pt-1) / Pt-1
    rend = (Precios[1:] - Precios[:-1]) / Precios[:-1] #
    
    # Media y matriz de covarianza de los retornos
    esperanza = np.mean(rend, axis=0) #
    covar = np.cov(rend, rowvar=False)  
    
    # Rendimiento esperado del portafolio (Producto punto vectorizado)
    esperanzaport = np.dot(part, esperanza)  
    
    # Cálculo iterativo del riesgo (varianza) para cada fila de ponderaciones
    npart = part.shape[0]  
    riesgoport = np.zeros(npart)
    
    for k in range(npart):  
        # Equivalente a part(k,:) * covar * part(k,:)'
        riesgoport[k] = np.dot(part[k, :], np.dot(covar, part[k, :].T))  
        
    desvestport = np.sqrt(riesgoport)  
    
    return esperanzaport, desvestport