# ------- PSO 2 ------- #
import numpy as np
import matplotlib.pyplot as plt

# --------- Inicialización de la colonia ---------
num_pob = 500  
phi0 = 0.7  
c1 = 0.5  
c2 = 0.5  

x1p = 20 * np.random.rand(num_pob) - 10  
x1pg = 0  
x1pL = np.copy(x1p)  
#----------------------------------------------------
x2p = 20 * np.random.rand(num_pob) - 10  
x2pg = 0  
x2pL = np.copy(x2p)  
#---------------------------------------------------

fxpg = np.inf  
fxpL = np.ones(num_pob) * fxpg  

vx1 = np.zeros(num_pob)  
#----------------------------------------------------
vx2 = np.zeros(num_pob)  
#---------------------------------------------------------------

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# --------- Movimiento de la población ---------
for k in range(100):  
    # Ecuación de movimiento
    vx1 = phi0 * vx1 + c1 * np.random.rand() * (x1pL - x1p) + c2 * np.random.rand() * (x1pg - x1p)  
    x1p = vx1 + x1p  
    #--------------------------------------------------
    vx2 = phi0 * vx2 + c1 * np.random.rand() * (x2pL - x2p) + c2 * np.random.rand() * (x2pg - x2p)  
    x2p = vx2 + x2p  
    #-------------------------------------------------

    # Evaluación de la función multivariable (Booth)
    #-----------------------------------------------------
    fx = (x1p + 2 * x2p - 7)**2 + (2 * x1p + x2p - 5)**2  
    #-----------------------------------------------------
    val = np.min(fx)  
    ind = np.argmin(fx)  

    # Actualizar mejor global
    if val < fxpg:  
        fxpg = val  
        x1pg = x1p[ind]  
        #-------------------------------------------------
        x2pg = x2p[ind]  
        #-------------------------------------------------

    # Actualizar mejor local
    mejores = fx < fxpL  
    fxpL[mejores] = fx[mejores]  
    x1pL[mejores] = x1p[mejores]  
    #-------------------------------------------------
    x2pL[mejores] = x2p[mejores]  
    #-------------------------------------------------

    # Sección de gráfica 3D
    if k == 0:  
        X, Y = np.meshgrid(np.arange(-10, 10.1, 0.5), np.arange(-10, 10.1, 0.5))  
        Z = (X + 2*Y - 7)**2 + (2*X + Y - 5)**2  
        ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')  
        ax.set_xlim([-10, 10])  
        ax.set_ylim([-10, 10])  
        ax.set_zlim([0, np.max(Z)])  
        
        h1, = ax.plot(x1p, x2p, fx, 'or', markerfacecolor='r')  
        
        ax.set_xlabel('x')  
        ax.set_ylabel('y')  
        ax.set_zlabel('z')  
    else:
        h1.set_data_3d(x1p, x2p, fx)  
        
    ax.set_title(rf'$f(x,y)=(x_1+2x_2-7)^2 + (2x_1+x_2-5)^2, \quad iteración: {k+1}$', fontsize=14)  
    plt.pause(0.05)  

plt.ioff()
plt.show()
print(f"x1pg = {x1pg:.4f}, x2pg = {x2pg:.4f}, fxpg = {fxpg:.4f}")  