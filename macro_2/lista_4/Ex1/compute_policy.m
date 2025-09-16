
% Iteração da Função valor - Job Search com Demissão
% Obs: Oferta é certa

function [V,g] = compute_policy(V,TV,g,den,beta,pi,N,b,wgrid)

    u = @(c)(c.^(0.5));

    dist = 10;
    tol = 1E-5;
    it  = 0;
    itmax = 1000;

    while dist>tol && it<itmax
        it = it + 1;
        U = u(b) + beta*sum(V.*den) ;
        for i=1:N
            [TV(i),g(i)] = max([ (u(wgrid(i)) + beta*pi*sum(V.*den))/(1-beta*(1-pi)),U]);
        end
        dist = max(abs(TV-V));
        %disp(dist);
        V = TV;
    end


end