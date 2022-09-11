function [ShortGSignal, RShortGSignal]=ShortTrading(sPdc,sPdh,sPdl,sPdvol,SvarMACD,SvarOBV,SvarADL,SvarATR,SvarOSC,SvarCCI,SStrt,SPortd,SAPort)
%% Short-Term
sPdsize=size(sPdc);
sPdsize2=size(sPdc,2);
%% S.Indicator Based Trading

%Indicators

%MACDs and Ind. variables 
t1=SvarMACD(:,1)';
t2=SvarMACD(:,2)';
t3=SvarMACD(:,3)';
ot1=SvarOBV(:,1)';
ot2=SvarOBV(:,2)';
ot3=SvarOBV(:,3)';
adt1=SvarADL(:,1)';
adt2=SvarADL(:,2)';
adt3=SvarADL(:,3)';
att1=SvarATR(:,1)';
att2=SvarATR(:,2)';
att3=SvarATR(:,3)';
os1=SvarOSC(:,1)';
os2=SvarOSC(:,2)';
act1=SvarCCI(:,1)';
act2=SvarCCI(:,2)';

%OBV
OBV=zeros(sPdsize);
for i=1:sPdsize2
  OBV(:,i)=onbalvol([sPdc(:,i),sPdvol(:,i)]);
end

%ADLine
ADLine=zeros(sPdsize);
for i=1:sPdsize2
  ADLine(:,i)=willad([sPdh(:,i),sPdl(:,i),sPdc(:,i)]);
end

%ATR
SATR=zeros(sPdsize);
for i=1:sPdsize2
  SATR(:,i)=ATR(sPdh(:,i),sPdl(:,i),sPdc(:,i),att1(i),att2(i),att3(i));
end

%CCI
CCILine=zeros(sPdsize);
for i=1:sPdsize2
  CCILine(:,i)=CCIf(sPdh(:,i),sPdl(:,i),sPdc(:,i),act1(i),act2(i));
end
    
%MACD
MACDline=zeros(sPdsize);
Signaline=zeros(sPdsize);
MACDdiff=zeros(sPdsize);
for i=1:sPdsize2
  MACDline(:,i)=movavg(sPdc(:,i),'exponential',t1(i))-movavg(sPdc(:,i),'exponential',t2(i));
  MACDline(isnan(MACDline))=0;
  Signaline(:,i)=movavg(MACDline(:,i),'exponential',t3(i));
  Signaline(isnan(Signaline))=0;
  MACDdiff(:,i)=MACDline(:,i)-Signaline(:,i);
end

%OVB MACD
OBVMACDline=zeros(sPdsize);
OBVSignaline=zeros(sPdsize);
OBVMACDdiff=zeros(sPdsize);
for i=1:sPdsize2
  OBVMACDline(:,i)=movavg(OBV(:,i),'exponential',ot1(i))-movavg(OBV(:,i),'exponential',ot2(i));
  OBVMACDline(isnan(OBVMACDline))=0;
  OBVSignaline(:,i)=movavg(OBVMACDline(:,i),'exponential',ot3(i));
  OBVSignaline(isnan(OBVSignaline))=0;
  OBVMACDdiff(:,i)=OBVMACDline(:,i)-OBVSignaline(:,i);
end
  
%ADLine MACD
ADMACDline=zeros(sPdsize);
ADSignaline=zeros(sPdsize);
ADMACDdiff=zeros(sPdsize);
for i=1:sPdsize2
  ADMACDline(:,i)=movavg(ADLine(:,i),'exponential',adt1(i))-movavg(ADLine(:,i),'exponential',adt2(i));
  ADMACDline(isnan(ADMACDline))=0;
  ADSignaline(:,i)=movavg(ADMACDline(:,i),'exponential',adt3(i));
  ADSignaline(isnan(ADSignaline))=0;
  ADMACDdiff(:,i)=ADMACDline(:,i)-ADSignaline(:,i);
end

%Stoch OSC (StockOSC{i}=[PercentK,PercentD])
StochOSC=zeros(sPdsize);
for i=1:sPdsize2
  StochOSC(:,i)=StOSC(sPdc(:,i),os1(i),os2(i));
end

%Strategies&Signals

%MACD Signal
SMACD=MACDdiff>0;

%OBV signal
SOBV=OBVMACDdiff>0;

%ADline Signal
SAD=ADMACDdiff>0;

%StochOSC Signal
SOSC=StochOSC>0;

%CCI Signal
SCCI=CCILine>0;
%% S.Strategized Signals (Genetic)
%fees&spread not accounted


SSig=zeros(sPdsize);
for i=1:sPdsize2
    S=[SMACD(:,i) SOBV(:,i) SAD(:,i) SATR(:,i) SOSC(:,i) SCCI(:,i)];
    SSig(:,i)=tradeSignal(SStrt(i,:),S);
end
RShortGSignal=SSig(end,:);
ShortGSignal=SPortd*SAPort.*SSig(end,:);
disp("ShortGSignal = "),disp(ShortGSignal)