

import time
import matplotlib.pyplot as plt
import numpy as np

# Exercicío 3

# Matriz do Processo de Markov
M = np.matrix( [[0.20, 0.30, 0.40, 0.10],
                [0.10, 0.10, 0.70, 0.10],
                [0.95, 0.024, 0.025, 0.001],
                [0.25, 0.25, 0.25, 0.25]])

# Distribuição Inicial
p0 = np.array([ 0.25, 0.25, 0.25, 0.25 ])

# Tolerância
tol = 10e-7

# Iteracao
p  = p0
q  = p0*M
k = 1

dist = np.sum( np.square(p-q) )

while dist > tol:
    # Atualiza vetores
    p = q
    q = q * M
    # Calcula distancia
    dist = np.sum( np.square(p-q))  
    k = k + 1

print(k)

## Exercicio 4
# - Inclusao de choques estocasticos
# - Inclusao da escolha de trabalho
start = time.time()
# Grid de Capital
k_grid = np.linspace(0.01, 10, 51 )

# Grid de Trabalho
n_grid = np.linspace(0, 1, 11 )

# Vetor de choques
Z = np.array([0.8, 1.0, 1.2])

# Matriz de transição
pi = np.array([[ 0.2,  0.5,  0.3 ], 
               [ 0.1,  0.6,  0.3 ], 
               [ 0.25, 0.25, 0.5 ]])

# Parametros
alpha = 0.3
beta  = 1/1.05
delta = 0.05
phi   = 1

# Funcao Utilidade
def uti(c,l,phi):
    return np.log(c) - (l**(1+phi))/(1+phi)

# Funcao de Producao
def prod( z,k,l, alpha):
    return z*(k**alpha)*(l**(1-alpha))

# Vetores de chute inicial e de iteracao
v_ini = np.zeros( len(k_grid) )
z_ini = np.array([ v_ini for i in range(0,len(Z)) ])
# Vetores de iteração
Gk_it = np.zeros( len( k_grid ))
Gn_it = np.zeros( len( k_grid ))
gn_it = np.zeros( len( k_grid ))
# Tolerancia
tol  = 1e-5
dist = 1000
it = 0
# Dist
hist_dist = []
V_hist    = []
k_hist    = []
n_hist    = []
# Loop
while dist > tol:
    # Para Loop se tivermos mais de 1000 Iteracoes
    if it >= 1000:
        break
    # Vetor de Iteracao Z
    Tz = np.array( [v_ini for i in range(0,len( Z ))]) 
    Gk = np.array( [v_ini for i in range(0,len( Z ))]) 
    Gn = np.array( [v_ini for i in range(0,len( Z ))]) 
    # Iteracao sobre vetor Z
    for z in range(0,len(Z)):
        # Vetor de Iteracao k
        Tv = np.zeros( len( k_grid ))
        # Iteracao sobre k
        for i in range(0,len(k_grid)):
            v_it = np.zeros( len( k_grid ))
            for j in range(0,len( k_grid )):
                # Iteracao sobre sobre vetor n_grid
                n_it = np.zeros( len( n_grid ))
                for n in range(0,len( n_grid )):
                    # Calcula Consumo
                    cons = prod(Z[z],k_grid[i],n_grid[n],alpha)+(1-delta)*k_grid[i]-k_grid[j]
                    if cons >  0:
                        Ev      = np.dot(pi[z],z_ini)[j] # np.sum((np.transpose(z_ini)*pi[z])[j])
                        n_it[n] = uti(cons,n_grid[n],phi) + beta*Ev
                    if cons <= 0:
                        n_it[n] = -np.inf               
                v_it[j]  = np.max( n_it )
                gn_it[j] = n_grid[ np.argmax( n_it ) ]
            Tv[i]   = np.max( v_it )
            Gk_it[i] = k_grid[ np.argmax( v_it ) ]
            Gn_it[i] = gn_it[ np.argmax( v_it ) ]
        # Guarda valores para cada z distinto
        Gn[z] = Gn_it
        Gk[z] = Gk_it 
        Tz[z] = Tv
    # Calcula distancia
    dist = np.max( abs( Tz - z_ini ))
    # Printa Iteração
    print( "iteracao: ", it," ,Distancia: ",dist )
    # Atualiza vetores
    z_ini = Tz
    # Atualiza Iteracao
    it = it + 1

end = time.time()
print( end - start )

# Plot Funcao Valor
for item in range(0,len(Tz)):
    plt.plot( k_grid, Tz[item], label = r"$z=$"+str(Z[item]) )
plt.legend()
plt.xlabel(r"$k$")
plt.ylabel(r"$V$")
plt.show()

# Plot Funcao Politica Capital
for item in range(0,len(Gk)):
    plt.plot( k_grid, Gk[item], label = r"$z=$"+str(Z[item]) )
plt.plot( k_grid, k_grid, linestyle = "dashed", color = "grey", label = "90 graus" )
plt.legend()
plt.xlabel(r"$k$")
plt.ylabel(r"$k'$")
plt.show()

# Plot Funcao Politica trabalho
for item in range(0,len(Gn)):
    plt.plot( k_grid, Gn[item], label = r"$z=$"+str(Z[item]) )
plt.legend()
plt.xlabel(r"$k$")
plt.ylabel(r"$l$")
plt.show()

# Capital de estado estacionario
for i_z, zs in enumerate( Z ):
    i_k = 0
    it  = 0
    while k_grid[i_k] != Gk[i_z][i_k] and it < 100:
        i_k = np.where( k_grid == Gk[i_z][i_k] )[0][0]

        it = it + 1       
    print( "z = ",zs,", k_ss = ",k_grid[i_k])   
