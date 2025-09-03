% Funcao Para realizar a Bissecao e encontrar r que zere excesso de Demanda
% para os Juros
function [V,gk,stationary_dist_k,w,kd,r,t,excDem,govBal] = ModelSolution_Gov(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,G,tipo_tau)
    % Tipo de Taxação
    if tipo_tau == "k"
        pk = 1;
        pl = 0;
    elseif tipo_tau == "l"
        pk = 0;
        pl = 1;
    elseif tipo_tau == "b"
        pk = 1;
        pl = 1;
    end
    % Chutes Iniciais
    t0 = 0.01;
    t1 = 0.7;
    % Iteracoes Maximas
    maxIterEq = 100;
    tolEq     = 0.001;
    % Incluimos O loop sobre de trabalho
    for iter_gov = 1:maxIterEq
        %
        tguess = (t0+t1)/2;
        % Calcula Excesso de demanda
        [V,gk,stationary_dist_k,w,kd,r,excDem,govBal] = ModelSolution_Interest(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,V,pk*tguess,pl*tguess,G);
        % Display das iterações
        %disp(["Iter Gov: ",iter_gov," ; Gov Bal: ",govBal]);
        % Checagem da tolerancia
        if abs(govBal) < tolEq
            break
        end
        % Atualização da Bisseção
        if excDem < 0
            t0 = tguess;
        else
            t1 = tguess;
        end
    end
    t = (t0+t1)/2;
    disp(['t = ',t]);
end