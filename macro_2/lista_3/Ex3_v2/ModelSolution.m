% Funcao Para realizar a Bissecao e encontrar r que zere excesso de Demanda
%
% Tax_Opt - Indica aonde vamos introduzir a taxação
%
% b - Uma aliquota sobre Capital e Trabalho
% l - Aliquota somente sobre Trabalho
% k - Aliquota somente sobre Capital

function [V,gk,gc,stationary_dist,w,Kd,r0,t0,excDem,Y ] = ModelSolution(alpha,beta,gamma,delta,n_grid,k_grid,pi,N,M,Nbar,V,Tax_Opt,G)

    % Chutes Iniciais de \tau
    r0 = 0.2;
    t0 = 0.2;

    % Iteracoes Maximas
    maxIterEq = 100;
    % Tolerancia Equilibrio
    tolEq     = 0.01;
    dist      = 10;
    lambda    = 0.90;
    iter      = 0;

    % Opções de Taxação

    if Tax_Opt == 'b'
        pw = 1;
        pk = 1;
    elseif Tax_Opt == 'k'
        pw = 0;
        pk = 1;
    elseif Tax_Opt == 'l'
        pw = 1;
        pk = 0;
    end
       

    while dist > tolEq && iter < maxIterEq

        iter = iter + 1;

        [excDem, Y, V, gk,gc, stationary_dist, w, Kd, K,L] = ExcessDemand(alpha,beta,gamma,delta,pw*t0,pk*t0,n_grid,k_grid,pi,N,M,Nbar,r0,V);

        % Atualizando Juros

        ra = alpha*(K/L)^(alpha-1) - delta;

        % Atualizando Impostos

        ta = (G)/(pk*K*r0 + pw*L*w);

        % Medindo Distância
        dist = max( abs(ra-r0),abs(ta-t0) );

        disp( [iter, ra, ta, dist]);

        % Atualizando Juros e Taxas
        r0 = lambda*r0 + (1-lambda)*ra;
        t0 = lambda*t0 + (1-lambda)*ta;

    end


end