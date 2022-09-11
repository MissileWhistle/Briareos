function Mre=MfunF1(X,x)
x=x';
Mre=X(1)*cos(X(3)*x+X(5))+X(2)*sin(X(4)*x+X(6))+X(7);
end