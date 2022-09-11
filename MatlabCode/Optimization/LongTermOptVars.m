function [LvarMACD,LvarOBV,LvarADL,LvarATR,LvarOSC,LvarCCI]=LongTermOptVars(lPdcFull,lPdhFull,lPdlFull,lPdvolFull)
%% Indicators
lPdsize2=size(lPdcFull,2);

%% MACD
LvarMACD=zeros(lPdsize2,4);
for i=1:lPdsize2
    opts=zeros(200,250,200);
    optv=cell(200,250,200);
    lPdc=lPdcFull(:,i);
    parfor a=1:200
        for b=1:250
            for c=1:200
                V=[a b c];
                
                %MACD
                MACDline=movavg(lPdc,'exponential',a)-movavg(lPdc,'exponential',b);
                MACDline(isnan(MACDline))=0;
                Signaline=movavg(MACDline,'exponential',c);
                Signaline(isnan(Signaline))=0;
                MACDdiff=MACDline-Signaline;

                %MACD Signal
                SMACDbuy=MACDdiff>0;

                PDret=tick2ret(lPdc(450:end));
                SCS1=SMACDbuy(450:end-1).*PDret;
                S=portalpha(SCS1,PDret,0);
                if isnan(S)==1
                    S=-inf;
                end
                
                opts(a,b,c)=S; 
                optv{a,b,c}=V;
             end
         end
    end
    r=max(max(max(opts(opts~=-inf))));
    x=find(opts==r(1),1);
    [l,j,k]=ind2sub([200,250,200],x);
    s=optv{l,j,k};
    LvarMACD(i,:)=[r s];
end
disp('LvarMACD = ')
disp(LvarMACD)
%% OBV
LvarOBV=zeros(lPdsize2,4);
for i=1:lPdsize2
    opts=zeros(200,250,200);
    optv=cell(200,250,200);
    lPdc = lPdcFull(:,i);
    lPdvol = lPdvolFull(:,i);
    parfor a=1:200
        for b=1:250
            for c=1:200
                V=[a b c];

                %OBV
                OBV=onbalvol([lPdc,lPdvol]);

                %OVB MACD
                OBVMACDline=movavg(OBV,'exponential',a)-movavg(OBV,'exponential',b);
                OBVMACDline(isnan(OBVMACDline))=0;
                OBVSignaline=movavg(OBVMACDline,'exponential',c);
                OBVSignaline(isnan(OBVSignaline))=0;
                OBVMACDdiff=OBVMACDline-OBVSignaline;

                %OBV signal
                SOBVbuy=OBVMACDdiff>0;

                PDret=tick2ret(lPdc(450:end));
                SCS1=SOBVbuy(450:end-1).*PDret;
                S=portalpha(SCS1,PDret,0)
                if isnan(S)==1
                    S=-inf;
                end
                    
                opts(a,b,c)=S; 
                optv{a,b,c}=V;
             end
         end
    end
    r=max(max(max(opts(opts~=-inf))));
    x=find(opts==r(1),1);
    [l,j,k]=ind2sub([200,250,200],x);
    s=optv{l,j,k};
    LvarOBV(i,:)=[r s];
end
disp('LvarOBV = ')
disp(LvarOBV)
%% AD Line
LvarADL=zeros(lPdsize2,4);
for i=1:lPdsize2
    opts=zeros(200,250,200);
    optv=cell(200,250,200);
    lPdh = lPdhFull(:,i);
    lPdl = lPdlFull(:,i);
    lPdc = lPdcFull(:,i);
    parfor a=1:200
        for b=1:250
            for c=1:200
                V=[a b c];
                
                %ADLine
                ADLine=willad([lPdh,lPdl,lPdc]);

                %ADLine MACD
                ADMACDline=movavg(ADLine,'exponential',a)-movavg(ADLine,'exponential',b);
                ADMACDline(isnan(ADMACDline))=0;
                ADSignaline=movavg(ADMACDline,'exponential',c);
                ADSignaline(isnan(ADSignaline))=0;
                ADMACDdiff=ADMACDline-ADSignaline;

                %ADline Signal
                SADbuy=ADMACDdiff>0;

                PDret=tick2ret(lPdc(450:end));
                SCS1=SADbuy(450:end-1).*PDret;
                S=portalpha(SCS1,PDret,0);
                if isnan(S)==1
                    S=-inf;
                end

                opts(a,b,c)=S; 
                optv{a,b,c}=V;
             end
         end
    end
    r=max(max(max(opts(opts~=-inf))));
    x=find(opts==r(1),1);
    [l,j,k]=ind2sub([200,250,200],x);
    s=optv{l,j,k};
    LvarADL(i,:)=[r s];
