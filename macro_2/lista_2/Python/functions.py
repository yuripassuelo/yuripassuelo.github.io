# Arquivo Compressor de Funcoes

import numpy as np
from numba import njit

# Iteracao da Funcao Valor
# - Recebe de Inputs:
#   1. beta   - propensao marginal a poupar
#   2. a_grid - grid de ativos
#   3. y_grid - grid de dotacoes
#   4. q      - Preco do ativo a
#   5. pi     - Matriz de Markov
#   6. u_func - Funcao utilidade
# - Retorna : Vetor de funcao Politica e funcao valor

@njit
def vfi( beta, y_grid, a_grid, q, pi, u_func ):
    # Distancias
    n_points = len( a_grid )
    n_states = len( y_grid )
    # Vetores de iteracao
    V        = np.zeros( ( n_points, n_states ) )
    Tv       = V.copy()
    pol_a    = V.copy()
    pol_p    = V.copy()
    # Parametros de Convergencia
    max_iter = 2000
    tol      = 1e-5
    dist     = 10
    iter     = 0
    # Iteracao ate convergencia
    while dist > tol and iter < max_iter:
        iter = iter + 1
        for j in range(0,n_states):
            y = y_grid[j] 
            for i in range(0,n_points):
                a  = a_grid[i]
                c  = (a + y - q*a_grid)
                c  = np.where(c > 0, c, np.finfo(float).eps)
                Ev = V @ pi[j,:]
                # Valor
                #v  = np.array( list( map( lambda con: u_func(con), c ) ) ) + beta*Ev
                v = u_func(c) + beta*Ev
                # Atualiza Vetores
                pol_p[i,j] = np.argmax(v)
                pol_a[i,j] = a_grid[int(pol_p[i,j])]
                Tv[i,j]    = np.max(v)
        # Atualiza Distancia
        dist = np.max(np.abs(Tv - V))
        #print( dist)
        V    = Tv.copy()
    return ( dist, V, pol_p, pol_a)

# Distribuicao Estacionaria e Excesso de demanda
# - Recebe de inputs
#   1. pol_a  - Vetor de funcao politica para cada estado
#   2. a_grid - Grid de a's possiveis
#   3. pi     - Distribuicao  de Markov
# - Retorna : Vetor de distribuicao estacionaria e vetor de excesso de demanda

def demand_n_distr( a_pol, a_grid, pi ):
    # Número de Pontos
    npo, ns = np.shape( a_pol )
    # Vetor Nulo
    Va = []
    # Loop preenchimento de matrizes
    for k in range(0, ns ):
        Va.append( a_pol[:,k][:,np.newaxis] == a_grid)
    # Convertendo para Array
    Va = np.array( Va, dtype=int  )
    # Criando Matriz M
    M = np.zeros( (npo*ns,npo*ns) )
    # Preenchendo matriz M
    for i in range(0,ns):
        for j in range(0,ns):
            #print( i*npo,':',(i+1)*(npo-1), '   ', j*npo,':',(j+1)*(npo-1) )
            M[ i*(npo):(i+1)*(npo) , j*(npo):(j+1)*(npo) ] = Va[i]*pi[i,j] 
    # Preenchendo Matriz M
    stat_dist = np.matrix( M )**1000
    stat_dist = np.reshape( np.array( stat_dist )[1,:], (ns,npo))
    # Excesso de Demanda
    demand_excess = - np.sum(a_pol * np.transpose(stat_dist) )
    # Retorna 
    return [stat_dist, demand_excess]

# Encontra Q em sinal Oposto para Iniciar Bicessao
# - Recebe Inputs:
#   1. excess_deman  - Excesso de Demanda
#   2. q0            - Preco Inicial
#   3. y_grid        - Grid de dotacao / Estados
#   4. beta          - Parametro
#   5. a_grid        - Grid de ativos
#   6. pi            - Matriz Markov
#   7. U             - Funcao Utilidade
#   5. price_i = 0.5 - Forca de Correcao
# - Retorna : qt ajustado para iniciar bissecao

def find_q( de, q0, y_grid, beta, a_grid, pi, U, price_i ):
    # Para dado preco Input de preco q0, vamos buscar um outro qt tal que
    # nos permita partir para a bissecao
    #
    # Regra é primeiro analisar o preço e sua relacao com o excesso de
    # demanda, caso o excesso de demanda seja positivo:
    #   1. Temos que aumentar o preco: qt = (1 - prc )*q
    # Caso o excesso seja negativo
    #   2. Temos que aumentar o preco: qt = (1 + prc )*q
    if de > 0:
        correction = 1 - price_i
        sign       = '>'
    else :
        correction = 1 + price_i
        sign       = '<'
    # Parametriza Condicoes
    qt   = q0
    de1  = de
    # Procurar em Loop
    while eval( 'de1'+sign+'0' ):
        # Aplica correcao
        qt = qt*correction
        # Reestima Iteracao sobre funcao valor e Excesso de Demanda
        dist_1, Vc_1, pol_p_1, pol_a_1  = vfi( beta, y_grid, a_grid, qt, pi, U )
        s_d_1, de1                      = demand_n_distr( pol_a_1, a_grid, pi )
        # Display dos resultados
        print( qt, de1 )
    # Retorna Preco novo e excesso de demanda 
    return (qt,de1)
