import numpy as np
import matplotlib.pyplot as plt

# 1. Passo - Definicao do Grrid

# Capital de Steady State
k_ss = ((0.3*(1/1.05)*1)/(1-(1/1.05)+(1/1.05)*0.05))**(1/(1-0.3))

# Grid de Capital
k_grid  = np.linspace( start = 0.7*k_ss, stop = 1.3*k_ss, num = 201 )

# 2. Passo - Parametrização da Economia

# Parametros globais
z     = 1
alpha = 0.3
beta  = 1/1.05
delta = 0.05
sigma = 1
# Funcao Utilidade
def uti( c, sigma ):
    if sigma == 1:
        return np.log( c )
    if sigma != 1:
        return (c**(1-sigma))/(1-sigma)
    
# Funcao de Producao
def prod( k, z, alpha ):
    return z*(k**alpha)

# 3. Passo - Vetores de iteracao e tolerancia (Todos de tamanho 1 x n)
v_it  = [ 0 for i in range(0,len(k_grid))]
g_it  = [ 0 for i in range(0,len(k_grid))]
V     = [ 0 for i in range(0,len(k_grid))]
tol   = 1e-5

# 4. Passo - Iteracao sobre funcao valor

# Contador de iterações e distância inicial
dist = 1000
it = 1
store = True

if store:
    v_hist = []
    g_hist = []

while (dist > tol) | (it >1000) :

    print( "Iteração: ", it, ", Distância: ", dist )

    #V  = [ 0 for i in range(0,len(k_grid))]
    Tv = [ 0 for i in range(0,len(k_grid))]

    for i in range(0,len(k_grid)):
        for j in range(0,len(k_grid)):
            # Calculo do Consumo 
            cons = prod( k_grid[i], z, alpha ) + (1-delta)*k_grid[i] - k_grid[j]
            # Como não queremos consumo negativo colocaaamos essa condicional
            if cons >= 0:
                v = uti(cons, sigma) + beta*V[j]
                Tv[j] = v
            # Caso consumo for negativo atribuimos valor muito baixo
            else: 
                Tv[j] = -999
        # Valores maximos de capital e da funcaoa valor
        max_k = np.argmax(Tv)
        max_v = np.max(Tv)
        # Guardamos os valores maximos
        v_it[i] = max_v
        g_it[i] = max_k

    # Calculo da distancia
    dist = np.max( np.abs( np.array(v_it)-np.array(V)) )
    # Atualizando Funcao valor
    V  = np.copy( v_it )
    it = it + 1

    if store:
        v_hist.append( np.copy( v_it ) )
        g_hist.append( np.copy( g_it ) )
  

# Resgata valores de Capital
g_it_k = [ k_grid[i] for i in g_it ]

# Encontra capital de steady state
p = 0
while k_grid[p] != g_it_k[p]:
    p = np.where( k_grid == g_it_k[p])[0][0]
    print(p)

k_ss = k_grid[p]
c_ss = z*k_grid[p]**alpha +(1-delta)*k_grid[p] - k_grid[p]

# Plots

plt.plot( k_grid, v_it )
plt.xlabel(r"$k$")
plt.ylabel(r"$v$")
plt.show()

plt.plot( k_grid, g_it_k, label = "Funcao Politica" )
plt.plot( k_grid, k_grid, label = "90 Graus" )
plt.scatter( k_ss, k_ss )
plt.vlines( x = k_ss, ymin = np.min(k_grid), ymax = k_ss, colors="grey", linestyles="dashed" )
plt.hlines( y = k_ss, xmin = np.min(k_grid), xmax = k_ss, colors="grey", linestyles="dashed" )
plt.legend()
plt.xlabel(r"$k$")
plt.ylabel(r"$k'$")
plt.show()

for i in [1,2,10,50,100,150,200,250,264]:
    plt.plot( v_hist[i], label = r"Iter "+str(i) )
plt.legend( loc = 'right')
plt.xlabel(r"$k$")
plt.ylabel(r"$v$")
plt.show()

# Itém (e)

