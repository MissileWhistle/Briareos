function ATR=ATR(H,L,C,n,k,p)
TR=max([H-L,abs(H-C),abs(L-C)],[],2);
AT=zeros(size(H));
for i=1:size(H)-n+1
    AT(i+n-1)=(1/n)*sum(TR(i:i+n-1));
end
MT=movavg(AT,"exponential",k);
MT(isnan(MT))=0;
ST=AT-MT;
AR=(sign(ST(p:end)).*sign((C(p:end)-C(1:end-p+1))./C(1:end-p+1))+1)/2;
ATR=[zeros(p-1,1); AR];