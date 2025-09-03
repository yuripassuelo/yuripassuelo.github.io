% Calculo do Excesso de Demanda

function [excDem, Y, V, gk,gc, stationary_dist, w, Kd, K,L] = ExcessDemand(alpha,beta,gamma,delta,tw,tk,n_grid,k_grid,pi,N,M,Nbar,r,V)

    % Demanda de Capital - Derivado de Pmgk 
    Kd = (alpha/(r+delta))^(1/(1-alpha))*Nbar;

    % Salario - Derivado da PmgL
    w  = (1-alpha)*(Kd/Nbar)^(alpha);

    % Iteracao sobre a funcao valor
    [V,gk,gc] = compute_policy(beta,gamma,tw,tk,n_grid,k_grid,pi,N,M,V,r,w );

    % Distribuição Invariante
    stationary_dist = compute_invariant_dist(gk, pi, M, N, k_grid);
    
    % Oferta de Capital
    Ks = sum( sum( stationary_dist .* gk ));
    
    % Excesso de Demanda
    excDem = (Ks - Kd)/((Ks + Kd) / 2);

    % Receita do Governo

    K = Ks;

    % Aqui não há escolha de trabalho, Oferta agregada é 1
    L = 1; 

    % PIB Da Economia
    % Consumo + Reposição do capital depreciado
    % sum( sum( stationary_dist .* gc )) + delta*K
    Y = (K^(alpha))*(L^(1-alpha));

end