clc;
format long g
Fun=@(x)(exp(-x^2));
a = 0;
b = 3;

I = GuassQuad5ab(Fun,a,b);
disp("Gauss Quadrature 5 point Method: I = " + I);
