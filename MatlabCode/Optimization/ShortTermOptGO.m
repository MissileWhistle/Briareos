function SStrt = ShortTermOptGO(sPdcFull,sPdhFull,sPdlFull,sPdvolFull,SvarMACD,SvarOBV,SvarADL,SvarATR,SvarOSC,SvarCCI)
sPdsize2=size(sPdcFull,2);

SStrt=zeros(sPdsize2,23);
for i=1:sPdsize2
    %% Indicators
    
    %MACDs variables 
    t1=SvarMACD(i,1);
    t2=SvarMACD(i,2);
    t3=SvarMACD(i,3);
    ot1=SvarOBV(i,1);
    ot2=SvarOBV(i,2);
    ot3=SvarOBV(i,3);
    adt1=SvarADL(i,1);
    adt2=SvarADL(i,2);
    adt3=SvarADL(i,3);
    att1=SvarATR(i,1);
    att2=SvarATR(i,2);
    att3=SvarATR(i,3);
    act1=SvarCCI(i,1);
    act2=SvarCCI(i,2);
    
    %OBV
    OBV=onbalvol([sPdcFull(:,i),sPdvolFull(:,i)]);

    %ADLine
    ADLine=willad([sPdhFull(:,i),sPdlFull(:,i),sPdcFull(:,i)]);
    
    %ATR (Sig.)
    SATRbuy=ATR(sPdhFull(:,i),sPdlFull(:,i),sPdcFull(:,i),att1,att2,att3);
    
    %CCI
    CCILine=CCIf(sPdhFull(:,i),sPdlFull(:,i),sPdcFull(:,i),act1,act2);
    
    %MACD
    MACDline=movavg(sPdcFull(:,i),'exponential',t1)-movavg(sPdcFull(:,i),'exponential',t2);
    MACDline(isnan(MACDline))=0;
    Signaline=movavg(MACDline,'exponential',t3);
    Signaline(isnan(Signaline))=0;
    MACDdiff=MACDline-Signaline;

    %OVB MACD
    OBVMACDline=movavg(OBV,'exponential',ot1)-movavg(OBV,'exponential',ot2);
    OBVMACDline(isnan(OBVMACDline))=0;
    OBVSignaline=movavg(OBVMACDline,'exponential',ot3);
    OBVSignaline(isnan(OBVSignaline))=0;
    OBVMACDdiff=OBVMACDline-OBVSignaline;

    %ADLine MACD
    ADMACDline=movavg(ADLine,'exponential',adt1)-movavg(ADLine,'exponential',adt2);
    ADMACDline(isnan(ADMACDline))=0;
    ADSignaline=movavg(ADMACDline,'exponential',adt3);
    ADSignaline(isnan(ADSignaline))=0;
    ADMACDdiff=ADMACDline-ADSignaline;
   

    %Stoch Oscilator variables
    a=SvarOSC(i,1);
    d=SvarOSC(i,2);

    %Stoch OSC
    StochOSC=StOSC(sPdcFull(:,i),a,d);

    %Strategies&Signals
    
    %MACD Signal
    SMACDbuy=MACDdiff>0;
    
    %OBV signal
    SOBVbuy=OBVMACDdiff>0;

    %ADline Signal
    SADbuy=ADMACDdiff>0;

    %StochOSC Signal
    PSOSC=StochOSC>0;
    
    %CCI Signal
    PSCCI=CCILine>0;
     
    %% Strategy 
    S=[SMACDbuy(500:end) SOBVbuy(500:end) SADbuy(500:end) SATRbuy(500:end) PSOSC(500:end) PSCCI(500:end)];

    sPdFul=sPdcFull(500:end,i);
    scaling=1;
    I=size(S,2);
    popSize=2^(I*2);
    pop = initializePopulation(I,popSize);

    obj = @(pop) fitness(pop,S,sPdFul,scaling);

    options = gaoptimset('Display','iter','PopulationType','bitstring',...
        'PopulationSize',size(pop,1),...
        'InitialPopulation',pop,...
        'CrossoverFcn', @crossover,...
        'MutationFcn', @mutation,...
        'Vectorized','on'); %#ok<GAOPT>

     [best,minsh] = ga(obj,size(pop,2),[],[],[],[],[],[],[],options);
     minShp=-minsh;
     SStrt(i,:)=[minShp best];

end

end