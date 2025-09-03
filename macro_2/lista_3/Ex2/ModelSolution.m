% Funcao Para realizar a Bissecao e encontrar r que zere excesso de Demanda

function [V,gk,gl,stationary_dist,w,Kd,Ks,Ls,r,excDem] = ModelSolution(alpha,beta,gamma,theta,eta,delta,l_grid,n_grid,k_grid,pi,N,M,L,Nbar,V)

    % Chutes Iniciais
    r0 = 0.001;
    r1 = 0.09;

    % Iteracoes Maximas
    maxIterEq = 100;
    tolEq     = 0.01;

    for iter = 1:maxIterEq
        % Atualização do Chute
        rguess = (r0+r1)/2;
        %
        [excDem, V, gk, gl, stationary_dist, w, Kd, Ks, Ls] = ExcessDemand(alpha,beta,gamma,theta,eta,delta,l_grid,n_grid,k_grid,pi,N,M,L,Nbar,rguess,V);
        % Display da Iteração e do Excesso de Demanda
        disp([iter, excDem]);
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
    %fprintf('r = ',r);

end