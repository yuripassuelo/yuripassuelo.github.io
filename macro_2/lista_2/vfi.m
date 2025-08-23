
% Iteracao da Funcao Valor
% - Recebe de Inputs:
%   1. beta   - propensao marginal a poupar
%   2. a_grid - grid de ativos
%   3. y_grid - grid de dotacoes
%   4. q      - Preco do ativo a
%   5. pi     - Matriz de Markov
%   6. u_func - Funcao utilidade
% - Retorna : Vetor de funcao Politica e funcao valor

function [V,ga] = vfi(beta,sigma,y_grid,a_grid,q,pi,M,N,V)
    % Função utilidade
    U = @(c) (c.^(1-sigma)) ./ (1-sigma);
    % Vetores
    TV = V;
    ga = V;
    %Iteracoes
    max_iter = 2000;
    tol      = 1e-5;
    dist     = 10;
    iter     = 0;

    % Iterate to solve the Bellman equation
    while dist > tol && iter < max_iter
        iter = iter + 1;
        for i = 1:M  % Loop over y_grid
            for j = 1:N  % Loop over a_grid
                c = (a_grid(j) + y_grid(i) - q * a_grid').*(a_grid(j) + y_grid(i) - q * a_grid' > 0) + eps.*(a_grid(j) + y_grid(i) - q * a_grid' < 0);
                value = U(c) + beta * V * pi(i,:)';
                [TV(j, i),pol] = max(value);
                ga(j, i) =  a_grid(pol);
            end
        end   
        dist = max(max(abs(TV - V)));
        V    = TV;
    end
    fprintf('Tol Achieved: %.10\n',max(max( abs( TV - V ))));
    fprintf('\nNum iter: %.0\n',iter);
end