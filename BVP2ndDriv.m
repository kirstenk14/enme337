function [y] = BVP2ndDriv(a, b, Ya, Db, n, pOFx, qOFx, rOFx)

h=(b-a)/n;
A=zeros(1,n-1);
B=zeros(1,n-1);
C=zeros(1,n-1);
D=zeros(1,n-1);
coeff=zeros((n-1));
const=zeros((n-1),1);

    for i=1:1:(n-1)
    % populating A,B,C,D vals for the matrix of coeffs
    D(i) = (2+(h^2)*qOFx(i+1));
    C(i) = -(1-(h/2)*pOFx(i+1));
    B(i) = -(h^2)*rOFx(i+1);
    A(i) = -(1+(h/2)*pOFx(i+1));
    
    end
    
    for k=1:1:(n-1)
    % populating vertical 'b' vector for Ax=b
        if k==1
          const(k,1) = B(1) - A(1)*Ya; 
        elseif k==(n-1)
          const(k,1) = B(k) - (2*C(k)*Db*h)/3; 
        else 
            const(k,1)= B(k);
        end
    end
    
    for row=1:1:(n-2)  % populating coeff 'A' matrix with A,B,C,D vals
        for col=1:1:(n-1)
            if row==col-1 
                coeff(row,col) = A(row);
            end
            if row==col
                coeff(row,col) = D(row);
            end
            if row==col+1
                coeff(row,col) = C(row);
            end
        end
    end
    
    for p=(n-2):1:(n-1)
        if p==(n-2)
            coeff((n-1),p) = A(n-1)-(C(n-1)/3);
        else
            coeff((n-1),p) = D(n-1)+(4/3)*C(n-1);
        end
    end

y = coeff\const;
yNplus1 = (2*h*Db+4*y(n-1)-y(n-2))/3;
y = [Ya;y;yNplus1];
end


