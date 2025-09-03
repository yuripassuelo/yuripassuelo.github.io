% Computacao da distribuicao Invariante

function stationary_dist = compute_invariant_dist(gk, pi, M, N, k_grid)

    % Loop que preenche matrizes
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
    
    stationary_dist = SS^1000;
    stationary_dist = stationary_dist(1,:);
    stationary_dist = reshape( stationary_dist,N,M ); % [stationary_dist(1:N)',stationary_dist(N+1:end)'];

end