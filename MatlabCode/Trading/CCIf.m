function [Osc]=CCIf(H,L,C,p,k)
TP=zeros(size(H));
MA=zeros(size(H));
MD=zeros(size(H));
for i=max(p,k):size(H,1)
    TP(i) = sum((H(i-p+1:i)+L(i-p+1:i)+C(i-p+1:i)))/(3);
    MA(i) = sum(TP(i-k+1:i))/k;
    MD(i) = sum(abs(TP(i-p+1:i)-MA(i-p+1:i)))/p;
end
CCI=(TP-MA)./(0.015*MD);
CCI(isnan(CCI))=0;

Osc=zeros(size(C));
for i=p+k:size(C,1)
    Osc(i)=(CCI(i)-min(CCI(i-p+1:i)))/(max(CCI(i-p+1:i))-min(CCI(i-p+1:i)));
end
