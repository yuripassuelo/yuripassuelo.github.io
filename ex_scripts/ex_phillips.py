
import numpy as np
import matplotlib.pyplot as plt


# Caso 1 : pit = 0

rho   = -0.1

T     = 10

pi0   = 5
piT   = 0

alpha = 1.5
beta  = 0.5
j     = 2

Omega = (alpha*(beta**2)*j*(rho+j))/(1+alpha*(beta**2))

r1 = (1/2)*( rho + np.sqrt( rho**2 + 4*Omega ) )
r2 = (1/2)*( rho - np.sqrt( rho**2 + 4*Omega ) )


A1   = (-pi0*np.exp(r2*T))/(np.exp(r1*T)-np.exp(r2*T))
A2   = (pi0*np.exp(r1*T))/(np.exp(r1*T)-np.exp(r2*T))

def Exp( t, A1, A2, r1, r2 ):

    return A1*np.exp( r1*t ) + A2*np.exp( r2*t )

Ts = np.linspace( 0, T, 1000 )


curva_Pi = list( map( lambda t: Exp(t, A1, A2, r1, r2 ), Ts ) )

plt.plot( Ts, curva_Pi )
plt.show( )

# Caso 2 : pit > 0

rho   = -0.1

T     = 10

pi0   = 5
piT   = 2

alpha = 1.5
beta  = 0.5
j     = 2

Omega = (alpha*(beta**2)*j*(rho+j))/(1+alpha*(beta**2))

r1 = (1/2)*( rho + np.sqrt( rho**2 + 4*Omega ) )
r2 = (1/2)*( rho - np.sqrt( rho**2 + 4*Omega ) )

A1   = (piT-pi0*np.exp(r2*T))/(np.exp(r1*T)-np.exp(r2*T))
A2   = (pi0*np.exp(r1*T)-piT)/(np.exp(r1*T)-np.exp(r2*T))


Ts = np.linspace( 0, T, 1000 )


curva_Pi = list( map( lambda t: Exp(t, A1, A2, r1, r2 ), Ts ) )

plt.plot( Ts, curva_Pi )
plt.show( )