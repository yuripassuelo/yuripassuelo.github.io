import sys
import numpy as np
from numba import njit
# Functions

@njit
def vfi(beta,gamma,theta,eta,l_grid,n_grid,k_grid,pi,N,M,L,V,r,w,eps ):
    # Função Anonuima relacionada a utilidade
    util = lambda c,l : ( (c**(1-gamma))/(1-gamma) - theta*((l**(1+eta))/(1+eta)) ) 
    # Vetores Base
    Tv = V.copy()
    gk = V.copy()
    gl = V.copy()
    # Parametros Iniciais
    dist     = 10
    iter_max = 2000
    tol      = 1e-5
    it       = 0
    # Inicia o Loop
    while dist > tol and it < iter_max:
        it = it + 1
        for i in range(0,M):
            for j in range(0,N):
                Lv = np.zeros(L)
                Lp = np.zeros(L, dtype=np.int64)
                for k in range(0,L):
                    # Calcula Consumo
                    c = ( w*l_grid[k]*n_grid[i] + (1+r)*k_grid[j] - k_grid ) * (( w*l_grid[k]*n_grid[i] + (1+r)*k_grid[j] - k_grid )>0) + eps * (( w*l_grid[k]*n_grid[i] + (1+r)*k_grid[j] - k_grid )<=0)
                    # Calcula Valor
                    value = util( c, l_grid[k] ) + beta  * V @ pi[i ,:]
                    # Pega máximo e argumento máximo
                    Lv[k] = np.max( value )
                    Lp[k] = np.argmax( value )
                # Salva Valores
                Tv[j,i] = np.max( Lv )
                pos     = np.argmax( Lv )
                gk[j,i] = k_grid[ Lp[pos] ]
                gl[j,i] = l_grid[ pos ]
        #print( "Iteração: ",it," ; Distância: ",dist )
        dist = np.max( np.abs( Tv - V) )
        V    = Tv.copy()
    return V, gk, gl



def demand_n_distr( gk, k_grid, pi, M, N ):
    # Vetor Nulo
    Va = []
    # Loop preenchimento de matrizes
    for k in range(0, M ):
        Va.append( gk[:,k][:,np.newaxis] == k_grid)
    # Convertendo para Array
    Va = np.array( Va, dtype=int  )
    # Criando Matriz M
    C = np.zeros( (N*M,N*M) )
    # Preenchendo matriz M
    for i in range(0,M):
        for j in range(0,M):
            #print( i*npo,':',(i+1)*(npo-1), '   ', j*npo,':',(j+1)*(npo-1) )
            C[ i*(N):(i+1)*(N) , j*(N):(j+1)*(N) ] = Va[i]*pi[i,j] 
    # Preenchendo Matriz M
    stat_dist = np.matrix( C )**1000
    stat_dist = np.reshape( np.array( stat_dist )[1,:], (M,N))
    # Excesso de Demanda
    # Retorna 
    return stat_dist



def Excess_Demand(alpha,beta,gamma,theta,eta,delta,l_grid,n_grid,k_grid,pi,N,M,L,V,Nbar,r,eps ):
    # Demanda de Capital
    Kd = (alpha/(r+delta))**(1/(1-alpha))*Nbar
    # Salario
    w  = (1-alpha)*(Kd/Nbar)**alpha
    # Calculo de oferta 
    V, gk, gl = vfi(beta,gamma,theta,eta,l_grid,n_grid,k_grid,pi,N,M,L,V,r,w,eps )
    stat_dist = demand_n_distr( gk, k_grid, pi, M, N )
    # Capital Agregado
    Ks        = np.sum( gk * np.transpose( stat_dist ) )
    # Trabalho Agregado
    Ls        = np.sum( gl * np.transpose( stat_dist ) * n_grid )
    # Excesso de Demanda
    excDem    = ((Ks/Ls) - Kd)/(((Ks/Ls) + Kd) / 2)
    # Retorna Valores
    return excDem, V, gk, gl, stat_dist, w, Kd, Ks, Ls



def Model_Solution( alpha,beta,gamma,theta,eta,delta,l_grid,n_grid,k_grid,pi,N,M,L,V,Nbar,eps ):
    # Chutes Iniciais
    r0 = 0.001
    r1 = 0.09
    # Configurando Iteracoes
    max_iter_eq = 100
    toleq       = 0.01
    # Loop
    for iter in range(0,max_iter_eq):
        # Chute Medio
        rguess = (r0+r1)/2
        # Excesso de Demanda
        excDem, V, gk, gl, stat_dist, w, Kd, Ks, Ls = Excess_Demand(alpha,beta,gamma,theta,eta,delta,l_grid,n_grid,k_grid,pi,N,M,L,V,Nbar,rguess,eps)
        # Atualização da Bisscao
        print( "Iteração: ", iter, " ; Excesso de Demanda : ", excDem )
        if abs(excDem) < toleq:
            break
        # COndicao de atualização
        if excDem < 0:
            r0 = rguess
        else:
            r1 = rguess
    r = (r0 + r1)/2
    print( r )
    # Retorna Parametros
    return excDem, V, gk, gl, stat_dist, r, w, Kd, Ks, Ls