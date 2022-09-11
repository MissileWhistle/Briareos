function [LongGSignal,RLongGSignal]=LongTrading(lPdc,lPdh,lPdl,lPdvol,LvarMACD,LvarOBV,LvarADL,LvarATR,LvarOSC,LvarCCI,LStrt,LPortd,LAPort)
%% Long-Term (LTPort%)
lPdsize=size(lPdc);
lPdsize2=size(lPdc,2);
%% L.Indicator Based Trading

%MACDs and Ind. variables 
lt1=LvarMACD(:,1)';
lt2=LvarMACD(:,2)';
lt3=LvarMACD(:,3)';
lot1=LvarOBV(:,1)';
lot2=LvarOBV(:,2)';
lot3=LvarOBV(:,3)';
ladt1=LvarADL(:,1)';
ladt2=LvarADL(:,2)';
ladt3=LvarADL(:,3)';
latt1=LvarATR(:,1)';
latt2=LvarATR(:,2)';
latt3=LvarATR(:,3)';
los1=LvarOSC(:,1)';
los2=LvarOSC(:,2)';
lact1=LvarCCI(:,1)';
lact2=LvarCCI(:,2)';

%Indicators
%LOBV
LOBV=zeros(lPdsize);
for i= 1:lPdsize2
  LOBV(:,i)=onbalvol([lPdc(:,i),lPdvol(:,i)]);
end

%LADLine
LADLine=zeros(lPdsize);
for i=1:lPdsize2
  LADLine(:,i)=willad([lPdh(:,i),lPdl(:,i),lPdc(:,i)]);
end

%ATR
LSATR=zeros(lPdsize);
for i=1:lPdsize2
  LSATR(:,i)=ATR(lPdh(:,i),lPdl(:,i),lPdc(:,i),latt1(i),latt2(i),latt3(i));
end

%CCI
LCCILine=zeros(lPdsize);
for i=1:lPdsize2
  LCCILine(:,i)=CCIf(lPdh(:,i),lPdl(:,i),lPdc(:,i),lact1(i),lact2(i));
end
    
%MACD
LMACDline=zeros(lPdsize);
LSignaline=zeros(lPdsize);
LMACDdiff=zeros(lPdsize);
for i=1:lPdsize2
  LMACDline(:,i)=movavg(lPdc(:,i),'exponential',lt1(i))-movavg(lPdc(:,i),'exponential',lt2(i));
  LMACDline(isnan(LMACDline))=0;
  LSignaline(:,i)=movavg(LMACDline(:,i),'exponential',lt3(i));
  LSignaline(isnan(LSignaline))=0;
  LMACDdiff(:,i)=LMACDline(:,i)-LSignaline(:,i);
end

%OVB MACD
LOBVMACDline=zeros(lPdsize);
LOBVSignaline=zeros(lPdsize);
LOBVMACDdiff=zeros(lPdsize);
for i=1:lPdsize2
  LOBVMACDline(:,i)=movavg(LOBV(:,i),'exponential',lot1(i))-movavg(LOBV(:,i),'exponential',lot2(i));
  LOBVMACDline(isnan(LOBVMACDline))=0;
  LOBVSignaline(:,i)=movavg(LOBVMACDline(:,i),'exponential',lot3(i));
  LOBVSignaline(isnan(LOBVSignaline))=0;
  LOBVMACDdiff(:,i)=LOBVMACDline(:,i)-LOBVSignaline(:,i);
end

%ADLine MACD
LADMACDline=zeros(lPdsize);
LADSignaline=zeros(lPdsize);
LADMACDdiff=zeros(lPdsize);
for i=1:lPdsize2
  LADMACDline(:,i)=movavg(LADLine(:,i),'exponential',ladt1(i))-movavg(LADLine(:,i),'exponential',ladt2(i));
  LADMACDline(isnan(LADMACDline))=0;
  LADSignaline(:,i)=movavg(LADMACDline(:,i),'exponential',ladt3(i));
  LADSignaline(isnan(LADSignaline))=0;
  LADMACDdiff(:,i)=LADMACDline(:,i)-LADSignaline(:,i);
end

%Stoch OSC 
LStochOSC=zeros(lPdsize);
for i=1:lPdsize2
  LStochOSC(:,i)=StOSC(lPdc(:,i),los1(i),los2(i));
end

%Strategies&Signals

%MACD Signal
LSMACD=LMACDdiff>0;

%OBV signal
LSOBV=LOBVMACDdiff>0;

%ADline Signal
LSAD=LADMACDdiff>0;

%StochOSC Signal
LSOSC=LStochOSC>0;

%CCI Signal
LSCCI=LCCILine>0;
%% L.Strategized Signals (Genetic)

LSig=zeros(lPdsize);
for i=1:lPdsize2
    lS=[LSMACD(:,i) LSOBV(:,i) LSAD(:,i) LSATR(:,i) LSOSC(:,i) LSCCI(:,i)];
    LSig(:,i)=tradeSignal(LStrt(i,:),lS);
end
RLongGSignal=LSig(end,:);
LongGSignal=LPortd*LAPort.*LSig(end,:);
disp("LongGSignal = "),disp(LongGSignal)
end