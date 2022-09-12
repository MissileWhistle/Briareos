function MiA=Dat_trans_v2(MDI)
MIDsize2=size(MDI,2);

%% In smooth and make-up

% Make-up
mk=10;

% In Smooth
SMT=[1:128; std(tick2ret(MDI))];
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

MID=zeros(size(MDI));
for i=1:MIDsize2
    if ismember(i,A1)==1
        MID(:,i)=MDI(:,i);
    elseif ismember(i,A2)==1
        MID(:,i)=smoothdata(MDI(:,i),'gaussian',3);
    elseif ismember(i,A3)==1
        MID(:,i)=smoothdata(MDI(:,i),'gaussian',5);
    elseif ismember(i,A4)==1
        MID(:,i)=smoothdata(MDI(:,i),'gaussian',7);
    elseif ismember(i,A5)==1
        MID(:,i)=smoothdata(MDI(:,i),'gaussian',9);
    elseif ismember(i,A6)==1
        MID(:,i)=smoothdata(MDI(:,i),'gaussian',11);
    elseif ismember(i,A7)==1
        MID(:,i)=smoothdata(MDI(:,i),'gaussian',13);
    end
end
%% Out smooth vals
% values relate to 170 days of backtest

% Smooth Scalar
m0=4;

MS=[1.6285    2.0104    0.5562    1.0323    1.5381    0.9890    1.6117    0.8718    1.5260    1.7957    1.8043 ...
    1.7157    1.7838    1.2806    1.8419    0.6670    1.3015    1.6787    0.8685    1.3011    1.6242    1.5487 ...
    1.7030    1.0047    1.5493    1.9537    1.3791    1.2778    1.7679    1.2981    2.3700    1.7711    1.9828 ...
    2.6404    1.3795    1.8862    1.2610    1.4424    1.8035    1.4358    1.5867    2.3927    1.8253    1.7799 ...
    1.6184    1.2903    2.6057    1.1176    1.1287    2.0490    1.6174    1.4005    1.3232    1.4956    0.9333 ...
    0.9707    1.4673    1.4710    1.8594    1.3998    1.7655    0.8623    1.9022    2.2983    1.8734    1.5082 ...
    1.5192    1.2867    1.0591    2.3178    1.4628    1.0440    1.4753    1.4035    1.2961    1.4718    1.6980 ...
    1.3496    1.3188    1.4338    0.8292    0.5429    0.6077    1.4171    0.5087    1.2507    1.7475    1.0816 ...
    1.2842    0.9478    1.1523    1.1183    0.8547    1.1007    0.9446    1.0102    0.7005    0.7280    0.8463 ...
    1.1920    1.4311    0.6965    2.1774    0.7517    0.4928    1.4010    0.7335    0.9900    1.1052    1.5787 ...
    2.3789    2.3780    2.3517    1.0109    1.0774    0.7725    1.2971    1.3883    0.9633    0.7865    0.9934 ...
    1.9311    1.6709    0.5781    0.6739    0.6956    1.7800    0.6870];

%% MiA

Mia(:,1)=log(MID(:,1));
Mia(:,2)=log(MID(:,2));
Mia(:,3)=-log(MID(:,3));
Mia(:,4)=log(MID(:,4));
Mia(:,5)=log(MID(:,5))+2;
for i=6:11
    Mia(:,i)=log(MID(:,i));
end
Mia(:,12)=log(MID(:,12))+4;
Mia(:,13)=log(MID(:,13));
Mia(:,14)=log(MID(:,14))+3;
for i=15:20
    Mia(:,i)=log(MID(:,i));
end
Mia(:,21)=log(MID(:,21))+12;
Mia(:,22)=log(MID(:,22));
Mia(:,23)=log(MID(:,23))+10;
for i=24:27
    Mia(:,i)=log(MID(:,i));
end
Mia(:,28)=log(MID(:,28))+2;
Mia(:,29)=log(MID(:,29))+2;
Mia(:,30)=log(MID(:,30))+9;
for i=31:34
    Mia(:,i)=log(MID(:,i));
