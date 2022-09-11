function y=MfunE(X,xdata)
xdata=xdata';
if min(X(2)-X(3)*xdata.^2)>=0
  y=X(1)*sqrt(X(2)-X(3)*xdata.^2)+X(4);
else
  y=zeros(size(xdata));  
end