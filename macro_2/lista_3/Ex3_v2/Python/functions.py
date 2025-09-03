import sys
import numpy as np
from numba import njit

# Functions

@njit
def vfi( beta,gamma,n_grid,k_grid,pi,N,M,V,r,w,tau1,tau2,eps ):

    util = lambda c : (c**(1-gamma))/(1-gamma)

    Tv = V.copy()
    gk = V.copy()
    gl = V.copy()

    # Parametros Iniciais
    dist     = 10
    iter_max = 2000
    tol      = 1e-5
    it       = 0

    while dist > tol and it < iter_max:
        it = it + 1
        for i in range(0,M):
            for j in range(0,N):
                    
                c = ( (1-tau1)*w*n_grid[i] + (1+r*(1-tau2))*k_grid[j] - k_grid ) * (( (1-tau1)*w*n_grid[i] + (1+r*(1-tau2))*k_grid[j] - k_grid )>0) + eps * (( (1-tau1)*w*n_grid[i] + (1+r*(1-tau2))*k_grid[j] - k_grid )<=0)

                value = util( c ) + beta  * V @ pi[i ,:]

                Tv[j,i] = np.max( value )
                pol     = np.argmax( value )
                gk[j,i] = k_grid[ pol ]
        dist = np.max( np.abs( Tv - V) )
        #print( it, ' - ',dist )
        V    = Tv.copy()
    return V, gk

# Original
def demand_n_distr( gk, k_grid, pi, M, N ):
    # Vetor Nulo
    Va = []
    # Loop preenchimento de matrizes
    for k in range(0, M ):
        Va.append( gk[:,k][:,np.newaxis] == k_grid)
    # Convertendo para Array
    #Va = np.array( Va, dtype=int  )
    Va = np.array( Va*1 )
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


def Excess_Demand( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,r,V,tau1,tau2,G,eps ):

    # Demanda de Capital
    kd = ((r+delta)/alpha)**(1/(alpha-1))
    # Salario
    w  = (1-alpha)*(kd)**alpha
    # Calculo de oferta 
    V, gk = vfi(beta,gamma,n_grid,k_grid,pi,N,M,V,r,w,tau1,tau2,eps)
    stat_dist = demand_n_distr( gk, k_grid, pi, M, N )
    # Oferta de Capital e Trabalho
    Ks = np.sum( gk * np.transpose( stat_dist ) )
    Ls = np.sum( ( np.transpose( stat_dist ) ) @ n_grid )
    #Ea        = np.sum( gk * np.transpose( stat_dist ) )
    excDem    = ((Ks/Ls) - kd)/(((Ks/Ls) + kd) / 2)
    # Analisa Resultado do Governo
    govBal    = r*tau1*Ks + w*tau2*Ls - G
    # Retorna Valores
    return excDem, govBal, V, gk, stat_dist, w, kd, Ks, Ls


def Model_Solution( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,Tax_Opt,G,eps ):
    # Chutes Iniciais
    K0 = 10
    L0 = 1
    t0 = 0.01
    # Configurando Iteracoes
    max_iter_eq = 100
    # toleq       = 0.01
    lamb        = 0.98
    iter        = 0
    # Opções de Taxação
    if Tax_Opt == "b":
        pl = 1
        pk = 1
    elif Tax_Opt == "k":
        pl = 0
        pk = 1
    elif Tax_Opt == "l":
        pl = 1
        pk = 0
    # Loop sobre iterações
    for iter in range(0,max_iter_eq):
        # cALCULA jUROS
        r0 = alpha*(K0/L0)**(alpha-1) - delta
        # Excesso de Demanda
        excDem, govBal, V, gk, stat_dist, w, kd, Ka, La = Excess_Demand( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,r0,V,pk*t0,pl*t0,G,eps )
        #print( excDem, govBal, V, gk, stat_dist, w, kd, K, L, "\n")
        # Atualização dos parâmetros
        #ra = alpha*(Ka/La)**(alpha-1) - delta
        # print( "Ok2", "\n")
        # Atualizando Impostos
        ta = (G)/(pk*Ka*r0 + pl*La*w)
        # Distância
        dist = max( abs(ra-r0),abs(ta-t0) )
        # Printa Iteração | Excesso de Demanda | Resultado do Governo | Distância ;
        print( "Iteração: ", iter, " ; Demand Excess: ", excDem, " ; Govmnt Bal: ", govBal, " ; Dist: ", dist, "\n" )
        # Atualizando Juros e Taxas
        #r0 = lamb*r0 + (1-lamb)*ra
        K0 = lamb*K0 + (1-lamb)*Ka
        L0 = lamb*L0 + (1-lamb)*La
        t0 = t0 + lamb*(ta-t0)
    # Retorna Parametros
    return V,gk,stat_dist,w,kd,r0,t0,excDem,govBal

# Versão 2 Que analisa tanto Balanço do Governo quanto juros na Bisseção