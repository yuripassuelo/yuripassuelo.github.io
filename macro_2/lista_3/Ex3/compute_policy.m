% Iteracao sobre a funcao valor

function [V,gk] = compute_policy(beta,gamma,n_grid,k_grid,pi,N,M,V,r,w,tau1,tau2)
    % Funcao Utilidade
    util = @(c) ((c.^(1-gamma))./(1-gamma));
    % Pre Alocando Operador de Bellman e F. pol igual a V
    Tv   = V;
    gk   = V;
    % Parametros Iniciais Para Convergência
    dist     = 10;
    iter_max = 1000;
    tol      = 1e-5;
    it       = 0;
    % Iteracao por meio do While
    while dist > tol && it < iter_max
        % Contador iteração
        it = it + 1;
        for i = 1:M
            for j = 1:N
                % Calculo Consumo
                c = ((1-tau1)*w*n_grid(i) + (1+r*(1-tau2))*k_grid(j) - k_grid').*((1-tau1)*w*n_grid(i) + (1+r*(1-tau2))*k_grid(j) - k_grid' > 0 ) + eps.*((1-tau1)*w*n_grid(i) + (1+r*(1-tau2))*k_grid(j) - k_grid' <= 0 );
                value = util( c ) + beta * V * pi(i,:)' ;
                % Função valor e Politica
                [Tv(j,i), pol ] = max( value );
                gk(j,i) = k_grid(pol);
            end
        end
        dist = max(max( abs( Tv - V )));
        V    = Tv;
    end
    %fprintf('Tol Achieved: %.10\n',max(max( abs( Tv - V ))));
    %fprintf('\nNum iter: %.0\n',it);
end