function f = fitness(pop,indicator,price,scaling)
%   See also tradeSignal, initializePopulation
%%
% Copyright 2010, The MathWorks, Inc.
% All rights reserved.
%% Generate Trading Signal from Population
s = tradeSignal(pop,indicator);
col = size(s,2);

%% PNL Caclulation
r = [zeros(1,col); s(1:end-1,:).*repmat(tick2ret(price),1,col)];
f = -scaling*portalpha(r(2:end,:),tick2ret(price),0);