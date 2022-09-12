from fpdf import FPDF
import numpy as np
import pandas as pd
import matlab.engine
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt
import mysql.connector
from datetime import date, timedelta
import time

def Report():
    # same database as Briareos Algo Trading System
    Database = mysql.connector.connect(
        host="",
        user="",
        passwd="")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    # matlab-python api; engine  working directory
    eng = matlab.engine.start_matlab()
    eng.cd(r'C:\Users\HC.deptR&D\Desktop\Report Generator and Twitter\Matlab Funcs', nargout=0)
    eng.ls(nargout=0)

    Tdate = date.today()

    # Data and Plots

    # Global Market conditions

    # Adoption

    query = f"SELECT date " \
            f"FROM btcMD " \
            f"ORDER BY date DESC " \
            f"LIMIT 100 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [list(item) for item in col]
    list.reverse(Col)
    Dates = np.asarray(Col)

    Crypto_str = ['btc', 'eth', 'xrp', 'link', 'usdt', 'doge', 'ada', 'ltc']
    Cry_AdrCnt = np.zeros((100, 8))
    i = 0
    for crypto in Crypto_str:
        query = f"SELECT AdrActCnt " \
                f"FROM {crypto}MD " \
                f"ORDER BY date DESC " \
                f"LIMIT 100 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        list.reverse(Col)
        Cry_AdrCnt[:, i] = np.reshape(np.asarray(Col), -1)
        i += 1

    Crypto_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'doge', 'ada', 'ltc']
    Cry_TxCnt = np.zeros((100, 9))
    i = 0
    for crypto in Crypto_str:
        query = f"SELECT TxCnt " \
                f"FROM {crypto}MD " \
                f"ORDER BY date DESC " \
                f"LIMIT 100 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        list.reverse(Col)
        Cry_TxCnt[:, i] = np.reshape(np.asarray(Col), -1)
        i += 1

    AdrCntInd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(Cry_AdrCnt/np.mean(Cry_AdrCnt, axis=0),
                                                                                 axis=1))),'gaussian',6)).reshape(100,)
    TxCntInd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(Cry_TxCnt/np.mean(Cry_TxCnt, axis=0), axis=1))),
                                         'gaussian',6)).reshape(100,)

    query = f"SELECT Bitcoin, BTC, ETH, Ethereum, Monero, Ripple_crypto, Stellar_Lumens, ChainLink, NEO_price, XRP, " \
                    f"blockchain, cryptocurrency, altcoin, Smart_Contract, Binance " \
                    f"FROM GT_searches " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 100 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [list(item) for item in col]
    list.reverse(Col)
    GTdata = np.asarray(Col)

    GTInd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata, axis=1)/14)),'gaussian',6)).reshape(100,)

    # Market Cap. Dominance

    cg = CoinGeckoAPI()

    CGlist = cg.get_coins_markets(vs_currency='usd')
    Clist = []
    for i in range(len(CGlist)):
        rnk = CGlist[i]['market_cap_rank']
        if rnk <= 6 and rnk != 1:
            Clist += [CGlist[i]['id']]

    CSu = np.zeros((100, len(Clist)))
    for i in range(len(Clist)):
        try:
            Dat = cg.get_coin_market_chart_by_id(id=Clist[i], vs_currency='usd', days=99)
        except:
            try:
                time.sleep(20)
                Dat = cg.get_coin_market_chart_by_id(id=Clist[i], vs_currency='usd', days=99)
            except:
                time.sleep(60)
                Dat = cg.get_coin_market_chart_by_id(id=Clist[i], vs_currency='usd', days=99)
        CMK = np.asarray(Dat['market_caps'])[:, 1]
        CSu[:, i] = CMK

    MainCMK = np.sum(CSu, axis=1)

    query = f"SELECT price " \
            f"FROM CryptoIndex " \
            f"ORDER BY date DESC " \
            f"LIMIT 100 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [item for sublist in [list(i) for i in col] for item in sublist]
    list.reverse(Col)
    TMK = np.asarray(Col)*10000000

    MainPer = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(MainCMK/TMK)),'gaussian',5)).reshape(100,)
    AltPer = 1-MainPer

    # Crypto Index

    CGlist = cg.get_coins_markets(vs_currency='usd')
    Clist = []
    for i in range(len(CGlist)):
        rnk = CGlist[i]['market_cap_rank']
        if rnk <= 30:
            Clist += [CGlist[i]['id']]

    CSP = np.zeros((122, len(Clist)))
    CSQ = np.zeros((1, len(Clist)))
    for i in range(len(Clist)):
        try:
            Dat = cg.get_coin_market_chart_by_id(id=Clist[i], vs_currency='usd', days=121)
        except:
            try:
                time.sleep(20)
                Dat = cg.get_coin_market_chart_by_id(id=Clist[i], vs_currency='usd', days=121)
            except:
                time.sleep(60)
                Dat = cg.get_coin_market_chart_by_id(id=Clist[i], vs_currency='usd', days=121)
        CMK = np.asarray(Dat['market_caps'])[:, 1]
        CMP = np.asarray(Dat['prices'])[:, 1]
        CSQ[0, i] = CMK[0]/CMP[0]
        CSP[:, i] = CMP

    CCI = 100 * np.sum(CSP*CSQ, axis=1) / np.sum(CSP[0, ]*CSQ)

    # CCI Predictions

    t = 35

    query = f"SELECT price " \
            f"FROM CryptoIndex " \
            f"ORDER BY date DESC " \
            f"LIMIT 700 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [item for sublist in [list(i) for i in col] for item in sublist]
    list.reverse(Col)
    Md = eng.transpose(matlab.double(Col[(-7 * t):]))
    mdfll = Col

    Cry_str = ['BTCUSDT', 'ETHUSDT', 'XMRUSDT', 'XRPUSDT']
    lPdcnp = np.zeros((len(mdfll), len(Cry_str)))
    r = 0
    for crypto in Cry_str:
        query = f"SELECT close " \
                f"FROM {crypto}d " \
                f"ORDER BY date DESC " \
                f"LIMIT 700 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [item for sublist in [list(i) for i in col] for item in sublist]
        list.reverse(Col)
        lPdcnp[:, r] = Col
        r += 1

    Pd = matlab.double(np.ndarray.tolist(lPdcnp[-(7 * t):, :]))

    lPdcnpv = np.zeros((7, len(Cry_str)))
    r = 0
    for crypto in Cry_str:
        query = f"SELECT volume " \
                f"FROM {crypto}d " \
                f"ORDER BY date DESC " \
                f"LIMIT 7 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [item for sublist in [list(i) for i in col] for item in sublist]
        list.reverse(Col)
        lPdcnpv[:, r] = Col
        r += 1

    query = f"SELECT BNB, IOTA, VET, ADA, LTC " \
            f"FROM cryptos " \
            f"ORDER BY date DESC " \
            f"LIMIT 700 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [list(item) for item in col]
    list.reverse(Col)
    Crypto1 = np.asarray(Col)

    Cry_str = ['XLMUSDT', 'LINKUSDT', 'NEOUSDT']
    Crypto2 = np.zeros((len(mdfll), len(Cry_str)))
    r = 0
    for crypto in Cry_str:
        query = f"SELECT close " \
                f"FROM {crypto}d " \
                f"ORDER BY date DESC " \
                f"LIMIT 700 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [item for sublist in [list(i) for i in col] for item in sublist]
        list.reverse(Col)
        Crypto2[:, r] = Col
        r += 1

    Cryptos = np.hstack((Crypto1, Crypto2))

    query = f"SELECT EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, " \
            f"SPY, EWC, MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT," \
            f" VDE, ERUS, XT, IAU, PICK, ICLN, ITA " \
            f"FROM worldindices " \
            f"ORDER BY date DESC " \
            f"LIMIT 700 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [list(item) for item in col]
    list.reverse(Col)
    Worldind = np.asarray(Col)

    query = f"SELECT TSLA, MSFT, GOOGL, AAPL, IBM, AMZN, FB, HYMTF, VWAGY " \
            f"FROM stocks " \
            f"ORDER BY date DESC " \
            f"LIMIT 700 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [list(item) for item in col]
    list.reverse(Col)
    Stocks = np.asarray(Col)

    Crypto_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo', 'gas', 'usdt', 'doge', 'ada', 'ltc']
    for crypto in Crypto_str:
        query = f"SELECT * " \
                f"FROM {crypto}MD " \
                f"ORDER BY date DESC " \
                f"LIMIT 700 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        list.reverse(Col)
        vars()[f"{crypto}ND"] = np.delete(np.asarray(Col), 0, 1)

    CryptoND = []
    for crypto in Crypto_str:
        if crypto == 'btc':
            CryptoND = vars()[f"{crypto}ND"]
        else:
            CryptoND = np.concatenate((CryptoND, vars()[f"{crypto}ND"]), axis=1)

    query = f"SELECT Bitcoin, BTC, ETH, Ethereum, Monero, Ripple_crypto, Stellar_Lumens, ChainLink, NEO_price, XRP, " \
            f"blockchain, cryptocurrency, altcoin, Smart_Contract, Binance " \
            f"FROM GT_searches " \
            f"ORDER BY date DESC " \
            f"LIMIT 700 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [list(item) for item in col]
    list.reverse(Col)
    GTdata = np.asarray(Col)

    mifll = np.ndarray.tolist(np.concatenate((CryptoND, GTdata, Worldind, Stocks, Cryptos, lPdcnp), axis=1))

    MDIFull = matlab.double([[*x, y] for x, y in zip(mifll, mdfll)])
    Mi = matlab.double(mifll[-(7 * t):])

    ccipred = eng.CCIPredictions(MDIFull, Mi, Md, nargout=1)
    CPP = ccipred*(CCI[-1]/ccipred[0])
    CCIPred = CPP + (CCI[-1]-CPP[0])

    CCI7 = np.round(((CCIPred[8]-CCIPred[0])/CCIPred[0]) * 1000)/10
    CCI15 = np.round(((CCIPred[16]-CCIPred[0])/CCIPred[0]) * 1000)/10
    CCI30 = np.round(((CCIPred[31]-CCIPred[0])/CCIPred[0]) * 1000)/10

    Cry_str = ['btc', 'eth', 'xmr', 'xrp']
    Par = np.zeros((4,13))
    j=0
    for crypto in Cry_str:
        query = f"Select accur, a, b, c, d, e, f, g, h, i, j, k, l " \
                f"FROM {crypto}popt " \
                f"ORDER BY date DESC " \
                f"LIMIT 1"
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Par[j, :] = np.asarray(Col)
        j += 1
    PPar = Par[:,1:]
    PParc = np.round(Par[:,0] * 1000) / 10

    # Plots

    # Adoption and Interest

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("Index of Active Address Count", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, AdrCntInd, linewidth=4)
    plt.savefig("Plots\AdrCntInd.png")
    plt.close()

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("Index of Transactions Count", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, TxCntInd, linewidth=4)
    plt.savefig("Plots\TxCntInd.png")
    plt.close()

    cmpa = (AdrCntInd[-1] - AdrCntInd[-7])/AdrCntInd[-7]
    cmpt = (TxCntInd[-1] - TxCntInd[-7])/TxCntInd[-7]
    cmap = cmpt + cmpa
    if cmap > 0:
        CMAA = "AU"
    elif cmap < 0:
        CMAA = "AD"
    else:
        CMAA = "AS"

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("Index of Search Queries", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, GTInd,linewidth=4)
    plt.savefig("Plots\GTInd.png")
    plt.close()

    cmip = (GTInd[-1]-GTInd[-7])/GTInd[-7]
    if cmip > 0:
        CMIA = "AU"
    elif cmip < 0:
        CMIA = "AD"
    else:
        CMIA = "AS"

    # Market Cap. Dominance

    plt.figure(figsize=(9, 3), dpi=600)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, np.transpose(np.vstack((MainPer, AltPer))),linewidth=4)
    plt.legend(labels=["Top 5 Market Share (Exc. BTC)", "Rest of Market Share"], bbox_to_anchor=(0., 1.02, 1., .102),
               loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig("Plots\MKdom.png")
    plt.close()

    # Crypto Index

    CCIst = np.zeros((len(CCI)-7, 1))
    for i in range(len(CCI)-7):
        CCIst[i] = np.std(CCI[i:i+7])
    CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

    CCIV = np.zeros((len(CCI)-4, 1))
    for i in range(4, len(CCI)):
        CCIV[i-4] = (CCI[i]-CCI[i-4])/4
    CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 6))

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("Crypto Index", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCI[-100:],linewidth=4)
    plt.savefig("Plots\CCI.png")
    plt.close()

    cmpp = (CCI[-1] - CCI[-7]) / CCI[-7]

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("Volatility of Crypto Index", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIstd[-100:],linewidth=4)
    plt.savefig("Plots\CCIstd.png")
    plt.close()

    cmvp = (CCIstd[-1]-CCIstd[-7])/CCIstd[-7]
    if cmvp > 0:
        CMVA = "AU"
    elif cmvp < 0:
        CMVA = "AD"
    else:
        CMVA = "AS"

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("Crypto Index Momentum", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIm[-100:],linewidth=4)
    plt.savefig("Plots\CCIv.png")
    plt.close()

    cmmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

    if np.sign(cmip)<0 and np.sign(cmpp)<0:
        cmgts=-1
    else:
        cmgts=np.sign(cmip) * np.sign(cmpp)

    # Predictions

    Fdate = pd.date_range(Dates[-1][0], Dates[-1][0] + timedelta(days=34))

    plt.figure(figsize=(9, 3), dpi=600)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates[-65:], CCI[-65:],linewidth=4)
    plt.plot(Fdate, CCIPred,linewidth=4)
    plt.legend(labels=["Crypto Index", "Crypto Index Prediction"], bbox_to_anchor=(0., 1.02, 1., .102),
               loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig("Plots\CCIPred.png")
    plt.close()

    if CCI7[0] > 0:
        CMPA = "AU"
    elif CCI7[0] < 0:
        CMPA = "AD"
    else:
        CMPA = "AS"


    ## Cryptocurrencies

    ccpred = eng.CryPredictions(MDIFull, Mi, Pd, nargout=1)

    CCPred = ccpred + (lPdcnp[-1, :]-ccpred[0])
    CCPredS = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCPred)),'gaussian',10))
    CC7S = np.round(((CCPredS[8, :] - CCPredS[0, :]) / CCPredS[0, :]) * 1000) / 10
    CC7 = np.round(((CCPred[8, :]-CCPred[0, :])/CCPred[0, :]) * 1000)/10
    CC15 = np.round(((CCPred[16, :]-CCPred[0, :])/CCPred[0, :]) * 1000)/10
    CC30 = np.round(((CCPred[31, :]-CCPred[0, :])/CCPred[0, :]) * 1000)/10

    # Plots

    # BTC

    # BTC:Network

    btctx=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"btcND"][-100:, 0])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("BTC Transaction Count", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, btctx, linewidth=4)
    plt.savefig("Plots\BTCTxCnt.png")
    plt.close()

    btcad=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"btcND"][-100:, 5])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("BTC Active Addresses", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, btcad, linewidth=4)
    plt.savefig("Plots\BTCActAdd.png")
    plt.close()

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("BTC Med. Transaction Value", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"btcND"][-100:, 2])),
                                              'gaussian',6)).reshape(100,), linewidth=4)
    plt.savefig("Plots\BTCTxVal.png")
    plt.close()

    btcpt = (btctx[-1] - btctx[-7])/btctx[-7]
    btcpa = (btcad[-1] - btcad[-7])/btcad[-7]
    btcap = btcpt + btcpa
    if btcap > 0:
        BTCAA = "AU"
    elif btcap < 0:
        BTCAA = "AD"
    else:
        BTCAA = "AS"

    # BTC: Google Trends

    btcgt=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata[-100:, 0:2], axis=1)/2)),'gaussian',6)).reshape(100,)

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("BTC Search Queries Index", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, btcgt, linewidth=4)
    plt.savefig("Plots\BTCGT.png")
    plt.close()

    btcip = (btcgt[-1]-btcgt[-7])/btcgt[-7]
    if btcip > 0:
        BTCIA = "AU"
    elif btcip < 0:
        BTCIA = "AD"
    else:
        BTCIA = "AS"

    # BTC: Price Analysis

    CCI = lPdcnp[-122:, 0]

    CCIst = np.zeros((len(CCI)-7, 1))
    for i in range(len(CCI)-7):
        CCIst[i] = np.std(CCI[i:i+7])
    CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

    CCIV = np.zeros((len(CCI)-4, 1))
    for i in range(4, len(CCI)):
        CCIV[i-4] = (CCI[i]-CCI[i-4])/4
    CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("BTC Price", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCI[-100:], linewidth=4)
    plt.savefig("Plots\BTC.png")
    plt.close()

    btcpp = (CCI[-1] - CCI[-7]) / CCI[-7]

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("BTC Volatility", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIstd[-100:], linewidth=4)
    plt.savefig("Plots\BTCV.png")
    plt.close()

    btcvp = (CCIstd[-1]-CCIstd[-7])/CCIstd[-7]
    if btcvp > 0:
        BTCVA = "AU"
    elif btcvp < 0:
        BTCVA = "AD"
    else:
        BTCVA = "AS"

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("BTC Momentum", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIm[-100:], linewidth=4)
    plt.savefig("Plots\BTCM.png")
    plt.close()

    btcmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

    # BTC: Predictions

    plt.figure(figsize=(9, 3), dpi=600)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates[-65:], CCI[-65:], linewidth=4)
    plt.plot(Fdate, CCPred[:, 0], linewidth=4)
    plt.legend(labels=["BTC Price", "BTC Price Prediction"], bbox_to_anchor=(0., 1.02, 1., .102),
               loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig("Plots\BTCPred.png")
    plt.close()

    btcvl=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 0])), 'gaussian', 10)).reshape(7,)
    btcvlp=(btcvl[-1] - btcvl[-7]) / btcvl[-7]

    if np.sign(btcvlp)<0 and np.sign(btcpp)<0:
        vol=-1
    else:
        vol=np.sign(btcvlp)*np.sign(btcpp)

    if CC7[0] > 0:
        BTCPA = "AU"
    elif CC7[0] < 0:
        BTCPA = "AD"
    else:
        BTCPA = "AS"

    if np.sign(btcip)<0 and np.sign(btcpp)<0:
        gts=-1
    else:
        gts=np.sign(btcip)*np.sign(btcpp)

    btcbs = PPar[0,0]*np.sign(btcap) + PPar[0,1]*gts + PPar[0,2]*np.sign(btcpp) + PPar[0,3]*np.sign(btcvp)*np.sign(btcpp) + \
            PPar[0,4]*np.sign(btcmp) + PPar[0,5]*np.sign(cmmp) + PPar[0,6]*vol + PPar[0,7]*np.sign(CC7S[0]) + \
            PPar[0,8]*np.sign(CCI7[0]) + PPar[0,9]*np.sign(cmap) + PPar[0,10]*cmgts + \
            PPar[0,11]*np.sign(cmvp)*np.sign(cmpp)


    if btcbs > 0:
        BTCB = "Buy"
    else:
        BTCB = "Sell"

    # ETH

    # ETH: Network

    ethtx=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"ethND"][-100:, 0])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("ETH Transaction Count", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, ethtx, linewidth=4)
    plt.savefig("Plots\ETHTxCnt.png")
    plt.close()

    ethad=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"ethND"][-100:, 5])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("ETH Active Addresses", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, ethad, linewidth=4)
    plt.savefig("Plots\ETHActAdd.png")
    plt.close()

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("ETH Med. Transaction Value", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"ethND"][-100:, 2])),'gaussian',6)).reshape(100,), linewidth=4)
    plt.savefig("Plots\ETHTxVal.png")
    plt.close()

    ethpt = (ethtx[-1] - ethtx[-7])/ethtx[-7]
    ethpa = (ethad[-1] - ethad[-7])/ethad[-7]
    ethap = ethpt + ethpa
    if ethap > 0:
        ETHAA = "AU"
    elif ethap < 0:
        ETHAA = "AD"
    else:
        ETHAA = "AS"

    # ETH: Google Trends

    ethgt = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata[-100:, [2, 3, 13]], axis=1)/3)),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("ETH Search Queries Index", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, ethgt, linewidth=4)
    plt.savefig("Plots\ETHGT.png")
    plt.close()

    ethip = (ethgt[-1]-ethgt[-7])/ethgt[-7]
    if ethip > 0:
        ETHIA = "AU"
    elif ethip < 0:
        ETHIA = "AD"
    else:
        ETHIA = "AS"

    # ETH: Price Analysis

    CCI = lPdcnp[-122:, 1]

    CCIst = np.zeros((len(CCI)-7, 1))
    for i in range(len(CCI)-7):
        CCIst[i] = np.std(CCI[i:i+7])
    CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

    CCIV = np.zeros((len(CCI)-4, 1))
    for i in range(4, len(CCI)):
        CCIV[i-4] = (CCI[i]-CCI[i-4])/4
    CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("ETH Price", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCI[-100:], linewidth=4)
    plt.savefig("Plots\ETH.png")
    plt.close()

    ethpp = (CCI[-1] - CCI[-7]) / CCI[-7]

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("ETH Volatility", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIstd[-100:], linewidth=4)
    plt.savefig("Plots\ETHV.png")
    plt.close()

    ethvp = (CCIstd[-1]-CCIstd[-7])/CCIstd[-7]
    if ethvp > 0:
        ETHVA = "AU"
    elif ethvp < 0:
        ETHVA = "AD"
    else:
        ETHVA = "AS"

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("ETH Momentum", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIm[-100:], linewidth=4)
    plt.savefig("Plots\ETHM.png")
    plt.close()

    ethmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

    # ETH: Predictions

    plt.figure(figsize=(9, 3), dpi=600)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates[-65:], CCI[-65:], linewidth=4)
    plt.plot(Fdate, CCPred[:, 1], linewidth=4)
    plt.legend(labels=["ETH Price", "ETH Price Prediction"], bbox_to_anchor=(0., 1.02, 1., .102),
               loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig("Plots\ETHPred.png")
    plt.close()

    ethvl=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 1])), 'gaussian', 10)).reshape(7,)
    ethvlp=(ethvl[-1] - ethvl[-7]) / ethvl[-7]

    if np.sign(ethvlp)<0 and np.sign(ethpp)<0:
        vol=-1
    else:
        vol=np.sign(ethvlp)*np.sign(ethpp)

    if CC7[1] > 0:
        ETHPA = "AU"
    elif CC7[1] < 0:
        ETHPA = "AD"
    else:
        ETHPA = "AS"

    if np.sign(ethip)<0 and np.sign(ethpp)<0:
        gts=-1
    else:
        gts=np.sign(ethip)*np.sign(ethpp)

    ethbs = PPar[1,0]*np.sign(ethap) + PPar[1,1]*gts + PPar[1,2]*np.sign(ethpp) + PPar[1,3]*np.sign(ethvp)*np.sign(ethpp) + \
            PPar[1,4]*np.sign(ethmp) + PPar[1,5]*np.sign(cmmp) + PPar[1,6]*vol + PPar[1,7]*np.sign(CC7S[1]) + \
            PPar[1,8]*np.sign(CCI7[0]) + PPar[1,9]*np.sign(cmap) + PPar[1,10]*cmgts + \
            PPar[1,11]*np.sign(cmvp)*np.sign(cmpp)

    if ethbs > 0:
        ETHB = "Buy"
    else:
        ETHB = "Sell"

    # XMR

    # XMR: Network

    xmrtx=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"xmrND"][-100:, 0])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XMR Transaction Count", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, xmrtx, linewidth=4)
    plt.savefig("Plots\XMRTxCnt.png")
    plt.close()

    xmrap = (xmrtx[-1] - xmrtx[-7])/xmrtx[-7]
    if xmrap > 0:
        XMRAA = "AU"
    elif xmrap < 0:
        XMRAA = "AD"
    else:
        XMRAA = "AS"

    # XMR: Google Trends

    xmrgt = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(GTdata[-100:, 4])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XMR Search Queries Index", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, xmrgt, linewidth=4)
    plt.savefig("Plots\XMRGT.png")
    plt.close()

    xmrip = (xmrgt[-1]-xmrgt[-7])/xmrgt[-7]
    if xmrip > 0:
        XMRIA = "AU"
    elif xmrip < 0:
        XMRIA = "AD"
    else:
        XMRIA = "AS"

    # XMR: Price Analysis

    CCI = lPdcnp[-122:, 2]

    CCIst = np.zeros((len(CCI)-7, 1))
    for i in range(len(CCI)-7):
        CCIst[i] = np.std(CCI[i:i+7])
    CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

    CCIV = np.zeros((len(CCI)-4, 1))
    for i in range(4, len(CCI)):
        CCIV[i-4] = (CCI[i]-CCI[i-4])/4
    CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XMR Price", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCI[-100:], linewidth=4)
    plt.savefig("Plots\XMR.png")
    plt.close()

    xmrpp = (CCI[-1] - CCI[-7]) / CCI[-7]

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XMR Volatility", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIstd[-100:], linewidth=4)
    plt.savefig("Plots\XMRV.png")
    plt.close()

    xmrvp = (CCIstd[-1]-CCIstd[-7])/CCIstd[-7]
    if xmrvp > 0:
        XMRVA = "AU"
    elif xmrvp < 0:
        XMRVA = "AD"
    else:
        XMRVA = "AS"

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XMR Momentum", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIm[-100:], linewidth=4)
    plt.savefig("Plots\XMRM.png")
    plt.close()

    xmrmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

    # XMR: Predictions

    plt.figure(figsize=(9, 3), dpi=600)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates[-65:], CCI[-65:], linewidth=4)
    plt.plot(Fdate, CCPred[:, 2], linewidth=4)
    plt.legend(labels=["XMR Price", "XMR Price Prediction"], bbox_to_anchor=(0., 1.02, 1., .102),
               loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig("Plots\XMRPred.png")
    plt.close()

    xmrvl=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 2])), 'gaussian', 10)).reshape(7,)
    xmrvlp=(xmrvl[-1] - xmrvl[-7]) / xmrvl[-7]

    if np.sign(xmrvlp)<0 and np.sign(xmrpp)<0:
        vol=-1
    else:
        vol=np.sign(xmrvlp)*np.sign(xmrpp)

    if CC7[2] > 0:
        XMRPA = "AU"
    elif CC7[2] < 0:
        XMRPA = "AD"
    else:
        XMRPA = "AS"

    if np.sign(xmrip)<0 and np.sign(xmrpp)<0:
        gts=-1
    else:
        gts=np.sign(xmrip)*np.sign(xmrpp)

    xmrbs = PPar[2,0]*np.sign(xmrap) + PPar[2,1]*gts + PPar[2,2]*np.sign(xmrpp) + PPar[2,3]*np.sign(xmrvp)*np.sign(xmrpp) + \
            PPar[2,4]*np.sign(xmrmp) + PPar[2,5]*np.sign(cmmp) + PPar[2,6]*vol + PPar[2,7]*np.sign(CC7S[2]) + \
            PPar[2,8]*np.sign(CCI7[0]) + PPar[2,9]*np.sign(cmap) + PPar[2,10]*cmgts + \
            PPar[2,11]*np.sign(cmvp)*np.sign(cmpp)

    if xmrbs > 0:
        XMRB = "Buy"
    else:
        XMRB = "Sell"

    # XRP

    # XRP: Network

    xrptx=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"xrpND"][-100:, 0])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XRP Transaction Count", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, xrptx, linewidth=4)
    plt.savefig("Plots\XRPTxCnt.png")
    plt.close()

    xrpad=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"xrpND"][-100:, 1])),'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XRP Active Addresses", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, xrpad, linewidth=4)
    plt.savefig("Plots\XRPActAdd.png")
    plt.close()

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XRP Med. Transaction Value", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"xrpND"][-100:, 2])),
                                              'gaussian',6)).reshape(100,), linewidth=4)
    plt.savefig("Plots\XRPTxVal.png")
    plt.close()

    xrppt = (xrptx[-1] - xrptx[-7])/xrptx[-7]
    xrppa = (xrpad[-1] - xrpad[-7])/xrpad[-7]
    xrpap = xrppt + xrppa
    if xrpap > 0:
        XRPAA = "AU"
    elif xrpap < 0:
        XRPAA = "AD"
    else:
        XRPAA = "AS"

    # XRP: Google Trends

    xrpgt = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata[-100:, [5, 9]], axis=1)/2)),
                                      'gaussian',6)).reshape(100,)
    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XRP Search Queries Index", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, xrpgt, linewidth=4)
    plt.savefig("Plots\XRPGT.png")
    plt.close()

    xrpip = (xrpgt[-1]-xrpgt[-7])/xrpgt[-7]
    if xrpip > 0:
        XRPIA = "AU"
    elif xrpip < 0:
        XRPIA = "AD"
    else:
        XRPIA = "AS"

    # XRP: Price Analysis

    CCI = lPdcnp[-122:, 3]

    CCIst = np.zeros((len(CCI)-7, 1))
    for i in range(len(CCI)-7):
        CCIst[i] = np.std(CCI[i:i+7])
    CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

    CCIV = np.zeros((len(CCI)-4, 1))
    for i in range(4, len(CCI)):
        CCIV[i-4] = (CCI[i]-CCI[i-4])/4
    CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XRP Price", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCI[-100:], linewidth=4)
    plt.savefig("Plots\XRP.png")
    plt.close()

    xrppp = (CCI[-1] - CCI[-7]) / CCI[-7]

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XRP Volatility", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIstd[-100:], linewidth=4)
    plt.savefig("Plots\XRPV.png")
    plt.close()

    xrpvp = (CCIstd[-1]-CCIstd[-7])/CCIstd[-7]
    if xrpvp > 0:
        XRPVA = "AU"
    elif xrpvp < 0:
        XRPVA = "AD"
    else:
        XRPVA = "AS"

    plt.figure(figsize=(9, 3), dpi=600)
    plt.title("XRP Momentum", fontsize=8)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates, CCIm[-100:], linewidth=4)
    plt.savefig("Plots\XRPM.png")
    plt.close()

    xrpmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

    # XRP: Predictions

    plt.figure(figsize=(9, 3), dpi=600)
    plt.xticks(rotation=9, fontsize=8)
    plt.yticks(fontsize=6)
    plt.plot(Dates[-65:], CCI[-65:], linewidth=4)
    plt.plot(Fdate, CCPred[:, 3], linewidth=4)
    plt.legend(labels=["XRP Price", "XRP Price Prediction"], bbox_to_anchor=(0., 1.02, 1., .102),
               loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig("Plots\XRPPred.png")
    plt.close()

    xrpvl=np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 3])), 'gaussian', 10)).reshape(7,)
    xrpvlp=(xrpvl[-1] - xrpvl[-7]) / xrpvl[-7]

    if np.sign(xrpvlp)<0 and np.sign(xrppp)<0:
        vol=-1
    else:
        vol=np.sign(xrpvlp)*np.sign(xrppp)

    if CC7[3] > 0:
        XRPPA = "AU"
    elif CC7[3] < 0:
        XRPPA = "AD"
    else:
        XRPPA = "AS"

    if np.sign(xrpip)<0 and np.sign(xrppp)<0:
        gts=-1
    else:
        gts=np.sign(xrpip)*np.sign(xrppp)

    xrpbs = PPar[3,0]*np.sign(xrpap) + PPar[3,1]*gts + PPar[3,2]*np.sign(xrppp) + PPar[3,3]*np.sign(xrpvp)*np.sign(xrppp) + \
            PPar[3,4]*np.sign(xrpmp) + PPar[3,5]*np.sign(cmmp) + PPar[3,6]*vol + PPar[3,7]*np.sign(CC7S[3]) + \
            PPar[3,8]*np.sign(CCI7[0]) + PPar[3,9]*np.sign(cmap) + PPar[3,10]*cmgts + \
            PPar[3,11]*np.sign(cmvp)*np.sign(cmpp)

    if xrpbs > 0:
        XRPB = "Buy"
    else:
        XRPB = "Sell"


    # Report

    class PDF(FPDF):
        # page footer
        def footer(self):
            if 1 < self.page_no() < 23:
                # set position of the footer
                self.set_y(-15)
                # set font
                self.set_font('helvetica', 'I', 10)
                # page number
                pdf.set_text_color(45, 45, 45)
                self.cell(0, 10, f"HC.dept Weekly Market Report - {Tdate}", align='L')
                pdf.set_text_color(57, 95, 96)
                self.cell(0, 10, f'{self.page_no() - 1}/{{nb}}', align='R')
                self.set_line_width(0.1)
                self.set_draw_color(r=95, g=158, b=160)
                self.line(x1=11, y1=282.5, x2=195, y2=282.5)
            elif self.page_no() == 1:
                # Cover footer
                # set position of the footer
                self.set_y(-15)
                # set font
                self.set_font('helvetica', 'I', 10)
                # page number
                pdf.set_text_color(45, 45, 45)
                self.cell(0, 10, f"HC.dept Weekly Market Report - {date.today()}", align='L')

        # create FPDF object
        # Layout ('P', 'L')
        # Unit ('mm', 'cm', 'in')
        # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))

    pdf = PDF('P', 'mm', 'A4')

    pdf.alias_nb_pages()  # get total page numbers
    pdf.set_auto_page_break(auto=True, margin=10)  # Set auto page break


    # Cover page
    pdf.add_page()
    pdf.image('Images\BriBGB.png', 0, 0, 210, 300)


    pdf.add_page()

    # 1st Page
    # Header Background
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 15)
    # Title
    pdf.cell(0, 40, 'HC.depi Weekly Report', 0, 1, 'L')
    # Logo
    pdf.image('Images\BriC.png', 11, 20, 20)  # (x,y, w,h) (position, image proportions)
    # Line break
    pdf.ln(10)


    # specify font
    # fonts ( 'times', 'courier', 'helvetica', 'symbol', 'zpdfingbats')
    # 'B' (Bold), 'U' (underline), 'I' (italic), '' (regular), combination (i.e. ('BU'))
    pdf.set_font('helvetica', '', 18)  # (font, type, size)

    # Add text (cell or multicell (single or multiple line text)
    # w= width
    # h = hight
    # text = text to print
    # ln= 0/1 (True/False), go to next line if 1
    # border = 0/1 (True/False), print cell boarder
    # fill=1/0, fill cell with color
    # e.g.: pdf.cell(0, 10, 'hello world!', ln=True, border=True)  # (w, h, text, next line, cell boarder)
    #  if w=0 then width is equal to width of pdf

    # Summary
    # Title
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Summary', ln=True)
    pdf.ln(10)

    # Table

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    data = [["", "BTC", "ETH", "XMR", "XRP", "Crypto Market"],
            [r"Adoption\Use", "", "", "", "", ""],
            ["Interest", "", "", "", "", ""],
            ["Volatility", "", "", "", "", ""],
            ["7d Prediction", "", "", "", "", ""],
            ["Buy/Sell", f"{BTCB}", f"{ETHB}", f"{XMRB}", f"{XRPB}"]]


    col_width = 32
    th = pdf.font_size
    i = 0
    for row in data:
        for datum in row:
            if i==0:
                pdf.cell(col_width, 4 * th, "")
            else:
                if datum=="" or datum=="Buy" or datum=="Sell":
                    pdf.set_fill_color(240, 248, 255)
                else:
                    pdf.set_fill_color(230, 230, 250)
                pdf.cell(col_width, 4 * th, str(datum), border=True, fill=True, align="C")
            i += 1
        pdf.ln(4 * th)

    # Arrows
    # BTC
    pdf.image(f'Images\{BTCAA}.png', 53, 100, 10, 10)
    pdf.image(f'Images\{BTCIA}.png', 53, 100 + 4*th, 10, 10)
    pdf.image(f'Images\{BTCVA}.png', 53, 100 + 8*th, 10, 10)
    pdf.image(f'Images\{BTCPA}.png', 53, 100 + 12*th, 10, 10)
    # ETH
    pdf.image(f'Images\{ETHAA}.png', 85, 100, 10, 10)
    pdf.image(f'Images\{ETHIA}.png', 85, 100 + 4*th, 10, 10)
    pdf.image(f'Images\{ETHVA}.png', 85, 100 + 8*th, 10, 10)
    pdf.image(f'Images\{ETHPA}.png', 85, 100 + 12*th, 10, 10)
    # XMR
    pdf.image(f'Images\{XMRAA}.png', 117, 100, 10, 10)
    pdf.image(f'Images\{XMRIA}.png', 117, 100 + 4*th, 10, 10)
    pdf.image(f'Images\{XMRVA}.png', 117, 100 + 8*th, 10, 10)
    pdf.image(f'Images\{XMRPA}.png', 117, 100 + 12*th, 10, 10)
    # XRP
    pdf.image(f'Images\{XRPAA}.png', 149, 100, 10, 10)
    pdf.image(f'Images\{XRPIA}.png', 149, 100 + 4*th, 10, 10)
    pdf.image(f'Images\{XRPVA}.png', 149, 100 + 8*th, 10, 10)
    pdf.image(f'Images\{XRPPA}.png', 149, 100 + 12*th, 10, 10)
    # Market
    pdf.image(f'Images\{CMAA}.png', 181, 100, 10, 10)
    pdf.image(f'Images\{CMIA}.png', 181, 100 + 4*th, 10, 10)
    pdf.image(f'Images\{CMVA}.png', 181, 100 + 8*th, 10, 10)
    pdf.image(f'Images\{CMPA}.png', 181, 100 + 12*th, 10, 10)


    pdf.set_y(-20)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(57, 95, 96)
    pdf.multi_cell(0, 5, txt=f"Buy/Sell signals accuracy: BTC {PParc[0]}%, ETH {PParc[1]}%, XMR {PParc[2]}%, "
                             f"XRP {PParc[3]}%,.", ln=1)

    pdf.add_page()

    # Global Market Conditions
    # Adoption

    # Chapter Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'Global Market Conditions: Adoption', 0, 1, 'L')
    pdf.ln(15)

    # Text
    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="The state of adoption and use of a cryptocurrency "
                            "can be tracked by monitoring the number of active addresses and executed transaction in a "
                            "time period, active addresses being those in a network that were either a recipient or "
                            "originator of a ledger change (e.g transaction). In order to track this metrics across the "
                            "whole cryptocurrency ecosystem we present them as an index composed of respective data "
                            "from several different cryptocurrencies.", ln=1)
    pdf.ln(7)

    pdf.image("Plots\AdrCntInd.png", -4, 95, 210, 70)
    pdf.image("Plots\TxCntInd.png", -4, 175, 210, 70)

    pdf.add_page()
    pdf.ln(15)

    pdf.multi_cell(w=0, h=5, txt="Another great metric to track interest in the crypto space is the count of search queries"
                            " related to cryptocurrencies on Google, as such, and in the spirit of the previous chart, we "
                            "have below an index composed of Google Trends data of a basket of search terms.", ln=1)

    pdf.image("Plots\GTInd.png", -4, 45, 210, 70)

    pdf.ln(95)
    pdf.multi_cell(w=0, h=5, txt="As prices of cryptocurrencies fluctuate and the overall market changes regime"
                                 " this information can be valuable for confirming market growth as organic or speculative.")

    pdf.add_page()


    # Market Cap. Dominance

    # Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'Market Psychology', 0, 1, 'L')
    pdf.ln(15)

    # Text
    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="To better observe the behaviour of investors in the market and gain insight into present "
                            "and future trends it is valuable to partition the market into classes and track changes "
                            "amongst them. As such, in order to understand if investors are prioritizing gains over risk "
                            "and behaving in a greedy or fearful manner we'll analyse market cap changes between the top "
                            "5 cryptocurrencies and the rest of the market. The following chart shows the market share "
                            "of the top 5 cryptos (by market cap) as a percentage of the overall crypto market cap along "
                            "with the same chart but for the total market excluding the top 5 cryptos. This chart will "
                            "show if investor are giving preference to well established projects in the market or to "
                            "emergent ones. We'll exclude Bitcoin from the top 5 cryptos for due to it's high market cap "
                            "it skews the data and hides the insight we're looking for, this is not a problem, due to the "
                            "high correlation the top cryptocurrencies have with BTC the data will still account for the "
                            "weight of BTC in changes to the top 5 cryptos total market cap.", ln=1)

    pdf.image("Plots\MKdom.png", -4, 128, 210, 70)

    pdf.add_page()


    # Crypto Index

    # Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'Cryptocurrency Index', 0, 1, 'L')
    pdf.ln(15)

    # Text
    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="As an index for the overall cryptocurrency market we'll compute a Laspeyres index "
                                 "composed of the top 30 cryptos (by market cap). Market volatility is presented below, "
                                 "smoothed to evidence current trends. Additionally we present a market momentum metric, "
                                 "this is simply the first discrete derivative of the Crypto Index, also smoothed, to track "
                                 "if the market is accelerating upwards or downwards .", ln=1)

    pdf.image("Plots\CCI.png", -4, 88, 210, 70)
    pdf.image("Plots\CCIstd.png", -4, 150, 210, 70)
    pdf.image("Plots\CCIv.png", -4, 212, 210, 70)

    pdf.add_page()


    # CCI Predictions

    # Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'Crypto Index Prediction', 0, 1, 'L')
    pdf.ln(15)

    # Text

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="To conclude our analysis of the Global Crypto Market we have below a prediction "
                                 "of the Crypto Index for the following 35 days.", ln=1)

    pdf.image("Plots\CCIPred.png", -4, 82, 210, 70)
    pdf.ln(87)

    pdf.multi_cell(w=0, h=5, txt="Additionally we present a table summarizing the predictions above.", ln=1)
    pdf.ln(10)

    data = [["", "%"],
           ["7 days", CCI7[0]],
           ["15 days", CCI15[0]],
           ["30 days", CCI30[0]]]

    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    i = 0
    for row in data:
        for datum in row:
            if i==0:
                pdf.cell(col_width, 2 * th, "")
            else:
                if datum=="7 days":
                    pdf.set_fill_color(152,251,152)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="15 days":
                    pdf.set_fill_color(255,255,153)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="30 days":
                    pdf.set_fill_color(240,128,128)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="%":
                    pdf.set_fill_color(230, 230, 250)
                    pdf.set_text_color(40, 66, 67)
                else:
                    pdf.set_fill_color(240, 248, 255)
                    pdf.set_text_color(40, 66, 67)
                pdf.cell(col_width, 2 * th, str(datum), border=1, fill=1)
            i += 1
        pdf.ln(2 * th)


    # Cryptocurrencies:

    pdf.add_page()

    # BTC

    # Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'Cryptocurrencies: BTC', 0, 1, 'L')
    pdf.ln(15)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="The following sections will provide an analysis on BTC, ETH, XMR, XRP. We'll start "
                                 "by tracking adoption, use and public interest, then move to price analysis and "
                                 "finish with a price prediction of the next 35 days.", ln=1)

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Network', ln=True)
    pdf.ln(7)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="To measure adoption we'll again use the count of Active Addresses and "
                                 "Transaction used previously, additionally we'll track the median transacted value "
                                 "(when available), in the native currency, to see if the average transaction value is "
                                 "rising or declining.", ln=1)

    pdf.image("Plots\BTCTxCnt.png", -4, 130, 210, 70)
    pdf.image("Plots\BTCActAdd.png", -4, 200, 210, 70)

    pdf.add_page()

    pdf.image("Plots\BTCTxVal.png", -4, 25, 210, 70)
    pdf.ln(95)

    # BTC: Public Interest

    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Public Interest', ln=True)
    pdf.ln(7)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="As a measure of public interest we'll resort to Google search queries of terms "
                                 "related to BTC.", ln=1)

    pdf.image("Plots\BTCGT.png", -4, 135, 210, 70)

    pdf.add_page()

    # BTC: Price Analysis

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price', ln=True)
    pdf.ln(7)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="Below we have BTC's price, it's volatility and momentum.", ln=1)

    pdf.image("Plots\BTC.png", -4, 55, 210, 70)
    pdf.image("Plots\BTCV.png", -4, 117, 210, 70)
    pdf.image("Plots\BTCM.png", -4, 177, 210, 70)


    pdf.add_page()

    # BTC: Price Prediction

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price Prediction', ln=True)
    pdf.ln(7)

    pdf.image("Plots\BTCPred.png", -4, 45, 210, 70)
    pdf.ln(85)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="The following table summarizes the predictions above.", ln=1)
    pdf.ln(10)

    data = [["", "%"],
            ["7 days", CC7[0]],
            ["15 days", CC15[0]],
            ["30 days", CC30[0]]]

    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    i = 0
    for row in data:
        for datum in row:
            if i==0:
                pdf.cell(col_width, 2 * th, "")
            else:
                if datum=="7 days":
                    pdf.set_fill_color(152,251,152)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="15 days":
                    pdf.set_fill_color(255,255,153)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="30 days":
                    pdf.set_fill_color(240,128,128)
                    pdf.set_text_color(20, 20, 20)
                elif datum == "%":
                    pdf.set_fill_color(230, 230, 250)
                    pdf.set_text_color(40, 66, 67)
                else:
                    pdf.set_fill_color(240, 248, 255)
                    pdf.set_text_color(40, 66, 67)
                pdf.cell(col_width, 2 * th, str(datum), border=1, fill=1)
            i += 1
        pdf.ln(2 * th)


    pdf.add_page()

    # ETH

    # Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'ETH', 0, 1, 'L')
    pdf.ln(15)

    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Network', ln=True)
    pdf.ln(7)

    pdf.image("Plots\ETHTxCnt.png", -4, 80, 210, 70)
    pdf.image("Plots\ETHActAdd.png", -4, 160, 210, 70)

    pdf.add_page()

    pdf.image("Plots\ETHTxVal.png", -4, 25, 210, 70)
    pdf.ln(100)

    # ETH: Public Interest

    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Public Interest', ln=True)
    pdf.ln(7)

    pdf.image("Plots\ETHGT.png", -4, 130, 210, 70)

    pdf.add_page()

    # ETH: Price Analysis

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price', ln=True)
    pdf.ln(7)

    pdf.image("Plots\ETH.png", -4, 40, 210, 70)
    pdf.image("Plots\ETHV.png", -4, 102, 210, 70)
    pdf.image("Plots\ETHM.png", -4, 164, 210, 70)


    pdf.add_page()

    # ETH: Price Prediction

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price Prediction', ln=True)
    pdf.ln(7)

    pdf.image("Plots\ETHPred.png", -4, 45, 210, 70)
    pdf.ln(90)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)

    data = [["", "%"],
            ["7 days", CC7[1]],
            ["15 days", CC15[1]],
            ["30 days", CC30[1]]]

    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    i = 0
    for row in data:
        for datum in row:
            if i==0:
                pdf.cell(col_width, 2 * th, "")
            else:
                if datum=="7 days":
                    pdf.set_fill_color(152,251,152)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="15 days":
                    pdf.set_fill_color(255,255,153)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="30 days":
                    pdf.set_fill_color(240,128,128)
                    pdf.set_text_color(20, 20, 20)
                elif datum == "%":
                    pdf.set_fill_color(230, 230, 250)
                    pdf.set_text_color(40, 66, 67)
                else:
                    pdf.set_fill_color(240, 248, 255)
                    pdf.set_text_color(40, 66, 67)
                pdf.cell(col_width, 2 * th, str(datum), border=1, fill=1)
            i += 1
        pdf.ln(2 * th)

    pdf.add_page()

    # XMR

    # Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'XMR', 0, 1, 'L')
    pdf.ln(15)

    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Network', ln=True)
    pdf.ln(7)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w=0, h=5, txt="Due to the nature of the XMR Network some data is not available.", ln=1)
    pdf.ln(90)

    pdf.image("Plots\XMRTxCnt.png", -4, 95, 210, 70)

    # XMR: Public Interest

    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Public Interest', ln=True)
    pdf.ln(7)

    pdf.image("Plots\XMRGT.png", -4, 190, 210, 70)

    pdf.add_page()

    # XMR: Price Analysis

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price', ln=True)
    pdf.ln(7)

    pdf.image("Plots\XMR.png", -4, 40, 210, 70)
    pdf.image("Plots\XMRV.png", -4, 102, 210, 70)
    pdf.image("Plots\XMRM.png", -4, 164, 210, 70)


    pdf.add_page()

    # XMR: Price Prediction

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price Prediction', ln=True)
    pdf.ln(7)

    pdf.image("Plots\XMRPred.png", -4, 45, 210, 70)
    pdf.ln(90)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)

    data = [["", "%"],
            ["7 days", CC7[2]],
            ["15 days", CC15[2]],
            ["30 days", CC30[2]]]

    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    i = 0
    for row in data:
        for datum in row:
            if i==0:
                pdf.cell(col_width, 2 * th, "")
            else:
                if datum=="7 days":
                    pdf.set_fill_color(152,251,152)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="15 days":
                    pdf.set_fill_color(255,255,153)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="30 days":
                    pdf.set_fill_color(240,128,128)
                    pdf.set_text_color(20, 20, 20)
                elif datum == "%":
                    pdf.set_fill_color(230, 230, 250)
                    pdf.set_text_color(40, 66, 67)
                else:
                    pdf.set_fill_color(240, 248, 255)
                    pdf.set_text_color(40, 66, 67)
                pdf.cell(col_width, 2 * th, str(datum), border=1, fill=1)
            i += 1
        pdf.ln(2 * th)

    pdf.add_page()

    # XRP

    # Header
    pdf.image('Images\HeaderB.png', 0, 0, 220, 50)  # (x,y, w,h) (position, image proportions)
    pdf.set_font('helvetica', 'B', 25)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 40, 'XRP', 0, 1, 'L')
    pdf.ln(15)

    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Network', ln=True)
    pdf.ln(7)

    pdf.image("Plots\XRPTxCnt.png", -4, 80, 210, 70)
    pdf.image("Plots\XRPActAdd.png", -4, 160, 210, 70)

    pdf.add_page()

    pdf.image("Plots\XRPTxVal.png", -4, 25, 210, 70)
    pdf.ln(100)

    # XRP: Public Interest

    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Public Interest', ln=True)
    pdf.ln(7)

    pdf.image("Plots\XRPGT.png", -4, 130, 210, 70)

    pdf.add_page()

    # XRP: Price Analysis

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price', ln=True)
    pdf.ln(7)

    pdf.image("Plots\XRP.png", -4, 40, 210, 70)
    pdf.image("Plots\XRPV.png", -4, 102, 210, 70)
    pdf.image("Plots\XRPM.png", -4, 164, 210, 70)


    pdf.add_page()

    # XRP: Price Prediction

    pdf.ln(15)
    pdf.set_font('helvetica', '', 18)
    pdf.set_text_color(56, 104, 144)
    pdf.cell(0, 10, 'Price Prediction', ln=True)
    pdf.ln(7)

    pdf.image("Plots\XRPPred.png", -4, 45, 210, 70)
    pdf.ln(90)

    pdf.set_text_color(40, 66, 67)
    pdf.set_font('helvetica', '', 12)

    data = [["", "%"],
            ["7 days", CC7[3]],
            ["15 days", CC15[3]],
            ["30 days", CC30[3]]]

    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    i = 0
    for row in data:
        for datum in row:
            if i==0:
                pdf.cell(col_width, 2 * th, "")
            else:
                if datum=="7 days":
                    pdf.set_fill_color(152,251,152)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="15 days":
                    pdf.set_fill_color(255,255,153)
                    pdf.set_text_color(20, 20, 20)
                elif datum=="30 days":
                    pdf.set_fill_color(240,128,128)
                    pdf.set_text_color(20, 20, 20)
                elif datum == "%":
                    pdf.set_fill_color(230, 230, 250)
                    pdf.set_text_color(40, 66, 67)
                else:
                    pdf.set_fill_color(240, 248, 255)
                    pdf.set_text_color(40, 66, 67)
                pdf.cell(col_width, 2 * th, str(datum), border=1, fill=1)
            i += 1
        pdf.ln(2 * th)

    pdf.set_y(-30)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(57, 95, 96)
    pdf.multi_cell(0, 5, txt="This report is for information purposes only. It is not intended "
                             "to be investment advice. Seek a duly licensed professional for investment advice.", ln=1)

    pdf.add_page()
    pdf.image('Images\BriBGbl.png', -5, 0, 215, 300)

    pdf.output(name=fr'C:\Users\HC.deptR&D\Desktop\Reports\HCdept_Weekly_Report_{Tdate}.pdf')
    print('Report Generated.')


    # Email to Subscrivers

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import stripe as st

    # Retrieve emails of subscrivers to the report on Stripe (stripe.com) (Payed subsrivers service)
    st.api_key = ""
    Custms = st.Customer.list(limit=10000000)
    submails=[]
    snames=[]
    for i in range(len(Custms)):
        submails += [Custms["data"][i]["email"]]
        snames += [Custms["data"][i]["name"]]

    # emails of friend who get it for free
    fiendmails = []
    fiendnames = []

    # Send emails with Report
    mails = submails + fiendmails
    names = snames + fiendnames
    i = 0
    for mail in mails:
        body = f"Hello {names[i]}!\n" \
               f"\n" \
               f"Here's your latest weekly report. Enjoy and be objective.\n" \
               f"\n" \
               f"Best regards;\n" \
               f"HC.dept"

        # sender email and password of email (gmail)
        sender = ""
        password = ''

        receiver = mail

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = mail
        message['Subject'] = f"HC.dept Weekly Report {Tdate}"

        message.attach(MIMEText(body, 'plain'))

        pdfloc = fr'C:\Users\HC.deptR&D\Desktop\Reports\HCdept_Weekly_Report_{Tdate}.pdf'

        binary_pdf = open(pdfloc, 'rb')

        payload = MIMEBase('application', 'octate-stream', Name=f"HCdept_Weekly_Report_{Tdate}.pdf")
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=f"HCdept_Weekly_Report_{Tdate}.pdf")
        message.attach(payload)


        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender, password)

        text = message.as_string()
        session.sendmail(sender, mail, text)
        session.quit()
        i+=1
    print('Emails Sent.')