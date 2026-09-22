# ------- PSO 1 ------- #
import numpy as np
import matplotlib.pyplot as plt

# --------- Gráfica de la función ---------
x = np.arange(-10, 10.01, 0.01)  
y = 10 + x**2 - 15 * np.cos(5 * x)  
#y = -20*np.exp(-0.2*np.sqrt(x**2)) - np.exp(np.cos(2*np.pi*x)) + 20 + np.exp(1)

# --------- Inicialización de la colonia ---------
num_pob = 500  
c1 = 0.5  
c2 = 0.5  
phi0 = 0.7  # Inercia  

x1p = (10 - (-10)) * np.random.rand(num_pob) - 10  
x1pg = 0  
x1pL = np.copy(x1p)  

fxpg = np.inf  
fxpL = np.ones(num_pob) * fxpg  
vx1 = np.zeros(num_pob)  

# Activar modo interactivo para gráfica en vivo
plt.ion() 
fig, ax = plt.subplots()

# --------- Movimiento de la población ---------
for k in range(100):  
    # Ecuación de movimiento
    vx1 = phi0 * vx1 + c1 * np.random.rand() * (x1pL - x1p) + c2 * np.random.rand() * (x1pg - x1p)  
    x1p = vx1 + x1p  

    # Evaluación del desempeño de cada partícula
    fx = 10 + x1p**2 - 15 * np.cos(5 * x1p)  
    #fx = -20*np.exp(-0.2*np.sqrt(x1p**2)) - np.exp(np.cos(2*np.pi*x1p)) + 20 + np.exp(1)
    val = np.min(fx)  
    ind = np.argmin(fx)  

    # Actualizar mejor global
    if val < fxpg:  
        fxpg = val  
        x1pg = x1p[ind]  

    # Actualizar mejor local (Vectorizado en lugar del 'for p=1:np')
    mejores = fx < fxpL  
    fxpL[mejores] = fx[mejores]  
    x1pL[mejores] = x1p[mejores]  

    # Graficar valores
    ax.clear()  
    ax.plot(x, y, 'b-')  
    ax.plot(x1p, fx, 'r*')  
    ax.plot(x1pg, fxpg, 'gp')  
    ax.set_xlim([-10, 10])  
    ax.set_ylim([-10, 120])  
    ax.set_title(f'x1pg = {x1pg:.4f}, fxpg = {fxpg:.4f}, iteración: {k+1}')  
    plt.pause(0.05)  

plt.ioff()
plt.show()