
import numpy as np
import matplotlib.pyplot as plt
import random

# Lista 1 - Parametrizacao Oficial

X  = np.array([ 0.1359,
                0.5949,
                1.0539,
                1.5129,
                1.9719])

pi = np.array([ [0.0300, 0.3262, 0.5175, 0.1224, 0.0040],
                [0.0190, 0.2679, 0.5420, 0.1642, 0.0069],
                [0.0116, 0.2131, 0.5506, 0.2131, 0.0116],
                [0.0069, 0.1642, 0.5420, 0.2679, 0.0190],
                [0.0040, 0.1224, 0.5175, 0.3262, 0.0300]])

# - Parametrização Alternativa

X = np.array([0.93041763, 0.97779789, 1.02517815, 1.0725584 , 1.11993866])

pi = np.array([ [8.33945361e-02, 4.94420212e-01, 3.84253432e-01, 3.75337148e-02, 3.98105405e-04],
                [3.03638094e-02, 3.53032757e-01, 5.16739810e-01, 9.77536214e-02, 2.11000207e-03],
                [8.93376704e-03, 2.05990573e-01, 5.70151320e-01, 2.05990573e-01, 8.93376704e-03],
                [2.11000207e-03, 9.77536214e-02, 5.16739810e-01, 3.53032757e-01, 3.03638094e-02],
                [3.98105405e-04, 3.75337148e-02, 3.84253432e-01, 4.94420212e-01, 8.33945361e-02] ])

#in_path = r'C:\\Users\\yurim\\Desktop\\Mestrado\\2S2024\\Macroeconomia 2\\Aulas\\1. Equity Premium Puzzle\\vetores\\'
#X  = 1+np.load( in_path+r'discrete_states.npy')
#pi = np.load( in_path+r'discrete_matrix.npy')

mu    = 0.018
delta = 0.036


#X = np.array([ 1 + mu - delta, 1 + mu + delta])

#phi = 0.43
#pi = np.array( [ [ phi    , 1- phi ],
#                 [ 1 - phi, phi    ]])

# Funcao para Calculo do Premio de Risco
def risk_pre( beta, sigma, pi=pi, X=X, prices=False ):

    # Distribuição Invariante
    pi_bar = np.array( np.matrix(pi)**1000 )

    # Tamanho de X
    l_x    = len( X )

    # Matrizes Formatadas X
    X_s1 = X**(1-sigma) 
    X_s2 = X**( -sigma)

    # Matrizes para Calculo (A e B)
    # Matriz A
    A = beta*np.full( (l_x,l_x), [X_s1] )*pi

    # Matriz B
    B = beta* ( X_s1.T @ pi )

    # Precos da arvore
    p = np.linalg.inv( np.identity( l_x ) - A  ) @ B

    # Retorno da arvore
    m_g_p = np.meshgrid( p, p )
    R  = ( (m_g_p[0] + np.ones( (l_x,l_x))) * np.full( (l_x,l_x), X) - m_g_p[1] )/ m_g_p[1]
    # Retorno esperado
    Re = ( pi.T * R ) @ np.ones( l_x )

    # Retorno esperado - Longo Prazo
    r_e = np.dot(Re, pi_bar[0] )

    # Parte do Bond:
    Q = beta * pi @ X_s2

    # Retornos Bonds Livres de Risco
    r_f = np.sum( ( 1/Q - 1) * pi_bar[0] )

    if prices:
        
        return ( r_e, r_f, r_e-r_f, p, Q )
    
    else:

        return ( r_e, r_f, r_e-r_f )

# Construindo Grids de Combinações Distintas de \beta e \sigma
beta_grid = np.linspace( 0.1, 1, 100 )
sigm_grid = np.linspace( 0.1, 5, 100  )

# Mesh Grid
bet, sig = np.meshgrid( beta_grid, sigm_grid )

# Combinacoes
comb = np.array( [ [ risk_pre( beta = b, sigma = s) for s in sigm_grid ] for b in beta_grid ] )

# Plots
# Reorganizando Vetores
z_0 = comb[:,:,0]
z_1 = comb[:,:,1]
z_2 = comb[:,:,2]

# Ativo Arvore

plot_lvl_0 = plt.contourf( sig, bet, z_0, levels = np.linspace( np.min(z_0), np.max(z_0), 100 ) )
cb_0 = plt.colorbar( plot_lvl_0 )
plt.xlabel(r"$\sigma$")
plt.ylabel(r"$\beta$")
plt.show()

# Superficie

ax = plt.figure().add_subplot(projection='3d')
ax.plot_surface(sig, bet, z_0 )
ax.set_xlabel(r'$\sigma$')
ax.set_ylabel(r'$\beta$')
ax.set_zlabel(r'$r^e$')
ax.set_title(r'Retorno Arvore')

plt.show()

# Bond

plot_lvl_1 = plt.contourf( sig, bet, z_1, levels = np.linspace( np.min(z_1), np.max(z_1), 100 ) )
cb_1 = plt.colorbar( plot_lvl_1 )
plt.xlabel(r"$\sigma$")
plt.ylabel(r"$\beta$")
plt.show()

# Superficie

ax = plt.figure().add_subplot(projection='3d')
ax.plot_surface(sig, bet, z_1 )
ax.set_xlabel(r'$\sigma$')
ax.set_ylabel(r'$\beta$')
ax.set_zlabel(r'$r^f$')
ax.set_title(r'Retorno ativo livre de risco')

plt.show()

# Premio de Risco

plot_lvl_2 = plt.contourf( sig, bet, z_2, levels = np.linspace( np.min(z_2), np.max(z_2), 100 ) )
cb_2 = plt.colorbar( plot_lvl_2 )
plt.xlabel(r"$\sigma$")
plt.ylabel(r"$\beta$")
plt.show()

# Superficie

ax = plt.figure().add_subplot(projection='3d')
ax.plot_surface(sig, bet, z_2 )
ax.set_xlabel(r'$\sigma$')
ax.set_ylabel(r'$\beta$')
ax.set_zlabel(r'$r^e - r^f$')
ax.set_title(r'Premio de risco')

plt.show()

# Combinação de Valores de Beta = 0.99 e sigma menor do que 1.3 temos valores aceitaveis

# Baixando Dados do Ibovespa e Retorno Livre de Risco

exemplo = risk_pre( beta = .99, sigma = 2.0, prices=True )

# Preços
p = exemplo[3]

def simulate_markov(M, T, x0=2):
    # P( x' = Proximo | x = Atual )
    states = np.arange(M.shape[0])
    s = np.empty(T, dtype=int)
    s[0] = x0
    for t in range(1, T):
        s[t] = np.random.choice(states, p=M[s[t-1], :])
    return s

T = 2000
s = simulate_markov(pi, T, x0=2)

# Simulando Cadeia de Markov 

# Simula dividendos Y_t (levels) ---
Y = np.empty(T)
Y[0] = 1.0   # nível inicial
for t in range(1, T):
    Y[t] = X[s[t]] * Y[t-1]  # Y_{t} = x_t * Y_{t-1}

# Preços P_t ---
P = p[s] * Y   # p[s] seleciona p_{x_t}

# Análises básicas
logP = np.log(P)
logY = np.log(Y)
rets = np.diff(logP)


# Plots 
fig, axs = plt.subplots(3,1,figsize=(10,8), sharex=True)
axs[0].plot(logP); axs[0].set_title('log P')
axs[1].plot(logY); axs[1].set_title('log Y')
axs[2].plot(np.concatenate([[np.nan], rets])); axs[2].set_title('log retornos log P_t - log P_{t-1}')
plt.tight_layout()
plt.show()