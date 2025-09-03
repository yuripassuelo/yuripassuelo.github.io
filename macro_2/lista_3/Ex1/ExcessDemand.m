% Computando Excesso de Demanda

function [excDem, V, gk, stationary_dist, w, Kd, Ea] = ExcessDemand(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,Nbar,r,V)

    % Demanda de Capital - Derivado de Pmgk 
    Kd = (alpha/(r+delta))^(1/(1-alpha))*Nbar;

    % Salario - Derivado da PmgL
    w  = (1-alpha)*(Kd/Nbar)^(alpha);

    % Calculo da Oferta de Capital - VFI

    [V,gk] = compute_policy(beta,gamma,n_grid,k_grid,pi,N,M,V,r,w );

    % Distribuição Invariante
    stationary_dist = compute_invariant_dist(gk, pi, M, N, k_grid);

    Ea = sum( sum( stationary_dist .* gk ));
    excDem = (Ea - Kd)/((Ea + Kd) / 2);

end