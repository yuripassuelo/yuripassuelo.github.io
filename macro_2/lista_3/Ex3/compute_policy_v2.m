
% Versão que Computa a Policie na versão Reduzida (Teoricamente mais
% rapida)
% Assumimos que u(c,l) aqui é:


function [V,gk,gl] = compute_policy_v2(beta,gamma,theta,eta,l_grid,n_grid,k_grid,pi,N,M,V,r,w)
    % Funcao Utilidade
    util = @(c,l) ((c.^(1-gamma))./(1-gamma) - theta.*((l.^(1+eta))./(1+eta) ));
    % Pre Alocando Operador de Bellman e F. pol igual a V
    Tv   = V;
    gk   = V;
    gl   = V;
    % Parametros Iniciais Para Convergência
    dist     = 10;
    iter_max = 1000;
    tol      = 1e-5;
    it       = 0;
    % Combinacoes de k' e l
    Cb = combvec( k_grid, l_grid);
    % Combinacoes de

    % Iteracao por meio do While

    while dist > tol && it < iter_max
        it = it + 1;
        %disp( dist );
        for i = 1:M
            for j = 1:N
                c = (w*n_grid(i)*Cb(2,:) + (1+r)*k_grid(j) - Cb(1,:)).*(w*n_grid(i)*Cb(2,:) + (1+r)*k_grid(j) - Cb(1,:) > 0 ) + eps.*(w*n_grid(i)*Cb(2,:) + (1+r)*k_grid(j) - Cb(1,:) <= 0 );
                Evs = combvec( (beta * V * pi(i,:)')', l_grid);
                value = util( c, Cb(2,:) ) + Evs(1,:) ;
           
                [Tv(j,i), pol ] = max( value );
                gk(j,i) = Cb(1,pol);
                gl(j,i) = Cb(2,pol);
            end
        end
        dist = max(max( abs( Tv - V )));
        V    = Tv;
    end
    fprintf('Tol Achieved: %.10\n',max(max( abs( Tv - V ))));
    fprintf('\nNum iter: %.0\n',it);
end


