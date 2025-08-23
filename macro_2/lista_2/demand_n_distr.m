
% Distribuicao Estacionaria e Excesso de demanda
% - Recebe de inputs
%   1. pol_a  - Vetor de funcao politica para cada estado
%   2. a_grid - Grid de a's possiveis
%   3. pi     - Distribuicao  de Markov
% - Retorna : Vetor de distribuicao estacionaria e vetor de excesso de
% demanda

function [stat_dist, demand_excess ] = demand_n_distr( ga, a_grid, pi,N,M )
    % Matriz de zeros que sera preenchida
    Ai = zeros( N );
    
    % Loop que preenche matrizes
    for k = 1:M
        Ai = zeros( N );
        for i = 1:N
            for j = 1:N
                Ai(i,j) = ga(i,k) == a_grid(j);
            end
        end
        eval( ['A' num2str(k) ' =  Ai ;']);
    end

    % Criando matriz M:
    SS = cell( M );

    % Preenchimento
    for row = 1:M
        for col = 1:M
            SS{row,col} = pi(row,col) .* eval(['A' num2str(row)]);
        end
    end

    % Conversão para matriz
    SS = cell2mat( SS );

    % Computando dist. Estacionaria:
    stat_dist = SS^1000;
    stat_dist = stat_dist(1, :);
    stat_dist = reshape(stat_dist, N,M);

    % Computando Excesso de demanda:
    demand_excess = -sum(sum(stat_dist .* ga));

end

