%% Labor Search - McCall (1970) - Demissão

% parameters

beta  = 0.98;
b     = 0.01;
wBar  = 20;
pi    = 0.1;
sigma = 5;

% grid
N     = 1000;
wgrid = linspace(0,wBar,N);

u = @(c)(c.^(0.5));


% using linear distribution of w: f(w) = a1+a2w
% Item c)
% f(0) = a1 = 2f(W) = 2a1 + 40 a2
% f(W) = a1 + 20 a2
% Item d)
% 2f(0) = f(W)
% 2a1 = a1 + 20 a2

% Calculo das integrais por intervalo

a11 = 2/30;
a12 = -1/600;

a21 = 1/30;
a22 = 1/600;

f1 = @(w)( a11 + a12.*w) ;
f2 = @(w)( a21 + a22.*w) ;

F1 = f1(wgrid);
F2 = f2(wgrid);

den1 = zeros(1,N);
den2 = zeros(1,N);
denN = zeros(1,N);

for i = 2:N
    den1( i ) = integral( f1, wgrid(i-1), wgrid(i) ); 
    den2( i ) = integral( f2, wgrid(i-1), wgrid(i) );
    denN( i ) = 1/N;
end

plot(wgrid,den1);
hold on;
plot(wgrid,den2);
hold on;
plot(wgrid,denN);
hold off;

%% value function iteration

V = zeros(1,N); g = V; TV = V;

tic

[V1,g1] = compute_policy(V,TV,g,den1,beta,pi,N,b,wgrid);

[V2,g2] = compute_policy(V,TV,g,den2,beta,pi,N,b,wgrid);

[V3,g3] = compute_policy(V,TV,g,denN,beta,pi,N,b,wgrid);

toc

%% Reservation wage

pos1 = find(g1<2,1);
pos2 = find(g2<2,1);
pos3 = find(g3<2,1);

wStar1 = wgrid(pos1);
wStar2 = wgrid(pos2);
wStar3 = wgrid(pos3);

fprintf('\n Reservation wage: %.4f\n', wStar1);
fprintf('\n Reservation wage: %.4f\n', wStar2);
fprintf('\n Reservation wage: %.4f\n', wStar3);

%% plots

% Função Valor
figure (1)
plot(wgrid,V1,'LineWidth', 2)
hold on
plot(wgrid,V2,'LineWidth', 2)
hold on
plot(wgrid,V3,'LineWidth', 2)
grid on;
legend('$f(w) = \frac{1}{30} + \frac{1}{600}w$','$f(w) = \frac{2}{30} - \frac{1}{600}w$','$f(w)=\frac{1}{20}$','interpreter','latex');
xlabel('w','interpreter','latex');
ylabel('Value function','interpreter','latex');
ax = gca;
exportgraphics(ax,'C:\Users\yurim\Desktop\Mestrado\2S2024\Macroeconomia 2\Listas\Lista 4\Ex1\figs\Plot_V1.pdf','Resolution',300)


% Função Politíca
figure (2)
plot(wgrid,(g1-2)*(-1),'LineWidth', 2 )
hold on;
plot(wgrid,(g2-2)*(-1),'LineWidth', 2 )
hold on;
plot(wgrid,(g3-2)*(-1),'LineWidth', 2 )
grid on;
legend('$f(w) = \frac{1}{30} + \frac{1}{600}w$','$f(w) = \frac{2}{30} - \frac{1}{600}w$','$f(w)=\frac{1}{20}$','interpreter','latex');
xlabel('w','interpreter','latex');
ylabel('Policy function','interpreter','latex');
ax = gca;
exportgraphics(ax,'C:\Users\yurim\Desktop\Mestrado\2S2024\Macroeconomia 2\Listas\Lista 4\Ex1\figs\Plot_p1.pdf','Resolution',300)

