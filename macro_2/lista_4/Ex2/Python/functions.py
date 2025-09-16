
import numpy as np


def compute_policy(Ve,Vu,TVe,TVu,gea,gua,den,beta,pi,N,M,b,r,wgrid,agrid):
    # Função utilidade
    u = lambda c: c**0.5
    # Parâmetros de iteração
    dist  = 10
    tol   = 1e-5
    it    = 0
    itmax = 1000
    # 
    while (dist > tol) and (it < itmax):
        # Contador de iterações
        it = it + 1
        # Função Valor do Desemprego:
        print( "Iteração: ", it, " ; Distancia: ", dist )
        # Iteração sobre o grid de capital
        for i in range(0,M):
            # Desempregado não depende de Salarios Logo
            c1 = ( b + (1+r)*agrid[i] - agrid >= 0 )*( b + (1+r)*agrid[i] - agrid ) + ( b + (1+r)*agrid[i] - agrid < 0 )*( np.finfo(float).eps )
            # Utilidade de se estar desempregado
            U   = u( c1 ) + beta * Vu
            # Iteração sobre o grid de salarios
            for j in range(0,N):
                # Consumo do empregado
                c2 = ( wgrid[j] + (1+r)*agrid[i] - agrid >= 0 )*( wgrid[j] + (1+r)*agrid[i] - agrid ) + ( wgrid[j] + (1+r)*agrid[i] - agrid < 0 )*( np.finfo(float).eps )
                # Salva vetor de funções valores e escolhas de capital
                E  = u( c2 ) + beta*( (1-pi)*Ve[:,j] + pi*Vu )
                # Armazena escolhas do empregado
                TVe[i,j]  = np.max( E ) # Guarda Valor do empregado
                gea[i,j]  = agrid[ np.argmax( E ) ] # Guarda Função Politica do Capital para empregado    (Quanto Poupar para o prox. Período)
            # Armazena escolhas do desempregado
            # print( np.shape(E))
            TVu[i]  = np.max( U )    # Guarda Valor do desempregado
            gua[i]  = agrid[ np.argmax( U ) ] # Guarda Função Politica do Capital para desempregado (Quanto Poupar para o prox. Período)
        # Calcula distância
        dist = np.max( [np.max( np.abs( TVu - Vu ) ), np.max( np.abs( TVe - Ve ) )] )
        # Copia do vetor para atualizat
        Vu = TVu.copy()
        Ve = TVe.copy()
    # Retorna Matrizes/Tensores
    return Ve,Vu,gea,gua
