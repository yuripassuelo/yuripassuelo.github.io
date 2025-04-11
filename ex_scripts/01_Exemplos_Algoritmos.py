



## Achar Ponto Fixo da função

# Setar a função
import math

f = lambda x: math.log(x) + 5

nmax = 1000

# Chute inicial

z = 1

n = 1

while n <= nmax:

    f_z = f( z )

    print( "Iteração: ", n, "; z = ", z, "; f(z) = ", f_z )

    if abs( f_z - z ) <= tol :
        break

    z = f_z

    n = n+1


tol  = 1e-5
nmax = 1000

xs = [ i for i in range(1,12)]

fxs = list(map( f, xs ))

plt.plot( xs, fxs )
plt.plot( xs,xs )
plt.show()


## Algoritmo de Bisseção

# Definição dos Inputs

C = 19
f = lambda x: x**2 - C

a = 3
b = 5

tol  = 1e-5
nmax = 1000

# Valorando a função em a e em b

f_a = f( a )
f_b = f( b )

# Vetor que guarda valores de x = y dos nossos chutes

it     = []
x_vec  = []
fx_vec = []


# Contagem de etapas
n = 1

while n <= nmax :
    
    # Ponto Mediano
    c = (a + b) / 2
    print( "iteração: ", n, "; valor: ", c )

    f_c = f( c )

    it.append( n )
    x_vec.append( c )
    fx_vec.append( f_c )
    
    if f_c == 0 or (b-a)/2 <= tol :
        break
    
    # Atualiza a ou b
    if ( f_c > 0 ) == (f_a > 0):
        a   = c
        f_a = f( a )
    else:
        b   = c
        f_b = f( b )
    
    # COnta iteração    
    n = n + 1


import matplotlib.pyplot as plt

#criando vetor de x's

xs = [ i/100 for i in range(400,470)]

fxs = list( map( f, xs ) )


plt.scatter( x_vec, fx_vec )
plt.plot( xs, fxs )
plt.hlines( y = 0, xmin = 4, xmax = 4.7, colors = "grey", linestyles = "dashed" )
plt.show()

## Gradient Descendente Regressão Linear


# Simulando Dados

import numpy as np

# Erros

N = 1000

e = np.random.normal( 0, 5, size = N )
x = np.random.uniform( low = -10, high = 10, size = N )

# Parametros

a = 15
b = 2

y = a + b*x + e 

y_hat = a + b*x 

plt.scatter( x, y )
plt.plot( x, a+b*x , c = "red" )
plt.show()

# Algoritmo de Gradiente descendente

nmax = 10000
tol  = 1e-5

# chute inicial

beta = np.zeros( 2 )

X = np.column_stack((np.ones(N), x))


def grad(X, erro ):
    N = len( erro )
    return -(2/N) * X.T @ erro

beta  = np.zeros(2)

n = 1
gamma = 0.001

hist_sqr = [  ]
hist_bet = [  ]

while n <= nmax:

    # Erro calculado
    erro = y - X @ beta
    sqr  = np.sum( np.square( erro ) )
    print( "Iteração: ", n, "; Beta: ", beta, "; SQR: ", sqr )

    # Calcula Gradiente
    grad_v = grad( X, erro )

    # Guarda Histórico
    hist_sqr.append( sqr )
    hist_bet.append( np.copy( beta ) )

    # Atualiza $\beta$
    beta -= gamma*grad_v

    # Condição de convergência
    if np.max( abs( beta - hist_bet[ len( hist_bet ) - 1] ) ) <= tol:
        print( "Convergência Alcançada em Beta: ", beta)
        break

    # Atualiza Passo
    n = n + 1

h = np.transpose( np.array( hist_bet ) )



plt.scatter( h[0,:], h[1,:])
plt.show()



# Plot 3D do

vec_x = np.linspace( 0, 20, num = 500 )
vec_y = np.linspace( -5, 5, num = 500 )

xs, ys = np.meshgrid( vec_x, vec_y )

def SQR(xf,yf, X, y):
    B = np.array([xf,yf])
    return np.sum( np.square( y - X @ B ) )

zs = np.zeros( (500,500) )

for i in range(0 , len( xs ) ):

    for j in range( 0, len( xs[i] ) ):

        zs[i,j] = SQR( xs[i,j], ys[i,j], X, y )

# Plot 3d

from matplotlib import cm

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Superficie
surf = ax.plot_surface(xs, ys, zs, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
surf = ax.scatter3D( h[0,:] , h[1,:], hist_sqr )
ax.set_xlabel( r"$\beta_0$")
ax.set_ylabel( r"$\beta_1$")
ax.set_zlabel( r"$SQR$")


plt.show()