end
disp('LvarADL = ')
disp(LvarADL)
%% ATR
LvarATR=zeros(lPdsize2,4);
for i=1:lPdsize2
    opts=zeros(200,200,100);
    optv=cell(200,200,100);
    lPdh = lPdhFull(:,i);
    lPdl = lPdlFull(:,i);
    lPdc = lPdcFull(:,i);
    parfor a=1:200
        for b=1:200
            for c=1:100
                V=[a b c];

                %ADLine Signal
                SATRbuy=ATR(lPdh,lPdl,lPdc,a,b,c);

                PDret=tick2ret(lPdc(500:end));
                SCS1=SATRbuy(500:end-1).*PDret;
                S=portalpha(SCS1,PDret,0);
                if isnan(S)==1
                    S=-inf;
                end
                
                opts(a,b,c)=S; 
                optv{a,b,c}=V;
            end
         end
    end
    r=max(max(max(opts(opts~=-inf))));
    x=find(opts==r(1),1);
    [l,j,k]=ind2sub([200,200,100],x);
    s=optv{l,j,k};
    LvarATR(i,:)=[r s];
end
disp('LvarATR = ')
disp(LvarATR)
%% OSC
LvarOSC=zeros(lPdsize2,3);
for i=1:lPdsize2
    opts=zeros(250,249);
    optv=cell(250,249);
    lPdc = lPdcFull(:,i);
    parfor a=1:250 
        for b=1:249
            V=[a b+1];
            f=V(1);
            s=V(2);

            %Stoch OSC
            StochOSC=StOSC(lPdc,f,s);

            %StochOSC Signal
            PSOSC=StochOSC>0;

            PDret=tick2ret(lPdc(500:end));
            SCS1=PSOSC(500:end-1).*PDret;
            S=portalpha(SCS1,PDret,0);
            if isnan(S)==1
                S=-inf;
            end

            opts(a,b)=S; 
            optv{a,b}=V;
        end
    end
    r=max(max(opts(opts~=-inf)));
    [k,y]=find(opts==r(1),1);
    s=optv{k,y};
    LvarOSC(i,:)=[r s];
end
disp('LvarOSC = ')
disp(LvarOSC)
%% CCI
LvarCCI=zeros(lPdsize2,3);
for i=1:lPdsize2
    opts=zeros(249,249);
    optv=cell(249,249);
    lPdh = lPdhFull(:,i);
    lPdl = lPdlFull(:,i);
    lPdc = lPdcFull(:,i);
    parfor a=1:249 
        for b=1:249
            V=[a+1 b+1];
            f=V(1);
            s=V(2);
            
            %CCI
            CCI=CCIf(lPdh,lPdl,lPdc,f,s);

            %CCI Signal
            PSCCI=CCI>0;
            PDret=tick2ret(lPdc(500:end));
            SCS1=PSCCI(500:end-1).*PDret;
            S=portalpha(SCS1,PDret,0);
            if isnan(S)==1
               S=-inf;
            end

            opts(a,b)=S; 
            optv{a,b}=V;
        end
    end
    r=max(max(opts(opts~=-inf)));
    [k,y]=find(opts==r(1),1);
    s=optv{k,y};
    LvarCCI(i,:)=[r s];
end
disp('LvarCCI = ')
disp(LvarCCI)
end