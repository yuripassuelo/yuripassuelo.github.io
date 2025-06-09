

import matplotlib.pyplot as plt
import numpy as np

# Define os parametros

alpha = 0.5
beta  = 1
gamma = 1

a = 100
b = 10
h = 5

T  = 5

r1 = np.sqrt( (b*(1+alpha*b))/(alpha*(h**2)) )
r2 = -r1

bar_P = (a+2*alpha*a*b+beta*b)/(2*b*(1+alpha*b))

P0 = 5
PT = 7

A1 = (P0 - bar_P - (PT - bar_P)*np.exp(r1*T))/(1-np.exp( 2*r1*T) )
A2 = (P0 - bar_P - (PT - bar_P)*np.exp(r2*T))/(1-np.exp( 2*r2*T) )


# Curva de Preço

Ts = np.linspace( 0, T, 1000 )

def P( t, A1, A2, bar_P, r ):
    return A1*np.exp(r*t) + A2*np.exp(-r*t) + bar_P

curva_P = list( map( lambda t: P(t, A1, A2, bar_P, r1 ), Ts ) )

plt.plot( Ts, curva_P )
plt.show( )

# Exemplo para Exercicio 4

C = 5
r = 0.5
B1 = 4
B2 = 0.1

curva_1 = list( map( lambda t: P(t, B1, B2, C, r ), Ts ) )
curva_2 = list( map( lambda t: P(t, B2, B2, C, r ), Ts ) )
curva_3 = list( map( lambda t: P(t, B2, B1, C, r ), Ts ) )


plt.plot( Ts, curva_1, label = r"$A_1>A_2$" )
plt.plot( Ts, curva_2, label = r"$A_1=A_2$" )
plt.plot( Ts, curva_3, label = r"$A_1<A_2$" )
plt.legend()
plt.show( )
