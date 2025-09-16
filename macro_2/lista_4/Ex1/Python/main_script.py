
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

path_fun = r""

# Parameters

beta  = 0.98
b     = 0.01
wBar  = 20
pi    = 0.1
sigma = 5

# Grid

N     = 1000
wgrid = np.linspace(0,wBar,N)

u = lambda c: c**0.5

# Distribution Function/Density
# f(0) = 2f(W) = 2 a1 + 40 a2
# f(W) = a1 + 20 a2

# Calulo das integrais por intervalo

a11 = 2/30 
a12 = -1/600

a21 = 1/30
a22 = 1/600

F1 = linear_dens_fun(a11,a12,wgrid) 
F2 = linear_dens_fun(a21,a22,wgrid)

# Vetores para densidade

den1 = np.zeros( N )
den2 = np.zeros( N ) 
denN = np.zeros( N )

for j in range(1,N):
    
    den1[j] = integrate.quad( lambda w: linear_dens_fun(a11,a12,w), wgrid[j-1],wgrid[j] )[0]
    den2[j] = integrate.quad( lambda w: linear_dens_fun(a21,a22,w), wgrid[j-1],wgrid[j] )[0]
    denN[j] = 1/N

# Plot das funções densidades

plt.plot( wgrid, den1, label = r"$f(w)=\frac{1}{30} + \frac{1}{600}w$" )
plt.plot( wgrid, den2, label = r"$f(w)=\frac{2}{30} - \frac{1}{600}w$"  )
plt.plot( wgrid, denN, label = r"$f(w)=\frac{1}{20}$"  )
plt.xlabel(r"$w$")
plt.ylabel(r"$f(w)$")
plt.legend()
plt.show()

# Iteração da função Valor

V  = np.zeros( N )
TV = V.copy()
g  = V.copy()

t0 = time.time()

V1, g1 = compute_policy(V,TV,g,den1,beta,pi,N,b,wgrid)
V2, g2 = compute_policy(V,TV,g,den2,beta,pi,N,b,wgrid)
V3, g3 = compute_policy(V,TV,g,denN,beta,pi,N,b,wgrid)

t1 = time.time()

# Salário de Reserva

wstar1 = wgrid[ np.where( g1 < 1 )[0][0] ] 
wstar2 = wgrid[ np.where( g2 < 1 )[0][0] ]
wstar3 = wgrid[ np.where( g3 < 1 )[0][0] ]

out_path = r"C:\\Users\\yurim\\Desktop\\Mestrado\\2S2024\\Macroeconomia 2\\Listas\\Lista 4\\Python\\figs\\"

# Função Valor

plt.plot( wgrid, V1, label = r"$f(w)=\frac{2}{30} - \frac{1}{600}w$" )
plt.plot( wgrid, V2, label = r"$f(w)=\frac{1}{30} + \frac{1}{600}w$" )
plt.plot( wgrid, V3, label = r"$f(w)=\frac{1}{20}$" )
plt.xlabel(r"$w$")
plt.ylabel(r"$V$")
plt.legend()
plt.savefig( out_path+r'1_Value.pdf')
plt.show()


# Função Politica

plt.plot( wgrid, (g1*(-1)+1), label = r"$f(w)=\frac{2}{30} - \frac{1}{600}w$" )
plt.plot( wgrid, (g2*(-1)+1), label = r"$f(w)=\frac{1}{30} + \frac{1}{600}w$" )
plt.plot( wgrid, (g3*(-1)+1), label = r"$f(w)=\frac{1}{20}$" )
plt.xlabel(r"$w$")
plt.ylabel(r"$V$")
plt.legend()
plt.savefig( out_path+r'1_Pol.pdf')
plt.show()


