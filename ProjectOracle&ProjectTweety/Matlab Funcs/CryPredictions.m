function CCPred=CryPredictions(MDIFull,Mi,Pd)

%% M.E.M(Macro Econ. Prediction Module):
Misize2=size(Mi,2);
Pdsize2=size(Pd,2);
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

SMdiA=Dat_trans_v2C(MDIFull);
SMdiAsize2=size(SMdiA,2);

Pd(:,1)=log(Pd(:,1));
Pd(:,2)=log(Pd(:,2));
Pd(:,3)=log(Pd(:,3))+3;
Pd(:,4)=log(Pd(:,4))+15;

t=35;
n=3000;
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
    MDDriftst=Dat_trans_v2_2C(MDDriftts);
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
MDDrifts=Dat_trans_v2_2C(MDDriftts);

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
    CFTst=Dat_trans_v2_2C(CFTc);
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
CFT=Dat_trans_v2_2C(CFTc);

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

%% P.P.M (Portfolio Prediction Module):
TiP=[ones(Pdsize2,Misize2-Pdsize2) (ones(Pdsize2)-eye(Pdsize2)) ones(Pdsize2,1)];
PdR=cell(n,Pdsize2);
pcort=[5 7 6 6];
cpb=[0.35 0.2 0.3 0.15];
rtb=[3 4 4 4];

for z=1:SMdiAsize2
    %% Correlations & Lags (Pit)
    CP=zeros(1,MDIsize2);
    LP=zeros(1,MDIsize2);
    for s=1:MDIsize2
        [r,lags]=crosscorr(tick2ret(Pd(end-pcort(z)*t+1:end,z)+1), ...
            tick2ret(TiP(z,s)*SMdiA{z}(end-pcort(z)*t+1:end,s)+1),2*t); 
        [~,I]=max(abs(r));
        l=lags(I);
        CP(s)=r(I);
        LP(s)=-l;
    end

    CtP=(LP>=0 & abs(CP)>cpb(z));
    CtP=CtP.*TiP(z,:);
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
    
    Dt=max(sum(CtP)+15,rtb(z)*t);
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

    Pdd=Pd(end-Dt+1:end,z);
    Beta=mvregress(PiRC,Pdd);
    
    PRerr=0;
    for i=1:n
        Pdr1=[ones(t,1) PciRC{i}]*Beta;
        Pdr1=Pdr1+(Pd(end,z)-Pdr1(1));
        if isempty(Pdr1(Pdr1<=0))==0 || ...
                (max(Pdr1)-Pdr1(1))/Pdr1(1) > 4*std( ...
                (Pd(t:end,z) - Pd(1:end-t+1,z))./Pd(1:end-t+1,z))
            disp("Regress with vals less than 0 or erroneous: "),disp(z)
            PRerr=1;
        end
        switch z
            case 1 
                PdR{i,z}=exp(Pdr1);
            case 2
                PdR{i,z}=exp(Pdr1);
            case 3
                PdR{i,z}=exp(Pdr1-3);
            case 4
                PdR{i,z}=exp(Pdr1-15);
        end
    end
    if PRerr==1
        for i=1:n
            PdR{i,z}=Mcts{i,z}(:,Misize2-Pdsize2+z);
        end
    end
end

PdRa=PdR(:,1);
Pdr1=zeros(t,n);
for i=1:n
    Pdr1(:,i)=PdRa{i};
end
PdR1=mean(Pdr1,2);

PdRb=PdR(:,2);
Pdr2=zeros(t,n);
for i=1:n
    Pdr2(:,i)=PdRb{i};
end
PdR2=mean(Pdr2,2);

PdRc=PdR(:,3);
Pdr3=zeros(t,n);
for i=1:n
    Pdr3(:,i)=PdRc{i};
end
PdR3=mean(Pdr3,2);

PdRd=PdR(:,4);
Pdr4=zeros(t,n);
for i=1:n
    Pdr4(:,i)=PdRd{i};
end
PdR4=mean(Pdr4,2);

CCPred=[PdR1 PdR2 PdR3 PdR4];



end