# Atualizando parâmetro z
z = 1.05

# Vamos agora a construção dos nossos vetores de iteração

v_hist = [ np.copy( v_it ) ]
g_hist = [ np.copy( g_it ) ]

dist = 1000
store = True

while (dist > tol) | (it >1000) :

    print( "Iteração: ", it, ", Distância: ", it )

    Tv     = [ 0 for i in range(0,len(k_grid))]

    for i in range(0,len(k_grid)):
        for j in range(0,len(k_grid)):
            # Calculo do Consumo 
            cons = prod( k_grid[i], z, alpha ) + (1-delta)*k_grid[i] - k_grid[j]
            # Como não queremos consumo negativo colocamos essa condicional
            if cons >= 0:
                v = uti(cons, sigma) + beta*V[j]
                Tv[j] = v
            # Caso consumo for negativo atribuimos valor muito baixo
            else: 
                Tv[j] = -999
        # Valores maximos de capital e da funcao valor
        max_k = np.argmax( Tv )
        max_v = np.max( Tv )
        # Guardamos os valores maximos
        v_it[i] = max_v
        g_it[i] = max_k

    # Calculo da distancia
    dist = np.max( np.abs( np.array(v_it)-np.array(V) ) )
    # Atualizando Funcao valor
    V    = np.copy( v_it )
    it   = it + 1

    if store:
        v_hist.append( np.copy( v_it ) )
        g_hist.append( np.copy( g_it ) )


v0 = v_hist[0]
vn = v_hist[len(v_hist)-1]

# Corrigindo funcao politica prra pegar capital
g_it_k_z105 = [ k_grid[i] for i in g_it ]

# Funcao Politica de Consumo
c_z100 = 1*k_grid**0.3 + (1-delta)*k_grid - g_it_k
c_z105 = 1.05*k_grid**0.3 + (1-delta)*k_grid - g_it_k_z105

# Estimando aa trajetória ótima a partir do Capital de Steady State Inicial
t = 0

t_vec   = [ t ]
k_trans = [ k_grid[p] ]
c_trans = [ 1*k_grid[p]*alpha + (1-delta)*k_grid[p] - k_grid[p] ]

while k_grid[p] != g_it_k_z105[p]:
    q = p

    p = np.where( k_grid == g_it_k_z105[p])[0][0]
    print(p) 

    k_trans.append( k_grid[p] )
    c_trans.append( z*k_grid[q]*alpha + (1-delta)*k_grid[q] - k_grid[p] )

    t = t + 1

    t_vec.append( t )

k_ss_z105 = k_grid[p]
c_ss_z105 = z*k_grid[p]**alpha +(1-delta)*k_grid[p] - k_grid[p]

# Plots
# Comparando Função valor Convergida de z=1 com z=1.05
plt.plot( k_grid, v_hist[0], label = r"$z=1$" )
plt.plot( k_grid, v_hist[len(v_hist)-1], label = r"$z=1.05$" )
plt.legend()
plt.xlabel( r"$k$" )
plt.ylabel( r"$v$" )
plt.show()

# Comparando função politica de consumo para z=1 e z=1.05
plt.plot( k_grid, c_z100, label = r"$z=1$" )
plt.plot( k_grid, c_z105, label = r"$z=1.05$" )
plt.xlabel(r"$k$")
plt.ylabel(r"$c$")
plt.legend()
plt.savefig(r"C:\\Users\\T-Gamer\Desktop\\Notas macroI\\figs\\"+r"04_f_pol_cons_s"+str(sigma)+"_comp.pdf")
plt.show()
plt.close()

# Transição de Capital e Consumo
fig, axs = plt.subplots(1, 2)

axs[0].plot( t_vec, k_trans )
axs[0].set_title(r"Transicao Capital")

axs[1].plot( t_vec, c_trans)
axs[1].set_title(r"Transicao Consumo")

plt.savefig(r"C:\\Users\\T-Gamer\Desktop\\Notas macroI\\figs\\"+r"06_f_trans_cons_s"+str(sigma)+".pdf")
plt.show()
plt.close()

