function y=MfunS(X,xdata)
xdata=xdata';
if min(X(2)+X(3)*xdata)>=0
  y=X(1)*sqrt(X(2)+X(3)*xdata)+X(4);
else
  y=zeros(size(xdata));  
end