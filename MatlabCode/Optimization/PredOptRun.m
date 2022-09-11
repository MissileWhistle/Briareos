%% PredOpt
function PPar=PredOptRun(MiFull,MdFull,lPdcFull,lPdvolFull)
Pdsize2=size(lPdcFull,2);
t=35;
%% CC(I)Pred
CCIPredA=cell(182,1);
CCPredA=cell(182,1);
for daycount=700:7:size(lPdcFull,1)-7
%% -> Predictions
%% Data
MDIFull=[MiFull(daycount-700+1:daycount,:) ...
    MdFull(daycount-700+1:daycount,:)];
Mi=MiFull(daycount-7*t+1:daycount,:);
Md=MdFull(daycount-7*t+1:daycount,:);
Pd=lPdcFull(daycount-7*t+1:daycount,:);
%% Predictions
[CCIPred, CCPred] = PredOptFun(MDIFull,Mi,Md,Pd);
CCIPredA{daycount-700+1}=CCIPred;
CCPredA{daycount-700+1}=CCPred;
end

%% Opt
PPar=zeros(Pdsize2,13);
for zet=1:Pdsize2
    OptFun=@(P) PredOpt(P,MiFull,MdFull,lPdcFull,lPdvolFull,CCIPredA,CCPredA,zet);

    ms= MultiStart('UseParallel',true);
    x0=ones(12,1);
    A=[];
    b=[];
    Aeq=ones(1,12);
    beq=1;
    lb=zeros(12,1);
    up=ones(12,1);

    problem= createOptimProblem('fmincon','objective',OptFun,...
            'x0',x0,'Aineq',A,'bineq',b,'Aeq',Aeq,'beq',beq,'lb',lb,'ub',up);
    [PA,fval]=run(ms,problem,400);
    PPar(zet,:)=[-fval PA'];
end

end
