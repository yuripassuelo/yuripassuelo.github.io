
% Modelo Ayiagari (1994) 

clc
clear
close all

tic

% Parametrizacao da Economia

beta  = 0.96 ;
gamma = 2    ;
alpha = 0.36 ;
delta = 0.05 ;

% Grids e Matriz de Transição
% Produtividade idiossincratica (Low and High)

n_grid = [ 0.5 1.0 1.1 ];
M      = length(n_grid);
% Matriz de Transição
pi     = [ 0.7 0.2 0.1 ; 0.2 0.6 0.2; 0.1 0.2 0.7 ];

% Distribuição Invariante   
inv_pi = pi^1000 ;
inv_pi = inv_pi(1,:) ;

% Produtividade Média
Nbar   = sum(n_grid.*inv_pi);

% Grids de Capital
N    = 1000;
kmax = 25;
k_grid = linspace(0, kmax, N);

% 1. Funcao para Iteracao da Funcao Valor

V = zeros( N,M );

% 4. Funcao que pega Bissecao e Aplica Bissecao

[V,gk,stationary_dist,w,Kd,Ea,r,excDem] = ModelSolution(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,Nbar,V);

toc

%% Plots

% Distribuição Agregada

agg_stat_dist = stationary_dist(:,1) + stationary_dist(:,2) + stationary_dist(:,3) ;


% Analise da desigualdade de Renda

k_len = length( k_grid );

x_axis = cumsum( agg_stat_dist );
y_axis = k_grid/kmax;

plot( x_axis, y_axis )    

% Calculando Indice de GINI

[sorted_incomes, sort_idx] = sort(y_axis);
sorted_cumulative_population = x_axis(sort_idx);

% Compute cumulative income proportions
cumulative_income = cumtrapz(sorted_cumulative_population, sorted_incomes);

% Compute the area under the Lorenz curve
area_lorenz_curve = cumulative_income(end); % Since Lorenz curve starts at 0 and ends at cumulative_income(end)

% Calculate the Gini index
gini_index = 1 - 2 * area_lorenz_curve;

% Display the result
disp(['Gini Index: ', num2str(gini_index)]);




