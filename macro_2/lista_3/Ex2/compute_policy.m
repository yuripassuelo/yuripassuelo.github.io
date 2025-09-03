% Iteracao sobre a funcao valor

function [V,gk,gl] = compute_policy(beta,gamma,theta,eta,l_grid,n_grid,k_grid,pi,N,M,L,V,r,w)
    % Funcao Utilidade
    util = @(c,l) ((c.^(1-gamma))./(1-gamma) - theta*(l.^(1+eta))./(1+eta) );
    % Pre Alocando Operador de Bellman e F. pol igual a V
    Tv   = V;
    gk   = V;
    gl   = V;
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
                Lv = zeros(L,1);
                Lp = zeros(L,1);
                for k = 1:L
                % Consumo
                    c = (w*l_grid(k)*n_grid(i) + (1+r)*k_grid(j) - k_grid').*(w*l_grid(k)*n_grid(i) + (1+r)*k_grid(j) - k_grid' > 0 ) + eps.*(w*l_grid(k)*n_grid(i) + (1+r)*k_grid(j) - k_grid' <= 0 );
                    %c = c .* (c>0) + eps .*(c<=0);
                    value = util( c, l_grid(k) ) + beta * V * pi(i,:)' ;
                    [Lv(k,1), Lp(k,1)] = max( value );   
                end
                %
                [Tv(j,i),pol_l ] = max(Lv);
                gk(j,i) = k_grid( Lp(pol_l,1) );
                gl(j,i) = l_grid( pol_l );
            end
        end
        dist = max(max( abs( Tv - V )));
        %disp([it, dist])
        V    = Tv;
    end
    %fprintf('Tol Achieved: %.10\n',max(max( abs( Tv - V ))));
    %fprintf('\nNum iter: %.0\n',it);
end