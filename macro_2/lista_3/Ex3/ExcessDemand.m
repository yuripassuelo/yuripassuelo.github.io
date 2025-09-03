% Computando Excesso de Demanda

function [excDem, govBal, V, gk, stationary_dist_k, w, kd ] = ExcessDemand(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,r,V,tau1,tau2,G)
    
    % Excesso de Demanda
    kd = ((r+delta)/(alpha))^(1/(alpha-1));

    % Salario - Derivado da PmgL
    w  = (1-alpha)*(kd)^(alpha);

    % Calculo da Oferta de Capital - VFI

    [V,gk] = compute_policy(beta,gamma,n_grid,k_grid,pi,N,M,V,r,w,tau1,tau2 );

    % Distribuição Invariante
    [stationary_dist_k ] = compute_invariant_dist(gk,pi,M,N,k_grid);

    Ks = sum( sum( stationary_dist_k .* gk ));
    Ls = sum( sum( stationary_dist_k .* n_grid ));
    
    % Excesso de Demanda de Capital
    excDem = ((Ks/Ls) - kd)/(( (Ks/Ls) + kd) / 2);
    
    % Orçamento do Governo
    govBal = r*tau1*Ks + w*tau2*Ls - G;
end