end
Mia(:,35)=MID(:,35)+1;
for i=36:54
    Mia(:,i)=log(MID(:,i));
end
Mia(:,55)=MID(:,55);
Mia(:,56)=log(MID(:,56))+6;
Mia(:,57)=MID(:,57);
for i=58:62
    Mia(:,i)=log(MID(:,i));
end
Mia(:,63)=-log(MID(:,63));
for i=64:66
    Mia(:,i)=log(MID(:,i));
end
Mia(:,67)=log(MID(:,67))+5;
Mia(:,68)=log(MID(:,68))+2;
Mia(:,69)=log(MID(:,69))+2;
Mia(:,70)=log(MID(:,70))+3;
Mia(:,71)=log(MID(:,71))+1;
Mia(:,72)=log(MID(:,72))+3;
Mia(:,73)=log(MID(:,73))+2;
Mia(:,74)=log(MID(:,74));
Mia(:,75)=log(MID(:,75))+2;
Mia(:,76)=log(MID(:,76))+3;
Mia(:,77)=log(MID(:,77));
Mia(:,78)=log(MID(:,78))+1;
Mia(:,79)=log(MID(:,79));
Mia(:,80)=log(MID(:,80))+3;
Mia(:,81)=MID(:,81).^4;
Mia(:,82)=MID(:,82);
Mia(:,83)=MID(:,83).^4;
Mia(:,84)=log(MID(:,84));
Mia(:,85)=MID(:,85).^3;
Mia(:,86)=MID(:,86).^3;
Mia(:,87)=log(MID(:,87));
Mia(:,88)=MID(:,88).^2;
Mia(:,89)=MID(:,89).^2;
Mia(:,90)=(log(MID(:,90))-4).^4;
Mia(:,91)=MID(:,91).^4;
Mia(:,92)=MID(:,92);
Mia(:,93)=MID(:,93).^4;
Mia(:,94)=MID(:,94);
Mia(:,95)=MID(:,95).^2;
Mia(:,96)=MID(:,96).^3;
Mia(:,97)=MID(:,97);
Mia(:,98)=(log(MID(:,98))-3.3).^2 + 1;
Mia(:,99)=(log(MID(:,99))-4.8).^3 + 1;
for i=100:104
    Mia(:,i)=MID(:,i);
end
Mia(:,105)=MID(:,105).^(1/3);
Mia(:,106)=MID(:,106);
Mia(:,107)=MID(:,107).^(1/7);
Mia(:,108)=(log(MID(:,108))-4.3).^3 + 1;
Mia(:,109)=MID(:,109);
Mia(:,110)=MID(:,110).^(1/4);
Mia(:,111)=MID(:,111).^(1/3);
Mia(:,112)=MID(:,112);
Mia(:,113)=log(MID(:,113)).^(1/3);
Mia(:,114)=(log(MID(:,114))-2.6).^3 + 1;
Mia(:,115)=log(MID(:,115)).^3;
Mia(:,116)=log(MID(:,116)).^(1/4);
Mia(:,117)=log(MID(:,117))+3;
Mia(:,118)=log(MID(:,118))+7;
Mia(:,119)=log(MID(:,119))+5;
Mia(:,120)=log(MID(:,120)).^(1/3);
Mia(:,121)=log(MID(:,121))+4;
Mia(:,122)=log(MID(:,122));
Mia(:,123)=log(MID(:,123));
Mia(:,124)=log(MID(:,124));
Mia(:,125)=log(MID(:,125));
Mia(:,126)=log(MID(:,126)).^2;
Mia(:,127)=(log(MID(:,127))+2).^(1/2);
Mia(:,128)=MID(:,128)-mk;
Mia(isnan(Mia)==1 | isinf(Mia)==1)=0;
Mia=Mia+mk;

% Data Smooth

MiA=zeros(size(Mia));
for i=1:MIDsize2
    if round(m0*MS(i))==0 || round(m0*MS(i))==1
        MiA(:,i)=Mia(:,i);
    else
        MiA(:,i)=smoothdata(Mia(:,i),'gaussian',round(m0*MS(i)));
    end
end

end