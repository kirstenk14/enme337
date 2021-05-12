clc;

a=1;
b=3;
n=50;
h=(b-a)/n;
Xarr = (a:h:b);
Ya=1;
Db=-1.2;

pOFx = @(x)(1/Xarr(x));
qOFx = @(x)(0);
rOFx = @(x)(-10);

% Discretizing the ODE
% d2y_dx2 = (y(i-1)-2*y(i)+y(i+1))/h^2;
% dy_dx = (y(i+1)-y(i-1))/2*h; 
% Discretized Form:
% yi1*(1-(h/2)*pOFx(i))+yi*(2+(h^2)*qOFx(i))- yi_1)*(1+(h/2)*pOFx(i)) = -(h^2)*rOFx(i)  ;
 
[y] = BVP2ndDriv(a, b, Ya, Db, n, pOFx, qOFx, rOFx);

plot(Xarr,y,'-')
title('BVP plotted y=f(x)')
grid on







