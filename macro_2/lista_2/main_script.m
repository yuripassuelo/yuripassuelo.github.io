clc
clear
close all

%tic

% Main Script
% 1. Parametrizacao da Economia

sigma = 1.5;
beta = 0.9932;
q = 1;
a_min = -4;
a_max = 6;
N = 300;
y_L = 0.1;
y_H = 1.0;

% Probabilidades de Transicao
pi_HH = 0.925;
pi_HL = 0.5;
pi_LH = 1 - pi_HH;
pi_LL = 1 - pi_HL;

% Grids
a_grid = linspace(a_min, a_max, N);
y_grid = [y_L, y_H];
pi = [pi_LL, pi_LH; pi_HL, pi_HH]';

M = length( y_grid );

V = zeros( N,M );

% 2. Primeira Etapa Chutes Iniciais

[ V, a_pol ] = vfi(beta,sigma,y_grid,a_grid,q,pi,M,N,V);

% Calculo Distribuicao e excesso de demanda

[ stat_dist, d_excess ] = demand_n_distr( a_pol, a_grid, pi, N, M);

% 3. Etapa Encontrado valor para inciar Bissecao

% Dado excesso de demanda C vamos ver o que fazer:

[ q1, d_excess_1 ] = find_q(d_excess,q,y_grid,beta,sigma,a_grid,pi,V,M,N,0.1 );

% 4. Aplicar Bicessao e encontrar nosso q otimo

% Parametrizando Iteracoes
iter_b     = 0;
max_iter_b = 100;
tol_b      = 1e-5;

% Organizando Precos
if q1 > q
    qb         = q1;
    qa         = q;
    d_excess_a = d_excess;
    d_excess_b = d_excess_1;
else
    qa         = q1;
    qb         = q;
    d_excess_a = d_excess_1;
    d_excess_b = d_excess;
end

hist_q = [ q q1 ];
hist_d = [ d_excess d_excess_1 ];

% Bisection method loop
while (qb - qa) / 2 > tol_b && iter_b < max_iter_b
    qc = (qa + qb) / 2;

    % Iterando funcao valor com novo preco
    [ V, a_pol ] = vfi(beta,sigma,y_grid,a_grid,qc,pi,M,N,V);

    % Calculando Excesso de Demanda
    [ stat_dist_c, d_excess_c ] = demand_n_distr( a_pol, a_grid, pi, N, M );
   
    % Atualizando
    if d_excess_c == 0
        break;
    elseif d_excess_a * d_excess_c < 0
        qb         = qc;
        d_excess_b = d_excess_c;
    else
        qa         = qc;
        d_excess_a = d_excess_c;
    end
    % Atualiza Iteracao
    iter_b = iter_b + 1;

    % Guarda Historico
    hist_d(end+1) = d_excess_c;
    hist_q(end+1) = qc;
    
    % Display iteracao
    disp( iter_b   );
    disp( d_excess_c );
end

toc

% Plots - 

% Funcao Valor Convergia
plot( a_grid, V_conv )

% Funcao Politica
figure(1)
plot( a_grid, a_pol(:,1) );
hold on;
plot( a_grid, a_pol(:,1) );
plot( a_grid, a_grid );
hold off ;
legend( 'High', 'Low', '90 Graus');

% Distribuicao
plot( sum( stat_dist_c,2) )


% Distribuicao por heterogeneidade
figure(2)
plot( a_grid, stat_dist(:,1) )
hold on
plot( a_grid, stat_dist(:,2) )
xlabel('Assets (a)');
ylabel('Density');
hold off
legend('High','Low')


% Scatter Plot - Excesso de Demanda e Precos
scatter( hist_q, hist_d)
xlabel( 'q')


