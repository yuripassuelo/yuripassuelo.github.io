# Importanto Bibliotecas
import numpy as np
import numba as nb
import matplotlib.pyplot as plt
import time
import sys
import os

# ATENÇÃO: Selecionar a raiz
path = r'C:\\Users\\...'

sys.path.append( path )
# Importanto Funcoes
import functions as fc

t0 = time.time()
# Mains Script
sigma = 1.5
beta  = .9932
q     = 1
a_min = -4
a_max = 6
n     = 300

# Vator de Estados
X     = np.array([ 0.1, 1.0 ])

# Matriz de transicao
pi    = np.array([ [ .5  , .5   ],
                   [ .075, .925 ] ])

# Funcao Anonima da Utilidade
U = lambda c: (c**(1-sigma))/(1-sigma)

def U(c,sigma=1.5):
    return ((c**(1-sigma))/(1-sigma))

# Construção dos Grids
a_grid = np.linspace( a_min, a_max, n )
y_grid = X

# 2. Dado parametros iniciais Calcula
dist, Vc, pol_p, pol_a = fc.vfi( beta, y_grid, a_grid, q, pi, U )

s_d, de = fc.demand_n_distr( pol_a, a_grid, pi ) 

# 3. Buscando Outro Preco para poder realizar Bissecao

q1, de1 = fc.find_q(de, q, y_grid, beta, a_grid, pi, U, .1 )

# 4. Iniciar Bissecao para encontrar preco que zera Demanda Agregada

# Parametrizando Iteracoes
iter_b     = 0
max_iter_b = 100
tol_b      = 1e-5

if q1 > q:
    qb = q1
    qa = q
    da = de
    db = de1
else:
    qa = q1
    qb = q
    da = de1
    db = de

# Historicos
hist_q = [ q, q1 ]
hist_d = [ de, de1 ]

while (qb-qa)/2 > tol_b and iter_b < max_iter_b :
    # Ponto Intermediario
    qc = (qa+qb)/2
    # Recalculando VFI
    dist_1, Vc_1, pol_p_1, pol_a_1 = fc.vfi( beta, y_grid, a_grid, qc, pi, U )
    # Calcula Distr Estac e Excesso de demanda
    s_e, dc = fc.demand_n_distr( pol_a_1, a_grid, pi ) 
    # Criterio
    if dc == 0:
        break
    elif da*dc < 0:
        qb = qc
        db = dc
    else:
        qa = qc
        da = dc
    # Atualiza iteracao e Hist
    iter_b = iter_b + 1
    hist_d.append( dc )
    hist_q.append( qc )
    # Print Resultado
    print( qc, dc, iter_b)

t1 = time.time()

print( t1-t0)
# 5. Plots

np.save( path+r'results'+str(round(abs(a_min)))+r'.npy', np.array([ qc, Vc_1, pol_a_1, s_e, dc ]))


# Funcao Valor Convergida
plt.plot( a_grid, Vc[:,0], label = 'Low' )
plt.plot( a_grid, Vc[:,1], label = 'High' )
plt.xlabel(r'$a$')
plt.ylabel(r'$V$')
plt.legend()
#plt.savefig(path+r'figs\\plot_1.pdf')
plt.show()
plt.close()

# Funcao Politica
plt.plot( a_grid, pol_a[:,0], label = 'Low' )
plt.plot( a_grid, pol_a[:,1], label = 'High' )
plt.plot( a_grid, a_grid, linestyle = '--', color = 'grey', label = '90 graus' )
plt.legend()
plt.ylabel(r"$a'$")
plt.xlabel(r"$a$")
#plt.savefig(path+r'figs\\plot_2.pdf')
plt.show()
plt.close()

# Distribuicao Convergida
plt.plot( a_grid, s_d[0,:], label = 'Low' )
plt.plot( a_grid, s_d[1,:], label = 'High' )
plt.ylabel('Percent')
plt.xlabel( r'$a$')
plt.legend()
#plt.savefig(path+r'figs\\plot_3.pdf')
plt.show()
plt.close()

# Scatterplot de Precos e Excesso de Demanda
plt.scatter( hist_q, hist_d )
plt.xlabel(r'$q$')
plt.ylabel(r'Excesso de Demanda')
#plt.savefig(path+r'figs\\plot_4.pdf')
plt.show()
plt.close()

t1 = time.time()

print( t1-t0,' Seconds')


# (b) Achar a matriz M (a,y) 

# Número de Pontos

npo, ns = np.shape( pol_a )
# Vetor Nulo
Va = []
# Loop preenchimento de matrizes
for k in range(0, ns ):
    Va.append( pol_a[:,k][:,np.newaxis] == a_grid)
# Convertendo para Array
Va = np.array( Va, dtype=int  )
# Criando Matriz M
M = np.zeros( (npo*ns,npo*ns) )
# Preenchendo matriz M
for i in range(0,ns):
    for j in range(0,ns):
        #print( i*npo,':',(i+1)*(npo-1), '   ', j*npo,':',(j+1)*(npo-1) )
        M[ i*(npo):(i+1)*(npo) , j*(npo):(j+1)*(npo) ] = Va[i]*pi[i,j]

# Olhando o Plot da Matrix M

plt.imshow(M)
plt.colorbar()
plt.show()

auto_val, auto_vecs = np.linalg.eig( np.matrix(M).T)

idx = np.argmin(np.abs(auto_val - 1))

stationary = np.real(auto_vecs[:, idx])

stationary = stationary / stationary.sum()

stat_reshape = np.reshape( stationary, (ns,npo) ).T

stationary_2 = np.matrix(M)**1000

stat_reshape_2 = np.reshape( np.array(stationary_2 )[1,:], (ns,npo)).T

plt.plot( stat_reshape, "--" ,label = "Metodo 1" )
plt.plot( stat_reshape_2, label = "Metodo 2" )
plt.legend()
plt.show()
