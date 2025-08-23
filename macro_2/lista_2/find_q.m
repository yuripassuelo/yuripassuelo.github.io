
% Encontra Q em sinal Oposto para Iniciar Bicessao
% - Recebe Inputs:
%   1. excess_deman - Excesso de Demanda
%   2. q0           - Preco Inicial
%   3. 
%   4.
%   5. i = 0.5      - Forca de Correcao
% - Retorna : qt ajustado para iniciar bissecao

function [ qt, d_excess_1 ] = find_q(d_excess,q0,y_grid,beta,sigma,a_grid,pi,V,M,N,price_i )

    % Para dado preco Input de preco q0, vamos buscar um outro qt tal que
    % nos permita partir para a bissecao

    % Regra é primeiro analisar o preço e sua relacao com o excesso de
    % demanda, caso o excesso de demanda seja positivo:
    %   1. Temos que aumentar o preco: qt = (1 - prc )*q
    % Caso o excesso seja negativo
    %   2. Temos que aumentar o preco: qt = (1 + prc )*q

    if d_excess > 0
        correction = 1 - price_i;
        sign       = '>';
    else
        correction = 1 + price_i;
        sign       = '<';
    end

    % Procura q Inicial
    qt = q0;
    d_excess_1 = d_excess;

    while eval([ num2str(d_excess_1) sign '0'])

        qt = correction .* qt;

        [V, a_pol   ] = vfi(beta,sigma,y_grid,a_grid,qt,pi,M,N,V);

        [~, d_excess_1] = demand_n_distr(a_pol,a_grid, pi, N, M);
        
        disp( qt );
        disp( d_excess_1 );

    end
end