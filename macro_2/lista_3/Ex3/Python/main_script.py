
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import integrate
from numba import njit

path = r'C:\\Users\\yurim\\Desktop\\Mestrado\\2S2024\\Macroeconomia 2\\Listas\\Lista 3\\Ex3\\Python\\'

sys.path.append( path )

import functions as fc
# Parametrização


beta  = 0.96
gamma = 2
delta = 0.05
alpha = 0.36
G     = 0.1 # Gasto Exógeno

N     = 1000
k_max = 25


k_grid = np.linspace( 0, k_max, N)

n_grid = np.array([ 0.5, 1, 1.1 ])

M      = len( n_grid )

pi = np.array( [[ 0.7, 0.2, 0.1 ],
                [ 0.2, 0.6, 0.2 ],
                [ 0.1, 0.2, 0.7 ]])


inv_pi = np.matrix( pi )**1000
inv_pi = np.array( inv_pi )[1,:]

Nbar   = np.sum( n_grid * inv_pi )

V  = np.zeros( (N,M) )

t0 = time.time()
V1,gk1 = fc.vfi( beta,gamma,n_grid,k_grid,pi,N,M,V,0.05,1,0.05,0.0,eps = sys.float_info.epsilon )
t1 = time.time()
print( t1- t0)

# 
t0 = time.time()
stat_dist1 = fc.demand_n_distr( gk1, k_grid, pi, M, N )
t1 = time.time()
print( t1- t0)


t0 = time.time()
excDemf, govBalf, Vf, gkf, stat_distf, wf, kdf =  fc.Excess_Demand( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,0.05,V, 0.05,0.05, G, eps = sys.float_info.epsilon )
t1 = time.time()

# Taxação Sob Capital

t0 = time.time()
Vk,gkk,stat_distk,wk,kdk,rk,tk,excDemk,govBalk = fc.Model_Solution_Gov( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,G,sys.float_info.epsilon,"k" )
t1 = time.time()

# Taxação Sob Trabalho

t0 = time.time()
Vl,gkl,stat_distl,wl,kdl,rl,tl,excDeml,govBall = fc.Model_Solution_Gov( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,G,sys.float_info.epsilon,"l" )
t1 = time.time()

# Taxação Sob Ambos

t0 = time.time()
Vb,gkb,stat_distb,wb,kdb,rb,tb,excDemb,govBalb = fc.Model_Solution_Gov( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,G,sys.float_info.epsilon,"b" )
t1 = time.time()

# Plots

path_fig = r"C:\\Users\\yurim\\Desktop\\Mestrado\\2S2024\\Macroeconomia 2\\Listas\\Lista 3\\Ex2_v2\\Python\\figs\\"

# Funções Valores

fig, axs = plt.subplots(1,3,sharey=True)

axs[0].plot( k_grid, Vk[:,0], label = r"$n=0.5$" )
axs[0].plot( k_grid, Vk[:,1], label = r"$n=1.0$" )
axs[0].plot( k_grid, Vk[:,2], label = r"$n=1.1$" )
axs[0].legend(loc = 'lower right')
axs[0].set_title( "Tax on Capital")
axs[1].plot( k_grid, Vl[:,0], label = r"$n=0.5$" )
axs[1].plot( k_grid, Vl[:,1], label = r"$n=1.0$" )
axs[1].plot( k_grid, Vl[:,2], label = r"$n=1.1$" )
axs[1].legend(loc = 'lower right')
axs[1].set_title( "Tax on Labour")
axs[2].plot( k_grid, Vb[:,0], label = r"$n=0.5$" )
axs[2].plot( k_grid, Vb[:,1], label = r"$n=1.0$" )
axs[2].plot( k_grid, Vb[:,2], label = r"$n=1.1$" )
axs[2].legend(loc = 'lower right')
axs[2].set_title( "Tax on Both" )
plt.legend( loc = 'lower right')
plt.savefig(path_fig+r'plot_V.pdf')
plt.show()
plt.close()

# Funlões Politicas

fig, axs = plt.subplots(1,3,sharey=True)

axs[0].plot( k_grid, gkk[:,0], label = r"$n=0.5$" )
axs[0].plot( k_grid, gkk[:,1], label = r"$n=1.0$" )
axs[0].plot( k_grid, gkk[:,2], label = r"$n=1.1$" )
axs[0].legend(loc = 'lower right')
axs[0].set_title( "Tax on Capital")
axs[1].plot( k_grid, gkl[:,0], label = r"$n=0.5$" )
axs[1].plot( k_grid, gkl[:,1], label = r"$n=1.0$" )
axs[1].plot( k_grid, gkl[:,2], label = r"$n=1.1$" )
axs[1].legend(loc = 'lower right')
axs[1].set_title( "Tax on Labour")
axs[2].plot( k_grid, gkb[:,0], label = r"$n=0.5$" )
axs[2].plot( k_grid, gkb[:,1], label = r"$n=1.0$" )
axs[2].plot( k_grid, gkb[:,2], label = r"$n=1.1$" )
axs[2].legend(loc = 'lower right')
axs[2].set_title( "Tax on Both" )
plt.legend( loc = 'lower right')
plt.savefig(path_fig+r'plot_pol.pdf')
plt.show()
plt.close()

# Distribuições Estacionarias

fig, axs = plt.subplots(1,3,sharey=True)

axs[0].plot( k_grid, stat_distk.T[:,0], label = r"$n=0.5$" )
axs[0].plot( k_grid, stat_distk.T[:,1], label = r"$n=1.0$" )
axs[0].plot( k_grid, stat_distk.T[:,2], label = r"$n=1.1$" )
axs[0].legend(loc = 'upper right')
axs[0].set_title( "Tax on Capital")
axs[1].plot( k_grid, stat_distl.T[:,0], label = r"$n=0.5$" )
axs[1].plot( k_grid, stat_distl.T[:,1], label = r"$n=1.0$" )
axs[1].plot( k_grid, stat_distl.T[:,2], label = r"$n=1.1$" )
axs[1].legend(loc = 'upper right')
axs[1].set_title( "Tax on Labour")
axs[2].plot( k_grid, stat_distb.T[:,0], label = r"$n=0.5$" )
axs[2].plot( k_grid, stat_distb.T[:,1], label = r"$n=1.0$" )
axs[2].plot( k_grid, stat_distb.T[:,2], label = r"$n=1.1$" )
axs[2].legend(loc = 'upper right')
axs[2].set_title( "Tax on Both")
plt.savefig(path_fig+r'plot_dens.pdf')
plt.show()
plt.close()