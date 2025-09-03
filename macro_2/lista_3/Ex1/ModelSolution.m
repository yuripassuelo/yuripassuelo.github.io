% Funcao Para realizar a Bissecao e encontrar r que zere excesso de Demanda

function [V,gk,stationary_dist,w,Kd,Ea,r,excDem] = ModelSolution(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,Nbar,V)

    % Chutes Iniciais
    r0 = 0.001;
    r1 = 0.09;

    % Iteracoes Maximas
    maxIterEq = 100;
    tolEq     = 0.01;

    for iter = 1:maxIterEq

        rguess = (r0+r1)/2;

        [excDem, V, gk, stationary_dist, w, Kd, Ea] = ExcessDemand(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,Nbar,rguess,V);

        if abs(excDem) < tolEq
            break
        end
    
        if excDem < 0
            r0 = rguess;
        else
            r1 = rguess;
        end
    end

    r = (r0+r1)/2;
    fprintf('r = ',r);

end