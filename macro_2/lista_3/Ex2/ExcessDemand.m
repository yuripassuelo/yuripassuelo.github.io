% Computando Excesso de Demanda

function [excDem, V, gk, gl, stationary_dist, w, Kd, Ks, Ls] = ExcessDemand(alpha,beta,gamma,theta,eta,delta,l_grid,n_grid,k_grid,pi,N,M,L,Nbar,r,V)

    % Demanda de Capital - Derivado de Pmgk 
    Kd = (alpha/(r+delta))^(1/(1-alpha))*Nbar;

    % Salario - Derivado da PmgL
    w  = (1-alpha)*(Kd/Nbar)^(alpha);

    % Calculo da Oferta de Capital - VFI

    [V,gk,gl] = compute_policy(beta,gamma,theta,eta,l_grid,n_grid,k_grid,pi,N,M,L,V,r,w);

    % Distribuição Invariante
    stationary_dist = compute_invariant_dist(gk, pi, M, N, k_grid);
    
    % Oferta de Capital
    Ks = sum( sum( stationary_dist .* gk ));
    % Oferta de Trabalho
    Ls = sum( sum( stationary_dist .* gl ) .* n_grid );

    % Calcula Excesso de Demanda
    excDem = ( (Ks/Ls) - Kd)/(( (Ks/Ls) + Kd) / 2);

end