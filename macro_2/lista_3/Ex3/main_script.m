
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

V  = zeros( N,M );

% 4.  Resolucao do Modelo

% Supondo apenas Taxação sob o Capital
tic
[V1,gk1,stationary_dist_k1,w1,kd1,r1,t1,excDem1,govBal1] = ModelSolution_Gov(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,0.1,"k");
toc

% Supondo apenas taxação sob o Trabalho
tic
[V2,gk2,stationary_dist_k2,w2,kd2,r2,t2,excDem2,govBal2] = ModelSolution_Gov(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,0.1,"l");
toc

% Supondo Uma aliquota unica que taxa capital e trabalho
tic
[V3,gk3,stationary_dist_k3,w3,kd3,r3,t3,excDem3,govBal3] = ModelSolution_Gov(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,0.1,"b");
toc

% Aprox 15-20 Mins

%% Plots






