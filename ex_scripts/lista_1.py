# Importanto pacotes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Funcao Consumo Individuo 1
def c_t_1(t, b1, b2):
   return ((b1**t)*(2-2*b1))/( (b1**t)*(1-b1) + (b2**t)*(1-b2) )
  
# Funcao Consumo Individuo 2  
def c_t_2(t, b1, b2): 
   return ((b2**t)*(2-2*b2))/( (b1**t)*(1-b1) + (b2**t)*(1-b2) )
  
# Parametro Fixado beta 2 
b2 = 0.95

# Vetor de Periodos que vamos guardar
t_s  = []
# Range de beta 1 que usaremos
b1_range = [ i/100 for i in range(1,95) ]

# Iteracaio para cada beta 1 possível
for b1 in b1_range:
    # Inicializando t em zero
    t = 0
    # loop
    while c_t_1(t,b1,b2) >= c_t_2(t,b1,b2):
        t = t+1
        # Ao fim do loop guardamos os valores dos periodos associados
    t_s.append( t )
# Plot das combinacoes de beta 1 e periodo ate sinais se inverterem
fig2 = plt.figure()
plt.plot( b1_range, t_s )
plt.xlabel( r'$\beta_1$' )
plt.ylabel( r'$t$' )
plt.title(r'$\beta_2$ = 0.95')
plt.show()