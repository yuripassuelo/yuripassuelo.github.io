% Funcao distribuicao Invariante

function [stationary_dist_k] = compute_invariant_dist(gk, pi, M, N, k_grid )
    % Loop que preenche matrizes Para Capital
    for k = 1:M
        Ai = zeros( N );
        for i = 1:N
            for j = 1:N
                Ai(i,j) = gk(i,k) == k_grid(j);
            end
        end
        eval( ['A' num2str(k) ' =  Ai ;']);
    end
    % Criando matriz M:
    C = cell( M );
    % Preenchimento
    for row = 1:M
        for col = 1:M
            C{row,col} = pi(row,col) .* eval(['A' num2str(row)]);
        end
    end
    % Conversão para matriz
    SS = cell2mat( C );
    % Calculando distribuição estacionaria
    stationary_dist_k = SS^1000;
    stationary_dist_k = stationary_dist_k(1,:);
    stationary_dist_k = reshape( stationary_dist_k,N,M ); % [stationary_dist(1:N)',stationary_dist(N+1:end)'];
end