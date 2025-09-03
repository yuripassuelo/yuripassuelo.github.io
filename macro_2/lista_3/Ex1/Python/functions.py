
import numpy as np

# Functions


def vfi(beta,gamma,n_grid,k_grid,pi,N,M,V,r,w ):

    util = lambda c : (c**(1-gamma))/(1-gamma) 

    Tv = V.copy()
    gk = V.copy()

    # Parametros Iniciais
    dist     = 10
    iter_max = 2000
    tol      = 1e-5
    it       = 0

    while dist > tol and it < iter_max:
        it = it + 1
        for i in range(0,M):
            for j in range(0,N):

                c = ( w*n_grid[i] + (1+r)*k_grid[j] - k_grid ) * (( w*n_grid[i] + (1+r)*k_grid[j] - k_grid )>0) + np.finfo(float).eps * (( w*n_grid[i] + (1+r)*k_grid[j] - k_grid )<=0)

                value = util( c ) + beta  * V @ pi[i ,:]

                Tv[j,i] = np.max( value )
                pos     = np.argmax( value )
                gk[j,i] = k_grid[ pos ]
        dist = np.max( abs( Tv - V) )
        #print( it, ' - ',dist )
        V    = Tv.copy()

    return V, gk



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



def Excess_Demand( alpha, beta, gamma, delta, n_grid, k_grid, pi, N, M, Nbar, r, V):
    # Demanda de Capital
    Kd = (alpha/(r+delta))**(1/(1-alpha))*Nbar
    # Salario
    w  = (1-alpha)*(Kd/Nbar)**alpha
    # Calculo de oferta 
    V, gk     = vfi(beta,gamma,n_grid,k_grid,pi,N,M,V,r,w)
    stat_dist = demand_n_distr( gk, k_grid, pi, M, N )
    #
    Ea        = np.sum( gk * np.transpose( stat_dist ) )
    excDem    = (Ea - Kd)/((Ea + Kd) / 2)
    # Retorna Valores
    return excDem, V, gk, stat_dist, w, Kd, Ea



def Model_Solution( alpha, beta, gamma, delta, n_grid, k_grid, pi, M, N, Nbar, V ):
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
        excDem, V, gk, stationary_dist, w, Kd, Ea = Excess_Demand(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,Nbar,rguess,V)
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
    return V,gk,stationary_dist,w,Kd,Ea,r,excDem