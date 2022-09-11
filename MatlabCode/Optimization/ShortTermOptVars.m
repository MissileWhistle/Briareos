function [SvarMACD,SvarOBV,SvarADL,SvarATR,SvarOSC,SvarCCI]=ShortTermOptVars(sPdcFull,sPdhFull,sPdlFull,sPdvolFull)
%% Indicators
sPdsize2=size(sPdcFull,2);

%% MACD
SvarMACD=zeros(sPdsize2,4);
for i=1:sPdsize2
    opts=zeros(200,250,200);
    optv=cell(200,250,200);
    sPdc=sPdcFull(:,i);
    parfor a=1:200
        for b=1:250
            for c=1:200
                V=[a b c];
                t1=V(1);
                t2=V(2);
                t3=V(3);

                % MACD
                MACDline=movavg(sPdc,'exponential',t1)-movavg(sPdc,'exponential',t2);
                MACDline(isnan(MACDline))=0;
                Signaline=movavg(MACDline,'exponential',t3);
                Signaline(isnan(Signaline))=0;
                MACDdiff=MACDline-Signaline;

                % MACD Signal
                SMACDbuy=MACDdiff>0;

                PDret=tick2ret(sPdc(450:end));
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
    SvarMACD(i,:)=[r s]; 
end
disp('SvarMACD = ')
disp(SvarMACD)
%% OBV
SvarOBV=zeros(sPdsize2,4);
for i=1:sPdsize2
    opts=zeros(200,250,200);
    optv=cell(200,250,200);
    sPdc = sPdcFull(:,i);
    sPdvol = sPdvolFull(:,i);
    parfor a=1:200
         for b=1:250
             for c=1:200
                V=[a b c];
                ot1=V(1);
                ot2=V(2);
                ot3=V(3);

                %OBV
                OBV=onbalvol([sPdc,sPdvol]);

                %OVB MACD
                OBVMACDline=movavg(OBV,'exponential',ot1)-movavg(OBV,'exponential',ot2);
                OBVMACDline(isnan(OBVMACDline))=0;
                OBVSignaline=movavg(OBVMACDline,'exponential',ot3);
                OBVSignaline(isnan(OBVSignaline))=0;
                OBVMACDdiff=OBVMACDline-OBVSignaline;

                %OBV signal
                SOBVbuy=OBVMACDdiff>0;

                PDret=tick2ret(sPdc(450:end));
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
    SvarOBV(i,:)=[r s];
end
disp('SvarOBV = ')
disp(SvarOBV)
%% AD Line
SvarADL=zeros(sPdsize2,4);
for i=1:sPdsize2
    opts=zeros(200,250,200);
    optv=cell(200,250,200);
    sPdh = sPdhFull(:,i);
    sPdl = sPdlFull(:,i);
    sPdc = sPdcFull(:,i);
    parfor a=1:200    
         for b=1:250
             for c=1:200
                V=[a b c];

                %ADLine
                ADLine=willad([sPdh,sPdl,sPdc]);

                %ADLine MACD
                ADMACDline=movavg(ADLine,'exponential',a)-movavg(ADLine,'exponential',b);
                ADMACDline(isnan(ADMACDline))=0;
                ADSignaline=movavg(ADMACDline,'exponential',c);
                ADSignaline(isnan(ADSignaline))=0;
                ADMACDdiff=ADMACDline-ADSignaline;

                %ADline Signal
                SADbuy=ADMACDdiff>0;

                PDret=tick2ret(sPdc(450:end));
                SCS1=SADbuy(450:end-1).*PDret;
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
    SvarADL(i,:)=[r s];
end
disp('SvarADL = ')
disp(SvarADL)
%% ATR
SvarATR=zeros(sPdsize2,4);
for i=1:sPdsize2
    opts=zeros(200,200,100);
    optv=cell(200,200,100);
    sPdh = sPdhFull(:,i);
    sPdl = sPdlFull(:,i);
    sPdc = sPdcFull(:,i);
    parfor a=1:200    
         for b=1:200
             for c=1:100
                V=[a b c];

                %ATR Signal
                SATRbuy=ATR(sPdh,sPdl,sPdc,a,b,c);

                PDret=tick2ret(sPdc(500:end));
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
    SvarATR(i,:)=[r s];
end
disp('SvarATR = ')
disp(SvarATR)
%% OSC
SvarOSC=zeros(sPdsize2,3);
for i=1:sPdsize2
    opts=zeros(250,249);
    optv=cell(250,249);
    sPdc = sPdcFull(:,i);
    parfor a=1:250
        for b=1:249
            V=[a b+1];
            f=V(1);
            s=V(2);

            %Stoch OSC
            StochOSC=StOSC(sPdc,f,s);

            %StochOSC Signal
            PSOSC=StochOSC>0;
            
            PDret=tick2ret(sPdc(500:end));
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
    SvarOSC(i,:)=[r s];
end
disp('SvarOSC = ')
disp(SvarOSC)
%% CCI
SvarCCI=zeros(sPdsize2,3);
for i=1:sPdsize2
    opts=zeros(249,249);
    optv=cell(249,249);
    sPdh = sPdhFull(:,i);
    sPdl = sPdlFull(:,i);
    sPdc = sPdcFull(:,i);
    parfor a=1:249
        for b=1:249
            V=[a+1 b+1];
            f=V(1);
            s=V(2);
            
            %CCI
            CCI=CCIf(sPdh,sPdl,sPdc,f,s);

            %CCI Signal
            PSCCI=CCI>0;
            
            PDret=tick2ret(sPdc(500:end));
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
    SvarCCI(i,:)=[r s];
end
disp('SvarCCI = ')
disp(SvarCCI)
end