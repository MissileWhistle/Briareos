function [SPortd,LPortd,LAPort,SAPort,LPortSD,SPortSD]=PortfolioOpt(t, ...
    daycount,SGSg,LGSg,Pd,sPd,TotalFunds1,PDExp,PPar,STP,LTP,simag,limag)

Pdsize2=size(Pd,2);

% Portfolio Covariance matrix
PDce=zeros(2*t-1,Pdsize2);
for i=1:(2*t-1)
  PDce(i,:)=(Pd(i+1,:)-Pd(i,:))./Pd(i,:);
end
CovP=cov(PDce);

% Long/Short Portfolio Division
if 1   % daycount < t
    SPortd=1;
    LPortd=0;
else
    SPP=(sum((1/Pdsize2)*SGSg.*tick2ret(sPd),2));
    LPP=(sum((1/Pdsize2)*LGSg.*tick2ret(sPd),2));
    SP=cumsum(SPP);
    LP=cumsum(LPP);
    A=[];
    b=[];
    Aeq=ones(1,2);
    beq=1;
    lb=zeros(1,2);
    ub=ones(1,2);
    x0=0.5*ones(1,2);
    Portd= @(X) -((round(X,3)*[SP(end); LP(end)])-(round(X,3)*sqrt([var(SPP); var(LPP)]))+((1+sqrt(round(X,3)))*(1+sqrt(round(X,3)')))); 
    portd=fmincon(Portd,x0,A,b,Aeq,beq,lb,ub);
    SPortd=round(portd(1)*(1/0.20))*0.20;
    LPortd=round(portd(2)*(1/0.20))*0.20;
    if SPortd+LPortd<1
        exx=1-SPortd+LPortd;
        SPortd=SPortd+exx;
    end
    if SPortd+LPortd>1
        exx=SPortd+LPortd-1;
        LPortd=LPortd-exx;
    end
    SPortd=round(SPortd,2); % round dependent on general rounding scheme
    LPortd=round(LPortd,2); % round dependent on general rounding scheme
end


AssetScenarios = mvnrnd(PDExp, CovP, 20000);
p = PortfolioMAD;
p = setScenarios(p, AssetScenarios);
p = setDefaultConstraints(p);
pwgt = estimateFrontier(p);
prsk = sqrt(estimatePortRisk(p, pwgt));
pret = estimatePortReturn(p, pwgt);
sptrd = mean(pwgt.*STP);
lptrd = mean(pwgt.*LTP);
Limag= mean(pwgt.*limag');
Simag = mean(pwgt.*simag');
ppar = mean(pwgt.*PPar');

[~,LI]=max((pret' .* lptrd .* ppar) ./ (prsk' .* Limag));
[~,SI]=max((pret' .* sptrd .* ppar) ./ (prsk' .* Simag));

SAPort=transpose(round(pwgt(:,SI)*(1/0.125))*0.125);
disp("SAPortO="),disp(SAPort)
if sum(SAPort)<1
    exx=1-sum(SAPort);
    sclr=exx/0.125;
    ind=SAPort>0;
    ma=maxk(PDExp(ind),sclr);
    I=[];
    for i=1:size(ma,2)
        [~,c]=find(PDExp==ma(i));
        I(i)=c;
    end
    SAPort(I)=SAPort(I)+0.125;
end
if sum(SAPort)>1
    exx=sum(SAPort)-1;
    sclr=exx/0.125;
    ind=SAPort>0;
    ma=mink(PDExp(ind),sclr);
    I=[];
    for i=1:size(ma,2)
        [~,c]=find(PDExp==ma(i));
        I(i)=c;
    end
    SAPort(I)=SAPort(I)-0.125;
end
disp("SAPort="),disp(SAPort) 
    
LAPort=transpose(round(pwgt(:,LI)*(1/0.125))*0.125);
disp("LAPortO="),disp(LAPort)
if sum(LAPort)<1
    Arisk=diag(CovP);
    exx=1-sum(LAPort);
    sclr=exx/0.125;
    ind=LAPort>0;
    shper=PDExp./Arisk';
    shper(isnan(shper))=0;
    shper(isinf(shper))=0;
    ma=maxk(shper(ind),sclr);
    I=[];
    for i=1:size(ma,2)
        [~,c]=find(shper==ma(i));
        I(i)=c;
    end
    LAPort(I)=LAPort(I)+0.125;
end
if sum(LAPort)>1
    Arisk=diag(CovP);
    exx=sum(LAPort)-1;
    sclr=exx/0.125;
    ind=LAPort>0;
    shper=PDExp./Arisk';
    shper(isnan(shper))=0;
    shper(isinf(shper))=0;
    ma=mink(shper(ind),sclr);
    I=[];
    for i=1:size(ma,2)
        [~,c]=find(shper==ma(i));
        I(i)=c;
    end
    LAPort(I)=LAPort(I)-0.125;
end
disp("LAPort="),disp(LAPort)
% current rounding scheme permits a minimum portfolio value of 400$ 

% Portfolios deviation
LPortSD=Pvar(LPortd*TotalFunds1*LAPort,CovP); 
                                       
SPortSD=Pvar(SPortd*TotalFunds1*SAPort,CovP); 
end