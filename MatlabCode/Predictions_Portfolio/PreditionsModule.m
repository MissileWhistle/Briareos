function [CFTA, MdR, MdRvar, MdRExp, MEMpredi, Pdr1, Pdr2, Pdr3, ...
    Pdr4, Pdr5, Pdr6, Pdr7, PDvar, PDExp, PPMpredi, ...
    Predicts, n]=PreditionsModule(t,MDIFull,Mi,lMd,lPd,lPdv,Par)

%% M.E.M(Macro Econ. Prediction Module):
Misize2=size(Mi,2);
Pdsize2=size(lPd,2);
Pdsize1=size(lPd,1);
MDIsize2=size(MDIFull,2);

%% MDIFull Smooth and Data Transf.

SMT=[1:128; std(tick2ret(MDIFull))];
SSMT=sortrows(SMT',2);
IND=SSMT(:,1);
VAL=SSMT(:,2);
A1=IND(VAL<0.02);
A2=IND(VAL>=0.02 & VAL<0.09);
A3=IND(VAL>=0.09 & VAL<0.2);
A4=IND(VAL>=0.2 & VAL<0.4);
A5=IND(VAL>=0.4 & VAL<0.6);
A6=IND(VAL>=0.6 & VAL<1);
A7=IND(VAL>=1);

SMdiFull=zeros(size(MDIFull));
for i=1:MDIsize2
    if ismember(i,A1)==1
        SMdiFull(:,i)=MDIFull(:,i);
    elseif ismember(i,A2)==1
        SMdiFull(:,i)=smoothdata(MDIFull(:,i),'gaussian',3);
    elseif ismember(i,A3)==1
        SMdiFull(:,i)=smoothdata(MDIFull(:,i),'gaussian',5);
    elseif ismember(i,A4)==1
        SMdiFull(:,i)=smoothdata(MDIFull(:,i),'gaussian',7);
    elseif ismember(i,A5)==1
        SMdiFull(:,i)=smoothdata(MDIFull(:,i),'gaussian',9);
    elseif ismember(i,A6)==1
        SMdiFull(:,i)=smoothdata(MDIFull(:,i),'gaussian',11);
    elseif ismember(i,A7)==1
        SMdiFull(:,i)=smoothdata(MDIFull(:,i),'gaussian',13);
    end
end

SMdiA=Dat_trans_v2(MDIFull);
SMdiAsize2=size(SMdiA,2);

Md=log(lMd);
Pd(:,1)=log(lPd(:,1));
Pd(:,2)=log(lPd(:,2));
Pd(:,3)=log(lPd(:,3))+15;
Pd(:,4)=log(lPd(:,4))+3;
Pd(:,5)=log(lPd(:,5))+15;
Pd(:,6)=log(lPd(:,6))+7;
Pd(:,7)=log(lPd(:,7))+7;

n=3000;
%% Correlations & Lags (MiA)

C=zeros(1,Misize2);
L=zeros(1,Misize2);
for i=1:Misize2
  [r,lags]=crosscorr(tick2ret(Md+1),tick2ret(SMdiA{1}(end-7*t+1:end,i)+1),2*t);
  [~,I]=max(abs(r));
  l=lags(I);
  C(1,i)=r(I);
  L(1,i)=-l;
end 

Ct=(L>=0 & abs(C)>0.3);

%% Curve Fit

xdata=1:2*t;
cftlb=xdata(end);

SMdi=zeros(cftlb,MDIsize2);
for i=1:MDIsize2
    SMdi(:,i)=SMdiFull(end-cftlb+1:end,i);
end

Mdisubt=SMdi;

CFStruct=zeros(3,MDIsize2);
lb=[];
ub=[];
errCF=zeros(MDIsize2,4);
MparF=cell(MDIsize2,3);
MparS=cell(MDIsize2,3);
MparE=cell(MDIsize2,3);
MparL=cell(MDIsize2,3);

s=1;
for i=1:MDIsize2
    x1=[1 Mdisubt(1,i)];
    [MparL{i,s}]=lsqcurvefit(@MfunL,x1,xdata,Mdisubt(:,i));
end

for i=1:MDIsize2
    Mdisubt(:,i)=Mdisubt(:,i)-MfunL(MparL{i,s},xdata);
    CFStruct(1,i)=4;
end

s=2;
for i=1:MDIsize2
    x0=[std(Mdisubt(:,i)) std(Mdisubt(:,i)) 1 1 0 0 Mdisubt(1,i)];
    x1=[1 0 1 Mdisubt(1,i)];
    x2=[1 0 1 Mdisubt(1,i)];
    x3=[1 Mdisubt(1,i)];
    ms= MultiStart('UseParallel',true);
    options=optimoptions(@lsqcurvefit,'Algorithm',...
    'levenberg-marquardt','MaxFunEvals',200*7,'MaxIterations',800);
    problemf= createOptimProblem('lsqcurvefit','objective',@MfunF1,...
        'x0',x0,'xdata',xdata,'ydata',Mdisubt(:,i),'lb',lb,'ub',ub,'options',options);
    [MparF{i,s}, errf]=run(ms,problemf,100);
    
    ms= MultiStart('UseParallel',true);
    options=optimoptions(@lsqcurvefit,'Algorithm',...
    'levenberg-marquardt','MaxFunEvals',200*7);
    probleme= createOptimProblem('lsqcurvefit','objective',@MfunE,...
        'x0',x1,'xdata',xdata,'ydata',Mdisubt(:,i),'lb',lb,'ub',ub,'options',options);
    [MparE{i,s}, erre]=run(ms,probleme,100);
    
    ms= MultiStart('UseParallel',true);
    options=optimoptions(@lsqcurvefit,'Algorithm',...
    'levenberg-marquardt','MaxFunEvals',200*7);
    problems= createOptimProblem('lsqcurvefit','objective',@MfunS,...
        'x0',x2,'xdata',xdata,'ydata',Mdisubt(:,i),'lb',lb,'ub',ub,'options',options);
    [MparS{i,s}, errs]=run(ms,problems,100);
    
    [MparL{i,s}, errl]=lsqcurvefit(@MfunL,x3,xdata,Mdisubt(:,i));
    errCF(i,:)=[errf erre errs errl];
end

for i=1:MDIsize2
   [~,I]=min(errCF(i,:));
   switch I
       case 1
           Mdisubt(:,i)=Mdisubt(:,i)-MfunF1(MparF{i,s},xdata);
           CFStruct(2,i)=1;
       case 2
           Mdisubt(:,i)=Mdisubt(:,i)-MfunE(MparE{i,s},xdata);
           CFStruct(2,i)=2;
       case 3
           Mdisubt(:,i)=Mdisubt(:,i)-MfunS(MparS{i,s},xdata);
           CFStruct(2,i)=3;
       case 4
           Mdisubt(:,i)=Mdisubt(:,i)-MfunL(MparL{i,s},xdata);
           CFStruct(2,i)=4;
   end
end

s=3;
for i=1:MDIsize2
    x0=[std(Mdisubt(:,i)) std(Mdisubt(:,i)) 1 1 0 0 Mdisubt(1,i)];
    x1=[1 0 1 Mdisubt(1,i)];
    x2=[1 0 1 Mdisubt(1,i)];
    x3=[1 Mdisubt(1,i)];
    ms= MultiStart('UseParallel',true);
    options=optimoptions(@lsqcurvefit,'Algorithm',...
    'levenberg-marquardt','MaxFunEvals',200*7,'MaxIterations',800);
    problemf= createOptimProblem('lsqcurvefit','objective',@MfunF1,...
        'x0',x0,'xdata',xdata,'ydata',Mdisubt(:,i),'lb',lb,'ub',ub,'options',options);
    [MparF{i,s}, errf]=run(ms,problemf,100);
    
    ms= MultiStart('UseParallel',true);
    options=optimoptions(@lsqcurvefit,'Algorithm',...
    'levenberg-marquardt','MaxFunEvals',200*7);
    probleme= createOptimProblem('lsqcurvefit','objective',@MfunE,...
        'x0',x1,'xdata',xdata,'ydata',Mdisubt(:,i),'lb',lb,'ub',ub,'options',options);
    [MparE{i,s}, erre]=run(ms,probleme,100);
    
    ms= MultiStart('UseParallel',true);
    options=optimoptions(@lsqcurvefit,'Algorithm',...
    'levenberg-marquardt','MaxFunEvals',200*7);
    problems= createOptimProblem('lsqcurvefit','objective',@MfunS,...
        'x0',x2,'xdata',xdata,'ydata',Mdisubt(:,i),'lb',lb,'ub',ub,'options',options);
    [MparS{i,s}, errs]=run(ms,problems,100);
    
    [MparL{i,s}, errl]=lsqcurvefit(@MfunL,x3,xdata,Mdisubt(:,i));
    errCF(i,:)=[errf erre errs errl];
end

for i=1:MDIsize2
   [~,I]=min(errCF(i,:));
   switch I
       case 1
           CFStruct(3,i)=1;
       case 2
           CFStruct(3,i)=2;
       case 3
           CFStruct(3,i)=3;
       case 4
           CFStruct(3,i)=4;
   end
end

SMdistd=zeros(size(SMdiFull,1)-t,MDIsize2);
for i=1:size(SMdiFull,1)-t
    SMdistd(i,:)=(SMdiFull(i+t,:)-SMdiFull(i,:))./SMdiFull(i,:);
end
SMdistd(isinf(SMdistd))=0;
SMdiStd=sum(abs(SMdistd-mean(SMdistd)))/(size(SMdistd,1)-1);

CFDrift=zeros(t,3);
MDDriftts=zeros(t,MDIsize2); 
for i=1:MDIsize2
    for s=1:3
        T=CFStruct(s,i);
        switch T
            case 1
                CFDrift(:,s)=MfunF1(MparF{i,s},cftlb:cftlb+t-1);
            case 2
                CFDrift(:,s)=MfunE(MparE{i,s},cftlb:cftlb+t-1);
            case 3
                CFDrift(:,s)=MfunS(MparS{i,s},cftlb:cftlb+t-1);
            case 4
                CFDrift(:,s)=MfunL(MparL{i,s},cftlb:cftlb+t-1);
        end
    end
    PDrift=sum(CFDrift,2);
    if min(PDrift)<=0
        linbeta=polyfit((1:cftlb)',SMdi(:,i),1);
        PDrift=linbeta(1)*(cftlb:cftlb+t-1)'+linbeta(2);
        if min(PDrift)<=0
            PDrift=mean(SMdi(:,i))*ones(t,1);
        end
    elseif  abs((PDrift(end)-PDrift(1))/PDrift(1))>1.64*SMdiStd(i)
        linbeta=polyfit((1:cftlb)',SMdi(:,i),1);
        PDrift=linbeta(1)*(cftlb:cftlb+t-1)'+linbeta(2);
        if min(PDrift)<=0
            PDrift=mean(SMdi(:,i))*ones(t,1);
        end
    end
    MDDriftts(:,i)=PDrift;
    MDDriftst=Dat_trans_v2_2(MDDriftts);
    imgerr=0;
    for k=1:SMdiAsize2
        if isreal(MDDriftst{k}(:,i))==0
            imgerr=1;
        end
    end
    if imgerr==1
        PDrift=mean(SMdi(:,i))*ones(t,1);
    end
    MDDriftts(:,i)=PDrift;
end
MDDrifts=Dat_trans_v2_2(MDDriftts);

CFDrift=zeros(cftlb,3);
CFTc=zeros(cftlb,MDIsize2); 
for i=1:MDIsize2
    for s=1:3
        T=CFStruct(s,i);
        switch T
            case 1
                CFDrift(:,s)=MfunF1(MparF{i,s},1:cftlb);
            case 2
                CFDrift(:,s)=MfunE(MparE{i,s},1:cftlb);
            case 3
                CFDrift(:,s)=MfunS(MparS{i,s},1:cftlb);
            case 4
                CFDrift(:,s)=MfunL(MparL{i,s},1:cftlb);
        end
    end
    PDrift=sum(CFDrift,2);
    if min(PDrift)<=0
        linbeta=polyfit((1:cftlb)',SMdi(:,i),1);
        PDrift=linbeta(1)*(1:cftlb)'+linbeta(2);
        if min(PDrift)<=0
            PDrift=mean(SMdi(:,i))*ones(cftlb,1);
        end
    elseif abs((PDrift(end)-PDrift(1))/PDrift(1))>1.64*SMdiStd(i)
        linbeta=polyfit((1:cftlb)',SMdi(:,i),1);
        PDrift=linbeta(1)*(1:cftlb)'+linbeta(2);
        if min(PDrift)<=0
            PDrift=mean(SMdi(:,i))*ones(cftlb,1);
        end
    end
    CFTc(:,i)=PDrift;
    CFTst=Dat_trans_v2_2(CFTc);
    imgerr=0;
    for k=1:SMdiAsize2
        if isreal(CFTst{k}(:,i))==0
            imgerr=1;
        end
    end
    if imgerr==1
        PDrift=mean(SMdi(:,i))*ones(cftlb,1);
    end
    CFTc(:,i)=PDrift;
end
CFT=Dat_trans_v2_2(CFTc);

SigErr=cell(1,SMdiAsize2);
for i=1:SMdiAsize2
    SigErr{i}=(SMdiA{i}(end-cftlb+1:end,:)-CFT{i});
end
%% Monte Carlos
Mcts=cell(n,SMdiAsize2);
for i=1:n
    for k=1:SMdiAsize2
        MCts=[(MDDrifts{k}(1,:)); zeros((t-1),MDIsize2)]; 
        for s=2:t
            MCts(s,:)=MDDrifts{k}(s,:)+datasample(SigErr{k},1);   
        end
        Mcts{i,k}=MCts+(SMdiA{k}(end,:)-MCts(1,:));
    end
end

%% Statistical data of M.C.'s (MiA)

%% Regressions (MiA)

MciRC=cell(n,1);
for i=1:n
    E=zeros(t,Misize2);
    A=Mcts{i,1};
    for ii=1:Misize2
        C=A(:,ii);
        if L(ii)>0
            if L(ii)<=t
                C(end-L(ii)+1:end)=[];
                D=(SMdiA{1}(end-L(ii)+1:end,ii));
            else
                C=[];
                D=(SMdiA{1}(end-L(ii)+1:end-L(ii)+t,ii));
            end
        else
            D=[];
        end
        E(:,ii)=[D;C];
    end
    E(:,Ct==0)=[];
    MciRC{i}=E;
end

Dt=max(sum(Ct)+15,3*t);
E=zeros(Dt,Misize2);
for i=1:Misize2
    if L(i)>0
        C=SMdiA{1}(end-Dt-L(i)+1:end,i);
        C(end-L(i)+1:end)=[];
    else
        C=SMdiA{1}(end-Dt+1:end,i);
    end
    E(:,i)=C;
end
E(:,Ct==0)=[];
MiRC=[ones(Dt,1) E];

Mdr=Md(end-Dt+1:end);
Beta=mvregress(MiRC,Mdr);

MdR=zeros(t,n);
Merr=0;
for i=1:n
    Ai=[ones(t,1) MciRC{i}];
    Mdr1=(Ai*Beta);
    Mdr1=Mdr1+(Md(end)-Mdr1(1));
    if isempty(Mdr1(Mdr1<=0))==0 || ...
            (max(Mdr1)-Mdr1(1))/Mdr1(1) > 4*std( ...
            (Md(t:end)-Md(1:end-t+1))./Md(1:end-t+1))
        disp("Regress with vals less than 0 or erroneous: "),disp("Md")
        Merr=1;
    end
    MdR(:,i)=exp(Mdr1);
end
if Merr==1
    for i=1:n
        MdR(:,i)=Mcts{i,1}(:,end);
    end
end
%% CCIPred & Statistical data of Regressions (MiA)

CCIPred=mean(MdR,2);

MdRet=zeros(n,1);
for i=1:n
    M=MdR(:,i);
    MdRet(i)=(M(8)-M(1))/M(1); 
end
MdRvar=var(MdRet);
MdRExp=mean(MdRet);

MEMpredi=exp(Md(end))*(1+MdRExp);


%% P.P.M (Portfolio Prediction Module):
TiP=[ones(Pdsize2,Misize2-Pdsize2) (ones(Pdsize2)-eye(Pdsize2)) ones(Pdsize2,1)];
PPMpredi=zeros(1,Pdsize2);
PdR=cell(n,Pdsize2);
CtPA=cell(1,SMdiAsize2-1);
NoReg=zeros(1,Pdsize2);
PDExp=zeros(1,Pdsize2);
PDvar=zeros(1,Pdsize2);
PDVaR=zeros(1,Pdsize2);
pcort=[5 7 7 6 6 5 7];
cpb=[0.35 0.2 0.4 0.3 0.15 0.4 0.4];
rtb=[3 4 4 4 4 5 4];

for z=2:SMdiAsize2
    x=z-1;
    %% Correlations & Lags (Pit)
    CP=zeros(1,MDIsize2);
    LP=zeros(1,MDIsize2);
    for s=1:MDIsize2
        [r,lags]=crosscorr(tick2ret(Pd(end-pcort(x)*t+1:end,x)+1), ...
            tick2ret(TiP(x,s)*SMdiA{z}(end-pcort(x)*t+1:end,s)+1),2*t); 
        [~,I]=max(abs(r));
        l=lags(I);
        CP(s)=r(I);
        LP(s)=-l;
    end

    CtP=(LP>=0 & abs(CP)>cpb(x));
    CtP=CtP.*TiP(x,:);
    CtPA{x}=CtP;
    NoReg(x)=sum(CtP);
    %% Regressions (Pit)

    PciRC=cell(n);
    for i=1:n
        A=Mcts{i,z};
        E=zeros(t,MDIsize2);
        for r=1:MDIsize2
            C=A(:,r);
            if LP(r)>0
                if LP(r)<=t
                    C(end-LP(r)+1:end)=[];
                    D=SMdiA{z}(end-LP(r)+1:end,r);
                else
                    C=[];
                    D=SMdiA{z}(end-LP(r)+1:end-LP(r)+t,r);
                end
            else
                D=[];
            end
            E(:,r)=[D;C];
        end
        E(:,CtP==0)=[];
        PciRC{i}=E;
    end
    
    Dt=max(sum(CtP)+15,rtb(x)*t);
    E=zeros(Dt,MDIsize2);
    for s=1:MDIsize2
        if LP(s)>0
            C=SMdiA{z}(end-Dt-LP(s)+1:end,s);
            C(end-LP(s)+1:end)=[];
            E(:,s)=C;
        else
            C=SMdiA{z}(end-Dt+1:end,s);
            E(:,s)=C;
        end
    end
    E(:,CtP==0)=[];
    PiRC=[ones(Dt,1) E];

    Pdd=Pd(end-Dt+1:end,x);
    Beta=mvregress(PiRC,Pdd);
    
    PRerr=0;
    for i=1:n
        Pdr1=[ones(t,1) PciRC{i}]*Beta;
        Pdr1=Pdr1+(Pd(end,x)-Pdr1(1));
        if isempty(Pdr1(Pdr1<=0))==0 || ...
                (max(Pdr1)-Pdr1(1))/Pdr1(1) > 4*std( ...
                (Pd(t:end,x) - Pd(1:end-t+1,x))./Pd(1:end-t+1,x))
            disp("Regress with vals less than 0 or erroneous: "),disp(x)
            PRerr=1;
        end
        switch x
            case 1 
                PdR{i,x}=exp(Pdr1);
            case 2
                PdR{i,x}=exp(Pdr1);
            case 3
                PdR{i,x}=exp(Pdr1-15);
            case 4
                PdR{i,x}=exp(Pdr1-3);
            case 5
                PdR{i,x}=exp(Pdr1-15);
            case 6
                PdR{i,x}=exp(Pdr1-7);
            case 7
                PdR{i,x}=exp(Pdr1-7);
        end
    end
    if PRerr==1
        for i=1:n
            PdR{i,x}=Mcts{i,z}(:,Misize2-Pdsize2+x);
        end
    end
    %% Statistical data of Regress. (Pit)
    
    T=zeros(n,1);
    for i=1:n
        K=PdR{i,x};
        T(i)=(K(8)-K(1))/K(1);
    end
    PdRet=T;

    PDvar(x)=var(PdRet);
    PDExp(x)=mean(PdRet);
    PDVaR(x)=PDExp(x)-1.64*sqrt(PDvar(x));
    
    switch x
        case 1
            pde=exp(Pd(end,x));
        case 2
            pde=exp(Pd(end,x));
        case 3
            pde=exp(Pd(end,x)-15);
        case 4
            pde=exp(Pd(end,x)-3);
        case 5
            pde=exp(Pd(end,x)-15);
        case 6
            pde=exp(Pd(end,x)-7);
        case 7
            pde=exp(Pd(end,x)-7);
    end
            
    PPMpredi(x)=(1+PDExp(x)).*pde;
end

%% CCPred
Pdr1=zeros(t,n);
for i=1:n
    Pdr1(:,i)=PdR{i,1};
end
PdR1m=mean(Pdr1,2);

Pdr2=zeros(t,n);
for i=1:n
    Pdr2(:,i)=PdR{i,2};
end
PdR2m=mean(Pdr2,2);

Pdr3=zeros(t,n);
for i=1:n
    Pdr3(:,i)=PdR{i,3};
end
PdR3m=mean(Pdr3,2);

Pdr4=zeros(t,n);
for i=1:n
    Pdr4(:,i)=PdR{i,4};
end
PdR4m=mean(Pdr4,2);

Pdr5=zeros(t,n);
for i=1:n
    Pdr5(:,i)=PdR{i,5};
end
PdR5m=mean(Pdr5,2);

Pdr6=zeros(t,n);
for i=1:n
    Pdr6(:,i)=PdR{i,6};
end
PdR6m=mean(Pdr6,2);

Pdr7=zeros(t,n);
for i=1:n
    Pdr7(:,i)=PdR{i,7};
end
PdR7m=mean(Pdr7,2);


CCPred=[PdR1m PdR2m PdR3m PdR4m PdR5m PdR6m PdR7m];

%% Predictions

%% CCI
CCIm = smooth((lMd(4:end)-lMd(1:end-3))/4,10);
CCImp = (CCIm(end)-CCIm(end-7+1))/CCIm(end-7+1);
ccipp = (lMd(end)-lMd(end-7+1))/lMd(end-7+1);
CCIprp = (CCIPred(8)-CCIPred(1))/CCIPred(1);
ccitx = smoothdata(sum(Mi(:,[1 10 19 22 26 31 36 40 44 52 59])./ ...
    mean(Mi(:,[1 10 19 22 26 31 36 40 44 52 59]),1),2),'gaussian',6);
cciad = smoothdata(sum(Mi(:,[6 15 28 32 37 41 42 45 53 60])./ ...
    mean(Mi(:,[6 15 28 32 37 41 42 45 53 60]),1),2),'gaussian',6);
cciap = (ccitx(end)-ccitx(end-7+1))/ccitx(end-7+1) + (cciad(end)-cciad(end-7+1))/cciad(end-7+1);
ccii = smoothdata(sum(Mi(:,66:80),2)/15,'gaussian',6);
cciip = (ccii(end)-ccii(end-7+1))/ccii(end-7+1);

if sign(cciip)<0 && sign(ccipp)<0
    ccigts=-1;
else
    ccigts=sign(cciip)*sign(ccipp);
end
        
ccist=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    ccist(i) = std(lMd(i-4+1:i));
end
ccistd = smoothdata(ccist,'gaussian',7);
ccistdp = (ccistd(end)-ccistd(end-7+1))/ccistd(end-7+1);
%% BTC
btctx = smoothdata(Mi(:,1),'gaussian',6);
btcad = smoothdata(Mi(:,6),'gaussian',6);
btcap = (btctx(end)-btctx(end-7+1))/btctx(end-7+1) + (btcad(end)-btcad(end-7+1))/btcad(end-7+1);
btci = smoothdata((Mi(:,66)+Mi(:,67))/2,'gaussian',6);
btcip = (btci(end)-btci(end-7+1))/btci(end-7+1);
btcp = lPd(:,1);
btcpp = (btcp(end)-btcp(end-7+1))/btcp(end-7+1);
btcvl=smoothdata(lPdv(:,1),'gaussian',10);
btcvlp = (btcvl(end)-btcvl(end-7+1))/btcvl(end-7+1);
btcst=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    btcst(i) = std(lPd(i-4+1:i,1));
end
btcstd = smoothdata(btcst,'gaussian',7);
btcstdp = (btcstd(end)-btcstd(end-7+1))/btcstd(end-7+1);
btcm = smoothdata((lPd(4:end,1)-lPd(1:end-3,1))/4,'gaussian',10);
btcmp = (btcm(end)-btcm(end-7+1))/btcm(end-7+1);
btcpr = smoothdata(CCPred(:,1),'gaussian',10);
btcprp = (btcpr(8)-btcpr(1))/btcpr(1);

if sign(btcip)<0 && sign(btcpp)<0
    gts=-1;
else
    gts=sign(btcip)*sign(btcpp);
end

if sign(btcvlp)<0 && sign(btcpp)<0
    vol=-1;
else
    vol=sign(btcvlp)*sign(btcpp);
end 

btcbs = Par(1,1)*sign(btcap) + Par(1,2)*gts + Par(1,3)*sign(btcpp) + ...
    Par(1,4)*sign(btcstdp)*sign(btcpp) + Par(1,5)*sign(btcmp) + ...
    Par(1,6)*sign(CCImp) + Par(1,7)*vol + Par(1,8)*sign(btcprp) + Par(1,9)*sign(CCIprp) + ...
    Par(1,10)*sign(cciap) + Par(1,11)*ccigts + Par(1,12)*sign(ccistdp)*sign(ccipp);

%% ETH
ethtx = smoothdata(Mi(:,10),'gaussian',6);
ethad = smoothdata(Mi(:,15),'gaussian',6);
ethap = (ethtx(end)-ethtx(end-7+1))/ethtx(end-7+1) + (ethad(end)-ethad(end-7+1))/ethad(end-7+1);
ethi = smoothdata((Mi(:,68)+Mi(:,69))/2,'gaussian',6);
ethip = (ethi(end)-ethi(end-7+1))/ethi(end-7+1);
ethp=lPd(:,2);
ethpp = (ethp(end)-ethp(end-7+1))/ethp(end-7+1);
ethvl=smoothdata(lPdv(:,2),'gaussian',10);
ethvlp = (ethvl(end)-ethvl(end-7+1))/ethvl(end-7+1);
ethst=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    ethst(i) = std(lPd(i-4+1:i,2));
end
ethstd = smoothdata(ethst,'gaussian',7);
ethstdp = (ethstd(end)-ethstd(end-7+1))/ethstd(end-7+1);
ethm = smoothdata((lPd(4:end,2)-lPd(1:end-3,2))/4,'gaussian',10);
ethmp = (ethm(end)-ethm(end-7+1))/ethm(end-7+1);
ethpr=smoothdata(CCPred(:,2),'gaussian',10);
ethprp = (ethpr(8)-ethpr(1))/ethpr(1);

if sign(ethip)<0 && sign(ethpp)<0
    gts=-1;
else
    gts=sign(ethip)*sign(ethpp);
end

if sign(ethvlp)<0 && sign(ethpp)<0
    vol=-1;
else
    vol=sign(ethvlp)*sign(ethpp);
end

ethbs = Par(2,1)*sign(ethap) + Par(2,2)*gts + Par(2,3)*sign(ethpp) + ...
    Par(2,4)*sign(ethstdp)*sign(ethpp) + Par(2,5)*sign(ethmp) + ...
    Par(2,6)*sign(CCImp) + Par(2,7)*vol + Par(2,8)*sign(ethprp) + Par(2,9)*sign(CCIprp) + ...
    Par(2,10)*sign(cciap) + Par(2,11)*ccigts + Par(2,12)*sign(ccistdp)*sign(ccipp);

%% XLM
xlmtx = smoothdata(Mi(:,19),'gaussian',6);
xlmap = (xlmtx(end)-xlmtx(end-7+1))/xlmtx(end-7+1);
xlmi = smoothdata(Mi(:,72),'gaussian',6);
xlmip = (xlmi(end)-xlmi(end-7+1))/xlmi(end-7+1);
xlmp=lPd(:,3);
xlmpp = (xlmp(end)-xlmp(end-7+1))/xlmp(end-7+1);
xlmvl=smoothdata(lPdv(:,3),'gaussian',10);
xlmvlp = (xlmvl(end)-xlmvl(end-7+1))/xlmvl(end-7+1);
xlmst=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    xlmst(i) = std(lPd(i-4+1:i,2));
end
xlmstd = smoothdata(xlmst,'gaussian',7);
xlmstdp = (xlmstd(end)-xlmstd(end-7+1))/xlmstd(end-7+1);
xlmm = smoothdata((lPd(4:end,3)-lPd(1:end-3,3))/4,'gaussian',10);
xlmmp = (xlmm(end)-xlmm(end-7+1))/xlmm(end-7+1);
xlmpr=smoothdata(CCPred(:,3),'gaussian',10);
xlmprp = (xlmpr(8)-xlmpr(1))/xlmpr(1);

if sign(xlmip)<0 && sign(xlmpp)<0
    gts=-1;
else
    gts=sign(xlmip)*sign(xlmpp);
end

if sign(xlmvlp)<0 && sign(xlmpp)<0
    vol=-1;
else
    vol=sign(xlmvlp)*sign(xlmpp);
end

xlmbs = Par(3,1)*sign(xlmap) + Par(3,2)*gts + Par(3,3)*sign(xlmpp) + ...
    Par(3,4)*sign(xlmstdp)*sign(xlmpp) + Par(3,5)*sign(xlmmp) + ...
    Par(3,6)*sign(CCImp) + Par(3,7)*vol + Par(3,8)*sign(xlmprp) + Par(3,9)*sign(CCIprp) + ...
    Par(3,10)*sign(cciap) + Par(3,11)*ccigts + Par(3,12)*sign(ccistdp)*sign(ccipp);

%% XMR
xmrtx = smoothdata(Mi(:,22),'gaussian',6);
xmrap = (xmrtx(end)-xmrtx(end-7+1))/xmrtx(end-7+1);
xmri = smoothdata(Mi(:,70),'gaussian',6);
xmrip = (xmri(end)-xmri(end-7+1))/xmri(end-7+1);
xmrp=lPd(:,4);
xmrpp = (xmrp(end)-xmrp(end-7+1))/xmrp(end-7+1);
xmrvl=smoothdata(lPdv(:,4),'gaussian',10);
xmrvlp = (xmrvl(end)-xmrvl(end-7+1))/xmrvl(end-7+1);
xmrst=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    xmrst(i) = std(lPd(i-4+1:i,4));
end
xmrstd = smoothdata(xmrst,'gaussian',7);
xmrstdp = (xmrstd(end)-xmrstd(end-7+1))/xmrstd(end-7+1);
xmrm = smoothdata((lPd(4:end,4)-lPd(1:end-3,4))/4,'gaussian',10);
xmrmp = (xmrm(end)-xmrm(end-7+1))/xmrm(end-7+1);
xmrpr=smoothdata(CCPred(:,3),'gaussian',10);
xmrprp = (xmrpr(8)-xmrpr(1))/xmrpr(1);

if sign(xmrip)<0 && sign(xmrpp)<0
    gts=-1;
else
    gts=sign(xmrip)*sign(xmrpp);
end

if sign(xmrvlp)<0 && sign(xmrpp)<0
    vol=-1;
else
    vol=sign(xmrvlp)*sign(xmrpp);
end

xmrbs = Par(4,1)*sign(xmrap) + Par(4,2)*gts + Par(4,3)*sign(xmrpp) + ...
    Par(4,4)*sign(xmrstdp)*sign(xmrpp) + Par(4,5)*sign(xmrmp) + ...
    Par(4,6)*sign(CCImp) + Par(4,7)*vol + Par(4,8)*sign(xmrprp) + Par(4,9)*sign(CCIprp) + ...
    Par(4,10)*sign(cciap) + Par(4,11)*ccigts + Par(4,12)*sign(ccistdp)*sign(ccipp);

%% XRP
xrptx = smoothdata(Mi(:,26),'gaussian',6);
xrpad = smoothdata(Mi(:,28),'gaussian',6);
xrpap = (xrptx(end)-xrptx(end-7+1))/xrptx(end-7+1) + (xrpad(end)-xrpad(end-7+1))/xrpad(end-7+1);
xrpi = smoothdata((Mi(:,71)+Mi(:,75))/2,'gaussian',6);
xrpip = (xrpi(end)-xrpi(end-7+1))/xrpi(end-7+1);
xrpp=lPd(:,5);
xrppp = (xrpp(end)-xrpp(end-7+1))/xrpp(end-7+1);
xrpvl=smoothdata(lPdv(:,5),'gaussian',10);
xrpvlp = (xrpvl(end)-xrpvl(end-7+1))/xrpvl(end-7+1);
xrpst=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    xrpst(i) = std(lPd(i-4+1:i,5));
end
xrpstd = smoothdata(xrpst,'gaussian',7);
xrpstdp = (xrpstd(end)-xrpstd(end-7+1))/xrpstd(end-7+1);
xrpm = smoothdata((lPd(4:end,5)-lPd(1:end-3,5))/4,'gaussian',10);
xrpmp = (xrpm(end)-xrpm(end-7+1))/xrpm(end-7+1);
xrppr=smoothdata(CCPred(:,5),'gaussian',10);
xrpprp = (xrppr(8)-xrppr(1))/xrppr(1);

if sign(xrpip)<0 && sign(xrppp)<0
    gts=-1;
else
    gts=sign(xrpip)*sign(xrppp);
end

if sign(xrpvlp)<0 && sign(xrppp)<0
    vol=-1;
else
    vol=sign(xrpvlp)*sign(xrppp);
end

xrpbs = Par(5,1)*sign(xrpap) + Par(5,2)*gts + Par(5,3)*sign(xrppp) + ...
    Par(5,4)*sign(xrpstdp)*sign(xrppp) + Par(5,5)*sign(xrpmp) + ...
    Par(5,6)*sign(CCImp) + Par(5,7)*vol + Par(5,8)*sign(xrpprp) + Par(5,9)*sign(CCIprp) + ...
    Par(5,10)*sign(cciap) + Par(5,11)*ccigts + Par(5,12)*sign(ccistdp)*sign(ccipp);

%% LINK
linktx = smoothdata(Mi(:,31),'gaussian',6);
linkad = smoothdata(Mi(:,32),'gaussian',6);
linkap = (linktx(end)-linktx(end-7+1))/linktx(end-7+1) + (linkad(end)-linkad(end-7+1))/linkad(end-7+1);
linki = smoothdata(Mi(:,73),'gaussian',6);
linkip = (linki(end)-linki(end-7+1))/linki(end-7+1);
linkp=lPd(:,6);
linkpp = (linkp(end)-linkp(end-7+1))/linkp(end-7+1);
linkvl=smoothdata(lPdv(:,6),'gaussian',10);
linkvlp = (linkvl(end)-linkvl(end-7+1))/linkvl(end-7+1);
linkst=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    linkst(i) = std(lPd(i-4+1:i,6));
end
linkstd = smoothdata(linkst,'gaussian',7);
linkstdp = (linkstd(end)-linkstd(end-7+1))/linkstd(end-7+1);
linkm = smoothdata((lPd(4:end,6)-lPd(1:end-3,6))/4,'gaussian',10);
linkmp = (linkm(end)-linkm(end-7+1))/linkm(end-7+1);
linkpr=smoothdata(CCPred(:,6),'gaussian',10);
linkprp = (linkpr(8)-linkpr(1))/linkpr(1);

if sign(linkip)<0 && sign(linkpp)<0
    gts=-1;
else
    gts=sign(linkip)*sign(linkpp);
end

if sign(linkvlp)<0 && sign(linkpp)<0
    vol=-1;
else
    vol=sign(linkvlp)*sign(linkpp);
end

linkbs = Par(6,1)*sign(linkap) + Par(6,2)*gts + Par(6,3)*sign(linkpp) + ...
    Par(6,4)*sign(linkstdp)*sign(linkpp) + Par(6,5)*sign(linkmp) + ...
    Par(6,6)*sign(CCImp) + Par(6,7)*vol + Par(6,8)*sign(linkprp) + Par(6,9)*sign(CCIprp) + ...
    Par(6,10)*sign(cciap) + Par(6,11)*ccigts + Par(6,12)*sign(ccistdp)*sign(ccipp); 

%% NEO
neotx = smoothdata(Mi(:,36),'gaussian',6);
neoad = smoothdata(Mi(:,37),'gaussian',6);
neoap = (neotx(end)-neotx(end-7+1))/neotx(end-7+1) + (neoad(end)-neoad(end-7+1))/neoad(end-7+1);
neoi = smoothdata(Mi(:,74),'gaussian',6);
neoip = (neoi(end)-neoi(end-7+1))/neoi(end-7+1);
neop=lPd(:,7);
neopp = (neop(end)-neop(end-7+1))/neop(end-7+1);
neovl=smoothdata(lPdv(:,7),'gaussian',10);
neovlp = (neovl(end)-neovl(end-7+1))/neovl(end-7+1);
neost=zeros(Pdsize1-4,1);
for i=4:Pdsize1
    neost(i) = std(lPd(i-4+1:i,7));
end
neostd = smoothdata(neost,'gaussian',7);
neostdp = (neostd(end)-neostd(end-7+1))/neostd(end-7+1);
neom = smoothdata((lPd(4:end,7)-lPd(1:end-3,7))/4,'gaussian',10);
neomp = (neom(end)-neom(end-7+1))/neom(end-7+1);
neopr=smoothdata(CCPred(:,7),'gaussian',10);
neoprp = (neopr(8)-neopr(1))/neopr(1);

if sign(neoip)<0 && sign(neopp)<0
    gts=-1;
else
    gts=sign(neoip)*sign(neopp);
end

if sign(neovlp)<0 && sign(neopp)<0
    vol=-1;
else
    vol=sign(neovlp)*sign(neopp);
end

neobs = Par(7,1)*sign(neoap) + Par(7,2)*gts + Par(7,3)*sign(neopp) + ...
    Par(7,4)*sign(neostdp)*sign(neopp) + Par(7,5)*sign(neomp) + ...
    Par(7,6)*sign(CCImp) + Par(7,7)*vol + Par(7,8)*sign(neoprp) + Par(7,9)*sign(CCIprp) + ...
    Par(7,10)*sign(cciap) + Par(7,11)*ccigts + Par(7,12)*sign(ccistdp)*sign(ccipp); 

%%
Predicts=[btcbs ethbs xlmbs xmrbs xrpbs linkbs neobs];
    
%% Curvefit time series
CFTA=zeros(cftlb+t,MDIsize2);
CFDrift=zeros(cftlb+t,3);
for i=1:MDIsize2
    for s=1:3
        T=CFStruct(s,i);
        switch T
            case 1
                CFDrift(:,s)=MfunF1(MparF{i,s},1:cftlb+t);
            case 2
                CFDrift(:,s)=MfunE(MparE{i,s},1:cftlb+t);
            case 3
                CFDrift(:,s)=MfunS(MparS{i,s},1:cftlb+t);
            case 4
                CFDrift(:,s)=MfunL(MparL{i,s},1:cftlb+t);
        end
    end
    PDrift=sum(CFDrift,2);
    if min(PDrift)<=0
        linbeta=polyfit((1:cftlb)',SMdi(:,i),1);
        PDrift=linbeta(1)*(1:cftlb+t)'+linbeta(2);
        if min(PDrift)<=0
            PDrift=mean(SMdi(:,i))*ones(cftlb+t,1);
        end
    elseif  abs((PDrift(end)-PDrift(1))/PDrift(1))>1.64*SMdiStd(i)
        linbeta=polyfit((1:cftlb)',SMdi(:,i),1);
        PDrift=linbeta(1)*(1:cftlb+t)'+linbeta(2);
        if min(PDrift)<=0
            PDrift=mean(SMdi(:,i))*ones(cftlb+t,1);
        end
    end
    CFTA(:,i)=PDrift;
    MDDriftst=Dat_trans_v2_2(CFTA);
    imgerr=0;
    for k=1:SMdiAsize2
        if isreal(MDDriftst{k}(:,i))==0
            imgerr=1;
        end
    end
    if imgerr==1
        PDrift=mean(SMdi(:,i))*ones(cftlb+t,1);
    end
    CFTA(:,i)=PDrift;
end
end