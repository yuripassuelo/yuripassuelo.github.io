% Iteracao sobre a funcao valor

function [V,gk,gc] = compute_policy(beta,gamma,tw,tk,n_grid,k_grid,pi,N,M,V,r,w)
    % Funcao Utilidade
    util = @(c) (c.^(1-gamma))./(1-gamma);
    % Pre Alocando Operador de Bellman e F. pol igual a V
    Tv   = V;
    gk   = V;
    gc   = V;
    % Parametros Iniciais Para Convergência
    dist     = 10;
    iter_max = 1000;
    tol      = 1e-5;
    it       = 0;

    % Iteracao por meio do While

    while dist > tol && it < iter_max
        it = it + 1;

        for i = 1:M
            for j = 1:N
                % Consumo
                c = ((1-tw)*w*n_grid(i) + (1+r*(1-tk))*k_grid(j) - k_grid').*((1-tw)*w*n_grid(i) + (1+r*(1-tk))*k_grid(j) - k_grid' > 0 ) + eps.*((1-tw)*w*n_grid(i) + (1+r*(1-tk))*k_grid(j) - k_grid' <= 0 );
                %c = c .* (c>0) + eps .*(c<=0);
                value = util( c ) + beta * V * pi(i,:)' ;
                [Tv(j,i),pol ] = max(value);
                gk(j,i) = k_grid(pol);
                gc(j,i) = c(pol);
            
            end
        end
        dist = max(max( abs( Tv - V )));
        V    = Tv;
    end
    fprintf('Tol Achieved: %.10\n',max(max( abs( Tv - V ))));
    fprintf('\nNum iter: %.0\n',it);
end