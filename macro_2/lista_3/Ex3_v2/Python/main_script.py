
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import integrate
from numba import njit

path = r'C:\\Users\\yurim\\Desktop\\Mestrado\\2S2024\\Macroeconomia 2\\Listas\\Lista 3\\Ex3_v2\\Python\\'

sys.path.append( path )


import functions as fc

# Parametrização
beta  = 0.96
gamma = 2
delta = 0.05
alpha = 0.36
theta = 1
eta   = 1.5 
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

# Função Política
t0 = time.time()
V1,gk1 = fc.vfi( beta,gamma,n_grid,k_grid,pi,N,M,V,0.05,1,0.05,0.0,eps = sys.float_info.epsilon )
t1 = time.time()
print( t1- t0)

# Demanda e Distr Estacionaria
t0 = time.time()
stat_dist1 = fc.demand_n_distr( gk1, k_grid, pi, M, N )
t1 = time.time()
print( t1- t0)

#
t0 = time.time()
excDem1, govBal1, V1, gk1, stat_dist1, w1, kd1, Ks1, Ls1 = fc.Excess_Demand( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,0.05,V,0.05,0.0,G,eps = sys.float_info.epsilon )
t1 = time.time()


# Solução
t0 = time.time()
V1,gk1,stat_dist1,w1,kd1,r1,tau1,excDem1,govBal1 = fc.Model_Solution( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,"k",G,eps = sys.float_info.epsilon )
t1 = time.time()
print( t1- t0)
