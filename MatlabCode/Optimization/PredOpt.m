
function RTT=PredOpt(P,MiFull,MdFull,lPdcFull,lPdvolFull,CCIPredA,CCPredA,zet)
t=35;
%% Opt Environment
for daycount=700:7:size(lPdcFull,1)-7

%% -> Predictions
CCPred=CCPredA{daycount-700+1};
CCIPred=CCIPredA{daycount-700+1};
%% Data
Mi=MiFull(daycount-7*t+1:daycount,:);
Md=MdFull(daycount-7*t+1:daycount,:);
Pd=lPdcFull(daycount-7*t+1:daycount,:);
Pdv=lPdvolFull(daycount-7*t+1:daycount,:);
Pdsize1=size(Pd,1);
%% CCI
CCIm = smooth((Md(4:end)-Md(1:end-3))/4,10);
CCImp = (CCIm(end)-CCIm(end-7+1))/CCIm(end-7+1);
ccipp = (Md(end)-Md(end-7+1))/Md(end-7+1);
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
        
ccist=zeros(size(Md,1)-4,1);
for i=4:size(Md,1)
    ccist(i) = std(Md(i-4+1:i));
end
ccistd = smoothdata(ccist,'gaussian',7);
ccistdp = (ccistd(end)-ccistd(end-7+1))/ccistd(end-7+1);
%% Crypto
switch zet
    case 1
        %% BTC
        btctx = smoothdata(Mi(:,1),'gaussian',6);
        btcad = smoothdata(Mi(:,6),'gaussian',6);
        btcap = (btctx(end)-btctx(end-7+1))/btctx(end-7+1) + (btcad(end)-btcad(end-7+1))/btcad(end-7+1);
        btci = smoothdata((Mi(:,66)+Mi(:,67))/2,'gaussian',6);
        btcip = (btci(end)-btci(end-7+1))/btci(end-7+1);
        btcp = Pd(:,1);
        btcpp = (btcp(end)-btcp(end-7+1))/btcp(end-7+1);
        btcvl=smoothdata(Pdv(:,1),'gaussian',10);
        btcvlp = (btcvl(end)-btcvl(end-7+1))/btcvl(end-7+1);
        btcst=zeros(Pdsize1-4,1);
        for i=4:Pdsize1
            btcst(i) = std(Pd(i-4+1:i,1));
        end
        btcstd = smoothdata(btcst,'gaussian',7);
        btcstdp = (btcstd(end)-btcstd(end-7+1))/btcstd(end-7+1);
        btcm = smoothdata((Pd(4:end,1)-Pd(1:end-3,1))/4,'gaussian',10);
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

        pbs(daycount-700+1) = P(1)*sign(btcap) + P(2)*gts + P(3)*sign(btcpp) + ...
            P(4)*sign(btcstdp)*sign(btcpp) + P(5)*sign(btcmp) + ...
            P(6)*sign(CCImp) + P(7)*vol + P(8)*sign(btcprp) + P(9)*sign(CCIprp) + ...
            P(10)*sign(cciap) + P(11)*ccigts + P(12)*sign(ccistdp)*sign(ccipp);
    case 2
        %% ETH
        ethtx = smoothdata(Mi(:,10),'gaussian',6);
        ethad = smoothdata(Mi(:,15),'gaussian',6);
        ethap = (ethtx(end)-ethtx(end-7+1))/ethtx(end-7+1) + (ethad(end)-ethad(end-7+1))/ethad(end-7+1);
        ethi = smoothdata((Mi(:,68)+Mi(:,69))/2,'gaussian',6);
        ethip = (ethi(end)-ethi(end-7+1))/ethi(end-7+1);
        ethp=Pd(:,2);
        ethpp = (ethp(end)-ethp(end-7+1))/ethp(end-7+1);
        ethvl=smoothdata(Pdv(:,2),'gaussian',10);
        ethvlp = (ethvl(end)-ethvl(end-7+1))/ethvl(end-7+1);
        ethst=zeros(Pdsize1-4,1);
        for i=4:Pdsize1
            ethst(i) = std(Pd(i-4+1:i,2));
        end
        ethstd = smoothdata(ethst,'gaussian',7);
        ethstdp = (ethstd(end)-ethstd(end-7+1))/ethstd(end-7+1);
        ethm = smoothdata((Pd(4:end,2)-Pd(1:end-3,2))/4,'gaussian',10);
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

        pbs(daycount-700+1) = P(1)*sign(ethap) + P(2)*gts + P(3)*sign(ethpp) + ...
            P(4)*sign(ethstdp)*sign(ethpp) + P(5)*sign(ethmp) + ...
            P(6)*sign(CCImp) + P(7)*vol + P(8)*sign(ethprp) + P(9)*sign(CCIprp) +...
            P(10)*sign(cciap) + P(11)*ccigts + P(12)*sign(ccistdp)*sign(ccipp);
    case 3
        %% XLM
        xlmtx = smoothdata(Mi(:,19),'gaussian',6);
        xlmap = (xlmtx(end)-xlmtx(end-7+1))/xlmtx(end-7+1);
        xlmi = smoothdata(Mi(:,72),'gaussian',6);
        xlmip = (xlmi(end)-xlmi(end-7+1))/xlmi(end-7+1);
        xlmp=Pd(:,3);
        xlmpp = (xlmp(end)-xlmp(end-7+1))/xlmp(end-7+1);
        xlmvl=smoothdata(Pdv(:,3),'gaussian',10);
        xlmvlp = (xlmvl(end)-xlmvl(end-7+1))/xlmvl(end-7+1);
        xlmst=zeros(Pdsize1-4,1);
        for i=4:Pdsize1
            xlmst(i) = std(Pd(i-4+1:i,2));
        end
        xlmstd = smoothdata(xlmst,'gaussian',7);
        xlmstdp = (xlmstd(end)-xlmstd(end-7+1))/xlmstd(end-7+1);
        xlmm = smoothdata((Pd(4:end,3)-Pd(1:end-3,3))/4,'gaussian',10);
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

        pbs(daycount-700+1) = P(1)*sign(xlmap) + P(2)*gts + P(3)*sign(xlmpp) + ...
            P(4)*sign(xlmstdp)*sign(xlmpp) + P(5)*sign(xlmmp) + ...
            P(6)*sign(CCImp) + P(7)*vol + P(8)*sign(xlmprp) + P(9)*sign(CCIprp) + ...
            P(10)*sign(cciap) + P(11)*ccigts + P(12)*sign(ccistdp)*sign(ccipp);
    case 4
        %% XMR
        xmrtx = smoothdata(Mi(:,22),'gaussian',6);
        xmrap = (xmrtx(end)-xmrtx(end-7+1))/xmrtx(end-7+1);
        xmri = smoothdata(Mi(:,70),'gaussian',6);
        xmrip = (xmri(end)-xmri(end-7+1))/xmri(end-7+1);
        xmrp=Pd(:,3);
        xmrpp = (xmrp(end)-xmrp(end-7+1))/xmrp(end-7+1);
        xmrvl=smoothdata(Pdv(:,3),'gaussian',10);
        xmrvlp = (xmrvl(end)-xmrvl(end-7+1))/xmrvl(end-7+1);
        xmrst=zeros(Pdsize1-4,1);
        for i=4:Pdsize1
            xmrst(i) = std(Pd(i-4+1:i,3));
        end
        xmrstd = smoothdata(xmrst,'gaussian',7);
        xmrstdp = (xmrstd(end)-xmrstd(end-7+1))/xmrstd(end-7+1);
        xmrm = smoothdata((Pd(4:end,3)-Pd(1:end-3,3))/4,'gaussian',10);
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

        pbs(daycount-700+1) = P(1)*sign(xmrap) + P(2)*gts + P(3)*sign(xmrpp) + ...
            P(4)*sign(xmrstdp)*sign(xmrpp) + P(5)*sign(xmrmp) + ...
            P(6)*sign(CCImp) + P(7)*vol + P(8)*sign(xmrprp) + P(9)*sign(CCIprp) + ...
            P(10)*sign(cciap) + P(11)*ccigts + P(12)*sign(ccistdp)*sign(ccipp);
    case 5
        %% XRP
        xrptx = smoothdata(Mi(:,26),'gaussian',6);
        xrpad = smoothdata(Mi(:,28),'gaussian',6);
        xrpap = (xrptx(end)-xrptx(end-7+1))/xrptx(end-7+1) + (xrpad(end)-xrpad(end-7+1))/xrpad(end-7+1);
        xrpi = smoothdata((Mi(:,71)+Mi(:,75))/2,'gaussian',6);
        xrpip = (xrpi(end)-xrpi(end-7+1))/xrpi(end-7+1);
        xrpp=Pd(:,4);
        xrppp = (xrpp(end)-xrpp(end-7+1))/xrpp(end-7+1);
        xrpvl=smoothdata(Pdv(:,4),'gaussian',10);
        xrpvlp = (xrpvl(end)-xrpvl(end-7+1))/xrpvl(end-7+1);
        xrpst=zeros(Pdsize1-4,1);
        for i=4:Pdsize1
            xrpst(i) = std(Pd(i-4+1:i,4));
        end
        xrpstd = smoothdata(xrpst,'gaussian',7);
        xrpstdp = (xrpstd(end)-xrpstd(end-7+1))/xrpstd(end-7+1);
        xrpm = smoothdata((Pd(4:end,4)-Pd(1:end-3,4))/4,'gaussian',10);
        xrpmp = (xrpm(end)-xrpm(end-7+1))/xrpm(end-7+1);
        xrppr=smoothdata(CCPred(:,4),'gaussian',10);
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

        pbs(daycount-700+1) = P(1)*sign(xrpap) + P(2)*gts + P(3)*sign(xrppp) + ...
            P(4)*sign(xrpstdp)*sign(xrppp) + P(5)*sign(xrpmp) + ...
            P(6)*sign(CCImp) + P(7)*vol + P(8)*sign(xrpprp) + P(9)*sign(CCIprp) + ...
            P(10)*sign(cciap) + P(11)*ccigts + P(12)*sign(ccistdp)*sign(ccipp);
    case 6
        %% LINK
        linktx = smoothdata(Mi(:,31),'gaussian',6);
        linkad = smoothdata(Mi(:,32),'gaussian',6);
        linkap = (linktx(end)-linktx(end-7+1))/linktx(end-7+1) + (linkad(end)-linkad(end-7+1))/linkad(end-7+1);
        linki = smoothdata(Mi(:,73),'gaussian',6);
        linkip = (linki(end)-linki(end-7+1))/linki(end-7+1);
        linkp=Pd(:,6);
        linkpp = (linkp(end)-linkp(end-7+1))/linkp(end-7+1);
        linkvl=smoothdata(Pdv(:,6),'gaussian',10);
        linkvlp = (linkvl(end)-linkvl(end-7+1))/linkvl(end-7+1);
        linkst=zeros(Pdsize1-4,1);
        for i=4:Pdsize1
            linkst(i) = std(Pd(i-4+1:i,6));
        end
        linkstd = smoothdata(linkst,'gaussian',7);
        linkstdp = (linkstd(end)-linkstd(end-7+1))/linkstd(end-7+1);
        linkm = smoothdata((Pd(4:end,6)-Pd(1:end-3,6))/4,'gaussian',10);
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

        pbs(daycount-700+1) = P(1)*sign(linkap) + P(2)*gts + P(3)*sign(linkpp) + ...
            P(4)*sign(linkstdp)*sign(linkpp) + P(5)*sign(linkmp) + ...
            P(6)*sign(CCImp) + P(7)*vol + P(8)*sign(linkprp) + P(9)*sign(CCIprp) + ...
            P(10)*sign(cciap) + P(11)*ccigts + P(12)*sign(ccistdp)*sign(ccipp); 
    case 7
        %% NEO
        neotx = smoothdata(Mi(:,36),'gaussian',6);
        neoad = smoothdata(Mi(:,37),'gaussian',6);
        neoap = (neotx(end)-neotx(end-7+1))/neotx(end-7+1) + (neoad(end)-neoad(end-7+1))/neoad(end-7+1);
        neoi = smoothdata(Mi(:,74),'gaussian',6);
        neoip = (neoi(end)-neoi(end-7+1))/neoi(end-7+1);
        neop=Pd(:,7);
        neopp = (neop(end)-neop(end-7+1))/neop(end-7+1);
        neovl=smoothdata(Pdv(:,7),'gaussian',10);
        neovlp = (neovl(end)-neovl(end-7+1))/neovl(end-7+1);
        neost=zeros(Pdsize1-4,1);
        for i=4:Pdsize1
            neost(i) = std(Pd(i-4+1:i,7));
        end
        neostd = smoothdata(neost,'gaussian',7);
        neostdp = (neostd(end)-neostd(end-7+1))/neostd(end-7+1);
        neom = smoothdata((Pd(4:end,7)-Pd(1:end-3,7))/4,'gaussian',10);
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

        pbs(daycount-700+1) = P(1)*sign(neoap) + P(2)*gts + P(3)*sign(neopp) + ...
            P(4)*sign(neostdp)*sign(neopp) + P(5)*sign(neomp) + ...
            P(6)*sign(CCImp) + P(7)*vol + P(8)*sign(neoprp) + P(9)*sign(CCIprp) + ...
            P(10)*sign(cciap) + P(11)*ccigts + P(12)*sign(ccistdp)*sign(ccipp); 
end

end

RTP=pbs(1:7:end)';
Dat=lPdcFull(700:7:daycount+7,zet);
RTT=-sum(sign(RTP)==sign(tick2ret(Dat)),1)/(size(RTP,1));
end