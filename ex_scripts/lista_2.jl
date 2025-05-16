

using Pkg
using Plots


# Iteração da função valor

# defini grid de capita

k_ss = ((0.3*(1/1.05)*1)/(1-(1/1.05)+(1/1.05)*0.05))^(1/(1-0.3))


k_grid = LinRange( 0.7*k_ss, 1.3*k_ss, 201 )

# Parametrização do problema

z = 1
α = 0.3
γ = 0.5
β = 1/1.05
δ = 0.05
r = 0

# Funções

#U( c ) = (c.^(1-γ))./(1-γ)
U( c ) = log.( c )
F( k ) = z.*k.^α

# Vetores de Iteração

v_it = zeros( length( k_grid ) )
g_it = zeros( length( k_grid ) )
V    = zeros( length( k_grid ) )

ε      = 1e-5
dist   = 100*1e-1 
max_it = 1000
it     = 0

typeof( ε )

while (it < max_it) 
    # Contador
    it = it + 1
    # Print Iteração e Distancia
    print( "Iteração: ", it, " ; Distância: ", dist, "\n" )
    # Cria vetor do operador
    Tv = zeros( 200 )
    for i in range(1,length(k_grid))
        # Calcula consumo
        c =  ( F(k_grid[i]) + (1-δ+r)*k_grid[i] .- k_grid .> 0 ).*(F(k_grid[i]) + (1-δ+r)*k_grid[i] .- k_grid ) + (( F(k_grid[i]) + (1-δ+r)*k_grid[i] .- k_grid  .<= 0 )).*eps()
        # Calcula Utilidade
        util = U( c ) .+ β.*V
        # Pega maior valor
        v_it[i] = maximum( util )
        g_it[i] = argmax( util )
    end
    # Calcula Distância
    dist = maximum( abs.( v_it .- V ) )
    # Atualiza vetor V
    V    = copy( v_it )

end

# Plots

plot( k_grid, V )

# Converte g_it para g_it k

g_it_k = [ k_grid[ Int64( g_it[i] ) ] for i in range(1, length( g_it )) ]

plot( k_grid, k_grid)
plot!( k_grid, g_it_k )


# 