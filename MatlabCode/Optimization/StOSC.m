function [Osc,RSI]=StOSC(C,f,s)
RSI=zeros(size(C));
rC=[0;tick2ret(C)];
PG=0;
PL=0;
for i=f:size(C,1)
    prC=rC(i-f+1:i);
    CG=mean(prC(prC>0));
    CL=(mean(prC(prC<0)));
    RSI(i)=100-(100/(1+((PG*13 + CG)/(PL*13 + CL))));
    PG=CG;
    PL=CL;
end

Osc=zeros(size(C));
for i=s+f:size(C,1)
    Osc(i)=(RSI(i)-min(RSI(i-s+1:i)))/(max(RSI(i-s+1:i))-min(RSI(i-s+1:i)));
end