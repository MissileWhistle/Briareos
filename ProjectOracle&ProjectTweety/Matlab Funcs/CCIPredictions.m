function  CCpred=CCIPredictions(MDIFull,Mi,Md)

%% M.E.M(Macro Econ. Prediction Module):
Misize2=size(Mi,2);
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

Md=log(Md);

n=3000;
t=35;

%% Correlations & Lags (MiA)

C=zeros(1,Misize2);
L=zeros(1,Misize2);
for i=1:Misize2
  [r,lags]=crosscorr(tick2ret(Md+1),tick2ret(SMdiA(end-7*t+1:end,i)+1),2*t);
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
    if isreal(MDDriftst(:,i))==0
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
    if isreal(CFTst(:,i))==0
        PDrift=mean(SMdi(:,i))*ones(cftlb,1);
    end
    CFTc(:,i)=PDrift;
end
CFT=Dat_trans_v2_2(CFTc);
SigErr=(SMdiA(end-cftlb+1:end,:)-CFT);

%% Monte Carlos
Mcts=cell(n,1);
for i=1:n
    MCts=[(MDDrifts(1,:)); zeros((t-1),MDIsize2)]; 
    for s=2:t
        MCts(s,:)=MDDrifts(s,:)+datasample(SigErr,1);   
    end
    Mcts{i}=MCts+(SMdiA(end,:)-MCts(1,:));
end
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
                D=(SMdiA(end-L(ii)+1:end,ii));
            else
                C=[];
                D=(SMdiA(end-L(ii)+1:end-L(ii)+t,ii));
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
        C=SMdiA(end-Dt-L(i)+1:end,i);
        C(end-L(i)+1:end)=[];
    else
        C=SMdiA(end-Dt+1:end,i);
    end
    E(:,i)=C;
end
E(:,Ct==0)=[];
MiRC=[ones(Dt,1) E];

Mdr=Md(end-Dt+1:end);
Beta=mvregress(MiRC,Mdr);

MdR=zeros(35,n);
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
%% Mean of Regressions (MiA)
CCpred=mean(MdR,2);

end