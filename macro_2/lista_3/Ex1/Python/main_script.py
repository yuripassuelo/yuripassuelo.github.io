
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import integrate

path = r'C:\\Users\\yurim\\Desktop\\Mestrado\\2S2024\\Macroeconomia 2\\Listas\\Lista 3\\Ex1\\Python\\'

sys.path.append( path )

import functions as fc
# Parametrização

t0 = time.time()
beta  = 0.96
gamma = 2
delta = 0.05
alpha = 0.36

N     = 1000
k_max = 25

k_grid = np.linspace( 0, k_max, N)

n_grid = np.array([ 0.5, 1, 1.1 ])

M = len( n_grid )

pi = np.array( [[ 0.7, 0.2, 0.1 ],
                [ 0.2, 0.6, 0.2 ],
                [ 0.1, 0.2, 0.7 ]])


inv_pi = np.matrix( pi )**1000
inv_pi = np.array( inv_pi )[1,:]

Nbar   = np.sum( n_grid * inv_pi )

V = np.zeros( (N,M) )

V,gk,stationary_dist,w,Kd,Ea,r,excDem = fc.Model_Solution( alpha, beta, gamma, delta, n_grid, k_grid, pi, M, N, Nbar, V )
t1 = time.time()

print( t1 - t0 )

out_path = r'C:\\Users\\yurim\\Desktop\\Mestrado\\2S2024\\Macroeconomia 2\\Listas\\Lista 3\\Ex1\\Python\\figs\\'

# Plots

plt.plot( k_grid, V[:,0], label = r"$n=0.5$")
plt.plot( k_grid, V[:,1], label = r"$n=1.0$")
plt.plot( k_grid, V[:,2], label = r"$n=1.1$")
plt.xlabel(r'$V$')
plt.ylabel(r'$k$')
plt.legend()
plt.savefig( out_path+r'ValueFun_1.pdf')
plt.close() 

plt.plot( k_grid, gk[:,0], label = r"$n=0.5$")
plt.plot( k_grid, gk[:,1], label = r"$n=1.0$")
plt.plot( k_grid, gk[:,2], label = r"$n=1.1$")
plt.xlabel(r"$k'$")
plt.ylabel(r'$k$')
plt.legend()
plt.savefig( out_path+r'PolFun_1.pdf')
plt.close()

plt.plot( k_grid, stationary_dist[0,:], label = r"$n=0.5$")
plt.plot( k_grid, stationary_dist[1,:], label = r"$n=1.0$")
plt.plot( k_grid, stationary_dist[2,:], label = r"$n=1.1$")
plt.xlabel('Density')
plt.ylabel(r'$k$')
plt.legend()
plt.savefig( out_path+r'StatDistG_1.pdf')
plt.close()

plt.plot( k_grid, stationary_dist[0,:]+stationary_dist[1,:]+stationary_dist[2,:] )
plt.xlabel('Density')
plt.ylabel(r'$k$')
plt.savefig( out_path+r'StatDistT_1.pdf')
plt.close()

# Analis de desigualdade 

# - Curva de Lorenz

stat_dist_tot = stationary_dist[0,:] + stationary_dist[1,:] + stationary_dist[2,:]

y_axis = k_grid/k_max
x_axis = np.cumsum( stat_dist_tot )

plt.plot( x_axis, y_axis )
plt.plot( x_axis, x_axis )
plt.xlabel('Proporção População Acumulada')
plt.ylabel('Proporção do Capital Acumulada')
plt.savefig( out_path+r'Lorenz_1.pdf')
plt.close()

# - Calculo GINI

area = integrate.cumtrapz( y_axis, x_axis )

GINI = 1 - 2*area[len(area)-1]

