
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import sys

path_fun = r"C:/Users/yurim/Desktop/Mestrado/2S2024/Macroeconomia 2/Listas/Lista 4/Ex2/Python/"

sys.path.append( path_fun )

from functions import compute_policy

# Parametros
beta  = 0.98
b     = 1#0.01
pi    = 0.1
sigma = 5
r     = 0
# Grid
# Limites do Grid de Ativos
amin  = 0
amax  = 20 
# Limites do Grid de Salarios
wmin  = 0
wmax  = 30
# Tamanho dos Grids
N     = 200 # Quantidade de pontos do grid de salarios
M     = 200 # Quantidade de pontos do grid de Ativos
# Grid de Salarios
wgrid = np.linspace(wmin,wmax,N)
# Grid de Atios
agrid = np.linspace(amin,amax,M)
# Função Utilidade
u = lambda c: c**0.5
# Vetores para densidade
denN = np.zeros( N )
for j in range(1,N):
    # Assumimos que é uma Uniforme no intervalo [w_min,w_max] 
    denN[j] = 1/N
# Iteração da função Valor
# Seta vetores iniciais
V  = np.zeros( (M,N) )

# Funções Valor
Ve = V.copy() # Empregado    (Dimensão N ativos x N grid salario )
Vu = np.zeros( M )# Desempregado (Dimensão N ativos )

TVe = V.copy() # Operador do Empregado
TVu = Vu.copy() # Operador do Desempregado 

gea = V.copy() # Função politica do Capital do Empregado
gua = Vu.copy() # Função Politica do Capital do Desempregado

t0 = time.time()
Ve_1, Vu_1, gea_1, gua_1 = compute_policy(Ve,Vu,TVe,TVu,gea,gua,denN,beta,pi,N,M,b,r,wgrid,agrid)
t1 = time.time()

# Plot 3D

from matplotlib import cm
from matplotlib.ticker import LinearLocator

# Plot Função Valor do empregado
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
X1, Y1 = np.meshgrid(wgrid, agrid)
# Plot the surface.
surf = ax.plot_surface(X1, Y1, Ve_1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel(r"$w$")
ax.set_ylabel(r"$a$")
ax.set_zlabel(r"$V^e$")
plt.show()


# Plot Função Valor do empregado
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
X1, Y1 = np.meshgrid(wgrid, agrid)
# Plot the surface.
surf = ax.plot_surface(X1, Y1, Vu_1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel(r"$w$")
ax.set_ylabel(r"$a$")
ax.set_zlabel(r"$V^e$")
plt.show()

# Plot Função Politica do empregado
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
X1, Y1 = np.meshgrid(wgrid, agrid)
# Plot the surface.
surf = ax.plot_surface(X1, Y1, gea_1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel(r"$w$")
ax.set_ylabel(r"$a$")
ax.set_zlabel(r"$g_{a'}^{e}(w,a)$")
plt.show()

# Plot Função Politica do deempregado
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
X1, Y1 = np.meshgrid(wgrid, agrid)
# Plot the surface.
surf = ax.plot_surface(X1, Y1, gua_1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel(r"$w$")
ax.set_ylabel(r"$a$")
ax.set_zlabel(r"$g_{a'}^{u}(w,a)$")
plt.show()

# Salário de Reserva

plt.plot( wgrid, Ve_1[100,:] )
plt.plot( wgrid, Ve_1[10,:] )
plt.plot( wgrid, Ve_1[0,:] )
plt.plot( wgrid, Vu_1 )
plt.show()
