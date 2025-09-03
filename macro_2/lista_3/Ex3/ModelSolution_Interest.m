% Funcao Para realizar a Bissecao e encontrar r que zere excesso de Demanda
% para os Juros
function [V,gk,stationary_dist_k,w,kd,r,excDem,govBal] = ModelSolution_Interest(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,tau1,tau2,G)
    % Chutes Iniciais
    r0 = 0.001;
    r1 = 0.2;
    % Iteracoes Maximas
    maxIterEq = 100;
    tolEq     = 0.001;
    % Incluimos O loop sobre de trabalho
    for iter = 1:maxIterEq
        %
        rguess = (r0+r1)/2;
        % Calcula Excesso de demanda
        [excDem, govBal, V, gk, stationary_dist_k, w, kd] = ExcessDemand(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,rguess,V,tau1,tau2,G);
        disp(["Iter Cap: ",iter," ; Exc Dem: ",excDem," ; Gov Bal: ",govBal]);
        % Checagem da tolerancia
        if abs(excDem) < tolEq
            break
        end
        % Atualização da Bisseção
        if excDem < 0
            r0 = rguess;
        else
            r1 = rguess;
        end
    end
    r = (r0+r1)/2;
    disp(['r = ',r]);
end