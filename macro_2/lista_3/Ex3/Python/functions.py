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


def Excess_Demand( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,r,V, tau1,tau2, G, eps ):  
    # Demanda de Capital
    kd = ((r+delta)/alpha)**(1/(alpha-1))
    # Salario
    w  = (1-alpha)*(kd)**alpha
    # Calculo de oferta 
    V, gk = vfi(beta,gamma,n_grid,k_grid,pi,N,M,V,r,w, tau1, tau2, eps)
    stat_dist = demand_n_distr( gk, k_grid, pi, M, N )
    #
    Ks = np.sum( gk * np.transpose( stat_dist ) )
    Ls = np.sum( ( np.transpose( stat_dist ) ) @ n_grid )
    #Ea        = np.sum( gk * np.transpose( stat_dist ) )
    excDem    = ((Ks/Ls) - kd)/(((Ks/Ls) + kd) / 2)
    # Analisa Resultado do Governo
    govBal    = r*tau1*Ks + w*tau2*Ls - G
    # Retorna Valores
    return excDem, govBal, V, gk, stat_dist, w, kd




def Model_Solution_Interest( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,tau1,tau2,G,eps ):
    # Chutes Iniciais
    r0  = 0.001
    r1  = 0.2
    # Configurando Iteracoes
    max_iter_int = 100
    toleq        = 0.001
    # Loop
    for iter_int in range(0,max_iter_int):
        # Chute Medio
        rguess = (r0+r1)/2
        # Excesso de Demanda
        #                                         Excess_Demand( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,r,     V, tau1,tau2, G, eps )
        excDem, govBal, V, gk, stat_dist, w, kd = Excess_Demand( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,rguess,V, tau1,tau2, G, eps)
        print( "Iteração Juros: ", iter_int, " ; Excesso de Demanda: ", excDem )
        # Atualização da Bisscao
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
    return V,gk,stat_dist,w,kd,r,excDem,govBal

def Model_Solution_Gov( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,G,eps,tipo_tau ):
    # 1 Etapa Define tipo de taxação
    if tipo_tau == "k":
        pk = 1
        pl = 0
    if tipo_tau == "l":
        pk = 0
        pl = 1
    if tipo_tau == "b": 
        pk = 1
        pl = 1
    # Chutes Iniciais
    t0 = 0.01
    t1 = 0.7
    # Configurando iterações
    max_iter_imp = 100
    tol_eq = 0.001
    # Loop
    for iter_imp in range(0,max_iter_imp):
        # Chute Medio
        tguess = (t0+t1)/2
        # Excesso de Demanda
        #                                     Model_Solution_Interest( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,tau1,     tau2,     G,eps )
        V,gk,stat_dist,w,kd,r,excDem,govBal = Model_Solution_Interest( alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,pk*tguess,pl*tguess,G,eps )
        print( "Iteração Imposto : ", iter_imp, " ; Orçamento Gov: ", govBal )
        # Atualização da Bisscao
        if abs(govBal) < tol_eq:
            break
        # COndicao de atualização
        if govBal < 0:
            t0 = tguess
        else:
            t1 = tguess
    t = (t0 + t1)/2
    print( t )
    return V,gk,stat_dist,w,kd,r,t,excDem,govBal
