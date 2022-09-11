function LStrt=LongTermOptGO(lPdcFull,lPdhFull,lPdlFull,lPdvolFull,LvarMACD,LvarOBV,LvarADL,LvarATR,LvarOSC,LvarCCI)
lPdsize2=size(lPdcFull,2);

LStrt=zeros(lPdsize2,23);
for i=1:lPdsize2
    %% Indicators

     %MACDs variables 
    lt1=LvarMACD(i,1);
    lt2=LvarMACD(i,2);
    lt3=LvarMACD(i,3);
    lot1=LvarOBV(i,1);
    lot2=LvarOBV(i,2);
    lot3=LvarOBV(i,3);
    ladt1=LvarADL(i,1);
    ladt2=LvarADL(i,2);
    ladt3=LvarADL(i,3);
    latt1=LvarATR(i,1);
    latt2=LvarATR(i,2);
    latt3=LvarATR(i,3);
    lact1=LvarCCI(i,1);
    lact2=LvarCCI(i,2);

    %LOBV
    LOBV=onbalvol([lPdcFull(:,i),lPdvolFull(:,i)]);

    %LADLine
    LADLine=willad([lPdhFull(:,i),lPdlFull(:,i),lPdcFull(:,i)]);

    %ATRLine
    LSATRbuy=ATR(lPdhFull(:,i),lPdlFull(:,i),lPdcFull(:,i),latt1,latt2,latt3);

    %CCI
    LCCILine=CCIf(lPdhFull(:,i),lPdlFull(:,i),lPdcFull(:,i),lact1,lact2);

    %MACD
    LMACDline=movavg(lPdcFull(:,i),'exponential',lt1)-movavg(lPdcFull(:,i),'exponential',lt2);
    LMACDline(isnan(LMACDline))=0;
    LSignaline=movavg(LMACDline,'exponential',lt3);
    LSignaline(isnan(LSignaline))=0;
    LMACDdiff=LMACDline-LSignaline;

    %OVB MACD
    LOBVMACDline=movavg(LOBV,'exponential',lot1)-movavg(LOBV,'exponential',lot2);
    LOBVMACDline(isnan(LOBVMACDline))=0;
    LOBVSignaline=movavg(LOBVMACDline,'exponential',lot3);
    LOBVSignaline(isnan(LOBVSignaline))=0;
    LOBVMACDdiff=LOBVMACDline-LOBVSignaline;

    %ADLine MACD
    LADMACDline=movavg(LADLine,'exponential',ladt1)-movavg(LADLine,'exponential',ladt2);
    LADMACDline(isnan(LADMACDline))=0;
    LADSignaline=movavg(LADMACDline,'exponential',ladt3);
    LADSignaline(isnan(LADSignaline))=0;
    LADMACDdiff=LADMACDline-LADSignaline;

    %Stoch Oscilator variables 
    la=LvarOSC(i,1);
    ld=LvarOSC(i,2);

    %Stoch OSC 
    LStochOSC=StOSC(lPdcFull(:,i),la,ld);

    %Strategies&Signals

    %MACD Signal
    LSMACDbuy=LMACDdiff>0;

    %OBV signal
    LSOBVbuy=LOBVMACDdiff>0;

    %ADline Signal
    LSADbuy=LADMACDdiff>0;

    %StochOSC Signal
    LPSOSC=LStochOSC>0;

    %CCI Signal
    LPSCCI=LCCILine>0;
    %% Strategy
    S=[LSMACDbuy(500:end) LSOBVbuy(500:end) LSADbuy(500:end) LSATRbuy(500:end) LPSOSC(500:end) LPSCCI(500:end)];

    scaling=1;
    I=size(S,2);
    popSize=2^(I*2); 
    pop = initializePopulation(I,popSize);

    obj = @(pop) fitness(pop,S,lPdcFull(500:end,i),scaling);

    options = gaoptimset('Display','iter','PopulationType','bitstring',...
        'PopulationSize',size(pop,1),...
        'InitialPopulation',pop,...
        'CrossoverFcn', @crossover,...
        'MutationFcn', @mutation,...
        'Vectorized','on'); %#ok<GAOPT>

    [best,minSh] = ga(obj,size(pop,2),[],[],[],[],[],[],[],options);
    minShp=-minSh;
    LStrt(i,:)=[minShp best];  
end

end