import tweepy
from pycoingecko import CoinGeckoAPI
from binance.client import Client
import numpy as np
import matplotlib.pyplot as plt
import matlab.engine
import mysql.connector
import random
import time

# Authenticate to Twitter
auth = tweepy.OAuthHandler("")
auth.set_access_token("")

api = tweepy.API(auth)

def smoothdat(X, n):
    p = int(np.round(n / 2))
    l = int(len(X) - p)
    SM = np.zeros(len(X))
    for i in range(p, len(X)):
        if i <= l:
            SM[i] = np.sum(X[i - p:i + p]) / n
        else:
            SM[i] = np.sum(X[i - p:len(X)]) / (p + len(X) - i)
    return (SM)


def TwitterBot(Ndate):
    # same data base as Briareos Algo Trading System
    Database = mysql.connector.connect(
        host="",
        user="",
        passwd="")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    if Ndate.hour == 9 and Ndate.weekday()==2:

        eng = matlab.engine.start_matlab()
        eng.cd(r'C:\Users\HC.deptR&D\Desktop\Report Generator and Twitter\Matlab Funcs', nargout=0)
        eng.ls(nargout=0)

        t = 35

        cg = CoinGeckoAPI()

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

        AdrCntInd = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(Cry_AdrCnt / np.mean(Cry_AdrCnt, axis=0),
                                                                  axis=1))), 'gaussian', 6)).reshape(100, )
        TxCntInd = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(Cry_TxCnt / np.mean(Cry_TxCnt, axis=0), axis=1))),
                           'gaussian', 6)).reshape(100, )

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

        GTInd = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata, axis=1) / 14)), 'gaussian', 6)).reshape(100, )

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
            CSQ[0, i] = CMK[0] / CMP[0]
            CSP[:, i] = CMP

        CCI = 100 * np.sum(CSP * CSQ, axis=1) / np.sum(CSP[0,] * CSQ)

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
        CPP = ccipred * (CCI[-1] / ccipred[0])
        CCIPred = CPP + (CCI[-1] - CPP[0])

        CCI7 = np.round(((CCIPred[8] - CCIPred[0]) / CCIPred[0]) * 1000) / 10

        Cry_str = ['btc', 'eth', 'xmr', 'xrp']
        Par = np.zeros((4, 13))
        j = 0
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
        PPar = Par[:, 1:]
        PParc = np.round(Par[:, 0] * 1000) / 10

        cmpa = (AdrCntInd[-1] - AdrCntInd[-7]) / AdrCntInd[-7]
        cmpt = (TxCntInd[-1] - TxCntInd[-7]) / TxCntInd[-7]
        cmap = cmpt + cmpa

        cmip = (GTInd[-1] - GTInd[-7]) / GTInd[-7]

        CCIst = np.zeros((len(CCI) - 7, 1))
        for i in range(len(CCI) - 7):
            CCIst[i] = np.std(CCI[i:i + 7])
        CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

        CCIV = np.zeros((len(CCI) - 4, 1))
        for i in range(4, len(CCI)):
            CCIV[i - 4] = (CCI[i] - CCI[i - 4]) / 4
        CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 6))

        cmpp = (CCI[-1] - CCI[-7]) / CCI[-7]
        cmvp = (CCIstd[-1] - CCIstd[-7]) / CCIstd[-7]
        cmmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

        if np.sign(cmip) < 0 and np.sign(cmpp) < 0:
            cmgts = -1
        else:
            cmgts = np.sign(cmip) * np.sign(cmpp)

        ccpred = eng.CryPredictions(MDIFull, Mi, Pd, nargout=1)

        CCPred = ccpred + (lPdcnp[-1, :] - ccpred[0])
        CCPredS = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCPred)), 'gaussian', 10))
        CC7S = np.round(((CCPredS[8, :] - CCPredS[0, :]) / CCPredS[0, :]) * 1000) / 10

        btctx = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"btcND"][-100:, 0])), 'gaussian', 6)).reshape(100, )

        btcad = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"btcND"][-100:, 5])), 'gaussian', 6)).reshape(100, )

        btcpt = (btctx[-1] - btctx[-7]) / btctx[-7]
        btcpa = (btcad[-1] - btcad[-7]) / btcad[-7]
        btcap = btcpt + btcpa

        btcgt = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata[-100:, 0:2], axis=1) / 2)), 'gaussian',
                           6)).reshape(100, )

        btcip = (btcgt[-1] - btcgt[-7]) / btcgt[-7]

        CCI = lPdcnp[-122:, 0]

        CCIst = np.zeros((len(CCI) - 7, 1))
        for i in range(len(CCI) - 7):
            CCIst[i] = np.std(CCI[i:i + 7])
        CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

        CCIV = np.zeros((len(CCI) - 4, 1))
        for i in range(4, len(CCI)):
            CCIV[i - 4] = (CCI[i] - CCI[i - 4]) / 4
        CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

        btcpp = (CCI[-1] - CCI[-7]) / CCI[-7]

        btcvp = (CCIstd[-1] - CCIstd[-7]) / CCIstd[-7]

        btcmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

        btcvl = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 0])), 'gaussian', 10)).reshape(
            7, )
        btcvlp = (btcvl[-1] - btcvl[-7]) / btcvl[-7]

        if np.sign(btcvlp) < 0 and np.sign(btcpp) < 0:
            vol = -1
        else:
            vol = np.sign(btcvlp) * np.sign(btcpp)

        if np.sign(btcip) < 0 and np.sign(btcpp) < 0:
            gts = -1
        else:
            gts = np.sign(btcip) * np.sign(btcpp)

        btcbs = PPar[0, 0] * np.sign(btcap) + PPar[0, 1] * gts + PPar[0, 2] * np.sign(btcpp) + PPar[0, 3] * np.sign(
            btcvp) * np.sign(btcpp) + \
                PPar[0, 4] * np.sign(btcmp) + PPar[0, 5] * np.sign(cmmp) + PPar[0, 6] * vol + PPar[0, 7] * np.sign(
            CC7S[0]) + \
                PPar[0, 8] * np.sign(CCI7[0]) + PPar[0, 9] * np.sign(cmap) + PPar[0, 10] * cmgts + \
                PPar[0, 11] * np.sign(cmvp) * np.sign(cmpp)

        ethtx = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"ethND"][-100:, 0])), 'gaussian', 6)).reshape(100, )

        ethad = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"ethND"][-100:, 5])), 'gaussian', 6)).reshape(100, )


        ethpt = (ethtx[-1] - ethtx[-7]) / ethtx[-7]
        ethpa = (ethad[-1] - ethad[-7]) / ethad[-7]
        ethap = ethpt + ethpa

        ethgt = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata[-100:, [2, 3, 13]], axis=1) / 3)), 'gaussian',
                           6)).reshape(100, )

        ethip = (ethgt[-1] - ethgt[-7]) / ethgt[-7]

        CCI = lPdcnp[-122:, 1]

        CCIst = np.zeros((len(CCI) - 7, 1))
        for i in range(len(CCI) - 7):
            CCIst[i] = np.std(CCI[i:i + 7])
        CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

        CCIV = np.zeros((len(CCI) - 4, 1))
        for i in range(4, len(CCI)):
            CCIV[i - 4] = (CCI[i] - CCI[i - 4]) / 4
        CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

        ethpp = (CCI[-1] - CCI[-7]) / CCI[-7]

        ethvp = (CCIstd[-1] - CCIstd[-7]) / CCIstd[-7]

        ethmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

        ethvl = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 1])), 'gaussian', 10)).reshape(
            7, )
        ethvlp = (ethvl[-1] - ethvl[-7]) / ethvl[-7]

        if np.sign(ethvlp) < 0 and np.sign(ethpp) < 0:
            vol = -1
        else:
            vol = np.sign(ethvlp) * np.sign(ethpp)

        if np.sign(ethip) < 0 and np.sign(ethpp) < 0:
            gts = -1
        else:
            gts = np.sign(ethip) * np.sign(ethpp)

        ethbs = PPar[1, 0] * np.sign(ethap) + PPar[1, 1] * gts + PPar[1, 2] * np.sign(ethpp) + PPar[1, 3] * np.sign(
            ethvp) * np.sign(ethpp) + \
                PPar[1, 4] * np.sign(ethmp) + PPar[1, 5] * np.sign(cmmp) + PPar[1, 6] * vol + PPar[1, 7] * np.sign(
            CC7S[1]) + \
                PPar[1, 8] * np.sign(CCI7[0]) + PPar[1, 9] * np.sign(cmap) + PPar[1, 10] * cmgts + \
                PPar[1, 11] * np.sign(cmvp) * np.sign(cmpp)


        xmrtx = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"xmrND"][-100:, 0])), 'gaussian', 6)).reshape(100, )

        xmrap = (xmrtx[-1] - xmrtx[-7]) / xmrtx[-7]

        xmrgt = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(GTdata[-100:, 4])), 'gaussian', 6)).reshape(
            100, )

        xmrip = (xmrgt[-1] - xmrgt[-7]) / xmrgt[-7]

        CCI = lPdcnp[-122:, 2]

        CCIst = np.zeros((len(CCI) - 7, 1))
        for i in range(len(CCI) - 7):
            CCIst[i] = np.std(CCI[i:i + 7])
        CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

        CCIV = np.zeros((len(CCI) - 4, 1))
        for i in range(4, len(CCI)):
            CCIV[i - 4] = (CCI[i] - CCI[i - 4]) / 4
        CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

        xmrpp = (CCI[-1] - CCI[-7]) / CCI[-7]

        xmrvp = (CCIstd[-1] - CCIstd[-7]) / CCIstd[-7]

        xmrmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

        xmrvl = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 2])), 'gaussian', 10)).reshape(
            7, )
        xmrvlp = (xmrvl[-1] - xmrvl[-7]) / xmrvl[-7]

        if np.sign(xmrvlp) < 0 and np.sign(xmrpp) < 0:
            vol = -1
        else:
            vol = np.sign(xmrvlp) * np.sign(xmrpp)

        if np.sign(xmrip) < 0 and np.sign(xmrpp) < 0:
            gts = -1
        else:
            gts = np.sign(xmrip) * np.sign(xmrpp)

        xmrbs = PPar[2, 0] * np.sign(xmrap) + PPar[2, 1] * gts + PPar[2, 2] * np.sign(xmrpp) + PPar[2, 3] * np.sign(
            xmrvp) * np.sign(xmrpp) + \
                PPar[2, 4] * np.sign(xmrmp) + PPar[2, 5] * np.sign(cmmp) + PPar[2, 6] * vol + PPar[2, 7] * np.sign(
            CC7S[2]) + \
                PPar[2, 8] * np.sign(CCI7[0]) + PPar[2, 9] * np.sign(cmap) + PPar[2, 10] * cmgts + \
                PPar[2, 11] * np.sign(cmvp) * np.sign(cmpp)


        xrptx = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"xrpND"][-100:, 0])), 'gaussian', 6)).reshape(100, )

        xrpad = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(vars()[f"xrpND"][-100:, 1])), 'gaussian', 6)).reshape(100, )

        xrppt = (xrptx[-1] - xrptx[-7]) / xrptx[-7]
        xrppa = (xrpad[-1] - xrpad[-7]) / xrpad[-7]
        xrpap = xrppt + xrppa

        xrpgt = np.asarray(
            eng.smoothdata(matlab.double(np.ndarray.tolist(np.sum(GTdata[-100:, [5, 9]], axis=1) / 2)), 'gaussian',
                           6)).reshape(100, )

        xrpip = (xrpgt[-1] - xrpgt[-7]) / xrpgt[-7]

        CCI = lPdcnp[-122:, 3]

        CCIst = np.zeros((len(CCI) - 7, 1))
        for i in range(len(CCI) - 7):
            CCIst[i] = np.std(CCI[i:i + 7])
        CCIstd = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIst)), 'gaussian', 7))

        CCIV = np.zeros((len(CCI) - 4, 1))
        for i in range(4, len(CCI)):
            CCIV[i - 4] = (CCI[i] - CCI[i - 4]) / 4
        CCIm = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(CCIV)), 'gaussian', 10))

        xrppp = (CCI[-1] - CCI[-7]) / CCI[-7]

        xrpvp = (CCIstd[-1] - CCIstd[-7]) / CCIstd[-7]

        xrpmp = (CCIm[-1] - CCIm[-7]) / CCIm[-7]

        xrpvl = np.asarray(eng.smoothdata(matlab.double(np.ndarray.tolist(lPdcnpv[-7:, 3])), 'gaussian', 10)).reshape(
            7, )
        xrpvlp = (xrpvl[-1] - xrpvl[-7]) / xrpvl[-7]

        if np.sign(xrpvlp) < 0 and np.sign(xrppp) < 0:
            vol = -1
        else:
            vol = np.sign(xrpvlp) * np.sign(xrppp)

        if np.sign(xrpip) < 0 and np.sign(xrppp) < 0:
            gts = -1
        else:
            gts = np.sign(xrpip) * np.sign(xrppp)

        xrpbs = PPar[3, 0] * np.sign(xrpap) + PPar[3, 1] * gts + PPar[3, 2] * np.sign(xrppp) + PPar[3, 3] * np.sign(
            xrpvp) * np.sign(xrppp) + \
                PPar[3, 4] * np.sign(xrpmp) + PPar[3, 5] * np.sign(cmmp) + PPar[3, 6] * vol + PPar[3, 7] * np.sign(
            CC7S[3]) + \
                PPar[3, 8] * np.sign(CCI7[0]) + PPar[3, 9] * np.sign(cmap) + PPar[3, 10] * cmgts + \
                PPar[3, 11] * np.sign(cmvp) * np.sign(cmpp)

        CCPT=[btcbs, ethbs, xmrbs, xrpbs]
        CA = []
        for i in range(len(CCPT)):
            if CCPT[i] > 0:
                CA += "↗"
            elif CCPT[i] < 0:
                CA += "↘"
            else:
                CA += "➡"


        # Create a tweet
        api.update_status(f"#Crypto 7Day Forecast: \n"
                          f"\n"
                          f"#BTC: {CA[0]}\n"
                          f"\n"
                          f"#ETH:      {CA[1]}\n"
                          f"\n"
                          f"#XMR:     {CA[2]}\n"
                          f"\n"
                          f"#XRP:      {CA[3]}\n"
                          f"\n"
                          f"Predictions Accuracy: BTC {PParc[0]}%, ETH {PParc[1]}%, XMR {PParc[2]}%, XRP {PParc[3]}%"
                          )

    elif Ndate.hour == 9 and (Ndate.weekday() in [0, 1, 3, 5]):

        query = f"SELECT date " \
                f"FROM BTCUSDTd " \
                f"ORDER BY date DESC " \
                f"LIMIT 100 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        list.reverse(Col)
        Dates = np.asarray(Col)
        cg = CoinGeckoAPI()

        if Ndate.weekday() == 1:

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
                CSQ[0, i] = CMK[0] / CMP[0]
                CSP[:, i] = CMP

            CCI = 100 * np.sum(CSP * CSQ, axis=1) / np.sum(CSP[0, ] * CSQ)

            plt.figure(figsize=(9, 5), dpi=400)
            plt.title("Crypto Index", fontsize=8)
            plt.xticks(rotation=9, fontsize=8)
            plt.yticks(fontsize=6)
            plt.plot(Dates[-60:], CCI[-60:],linewidth=6)
            plt.savefig("Plots\CCI.png")
            plt.close()

            status = "Chart of the day:\n" \
                     "Crypto Market Index\n" \
                     "Last 60 days\n" \
                     "\n" \
                     "#Crypto #Bitcoin #ETH #BNB #ADA #DOGE #SOL"

            img = "Plots\CCI.png"
            api.update_with_media(img, status)

        elif Ndate.weekday() == 3:

            client = Client("",
                            "")

            CCrk = sorted(cg.get_coins_markets(vs_currency='usd'), key=lambda x: x["market_cap_rank"])[:20]
            CClst=[]
            for i in range(len(CCrk)):
                if CCrk[i]["symbol"] != "btc" and CCrk[i]["symbol"] != "usdt" and CCrk[i]["symbol"] != "busd" \
                        and CCrk[i]["symbol"] != "usdc":
                    CClst += [(CCrk[i]["symbol"]+"btc").upper()]

            Cry_str= ["BTCUSDT"] + CClst

            CCTop = np.zeros((30, len(CClst)))
            i = -1
            for crypto in Cry_str:
                print(crypto)
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{30 + 1} days ago UTC")
                print(data)
                data_np = np.asarray(data)
                if crypto == 'BTCUSDT':
                    BTCP = data_np[-30 - 1:-1, 4].astype(float)
                else:
                    CCTop[:, i] = data_np[-30 - 1:-1, 4].astype(float)*BTCP
                i += 1

            ccprc = np.ndarray.tolist((CCTop[-1, :]-CCTop[-7, :]) / CCTop[-7, :])
            ccps = sorted(ccprc, reverse=True)[0]
            tcind = ccprc.index(ccps)
            tppc = np.round(ccprc[tcind]*1000)/10

            plt.figure(figsize=(9, 5), dpi=400)
            plt.title(f"Week Top Performer: {CClst[tcind][:-3]}", fontsize=8)
            plt.xticks(rotation=9, fontsize=8)
            plt.ylabel("Price $")
            plt.yticks(fontsize=6)
            plt.plot(Dates[-30:], CCTop[:, tcind],linewidth=6)
            plt.savefig("Plots\CCTop.png")
            plt.close()

            if tppc > 0:
                txtd='Up'
            else:
                txtd='Down'

            status = f"This Week's Top Performer ➡ #{CClst[tcind][:-3]}\n" \
                     f"{txtd} {tppc}% over the last 7 days\n" \
                     f"\n" \
                     f"#Crypto #Bitcoin #ETH #BNB #ADA #DOGE #SOL"

            img = "Plots\CCTop.png"
            api.update_with_media(img, status)

        elif Ndate.weekday() == 0:

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
                CSQ[0, i] = CMK[0] / CMP[0]
                CSP[:, i] = CMP

            CCI = 100 * np.sum(CSP * CSQ, axis=1) / np.sum(CSP[0,] * CSQ)

            CCIst = np.zeros((len(CCI) - 7, 1))
            for i in range(len(CCI) - 7):
                CCIst[i] = np.std(CCI[i:i + 7])
            CCIstd = smoothdat(CCIst, 7)

            plt.figure(figsize=(9, 5), dpi=400)
            plt.title("Crypto Index Volatility", fontsize=8)
            plt.xticks(rotation=9, fontsize=8)
            plt.yticks(fontsize=6)
            plt.plot(Dates[-60:], CCIstd[-60:],linewidth=6)
            plt.savefig("Plots\CCIstd.png")
            plt.close()

            status = "Chart of the day:\n" \
                     "Crypto Market Index Volatility\n" \
                     "Last 60 days\n" \
                     "\n" \
                     "#Crypto #Bitcoin #ETH #BNB #ADA #DOGE #SOL"

            img = "Plots\CCIstd.png"
            api.update_with_media(img, status)

    elif Ndate.hour == 17 and (Ndate.weekday() in [0, 1, 2, 3, 5]):

        if Ndate.weekday() == 0:
            Cry=random.sample(["BTC","ETH","XMR","XRP"], k=1)[0]
            query = f"SELECT date " \
                    f"FROM {Cry}USDTd " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 60 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            Dates = np.asarray(Col)

            query = f"SELECT AdrActCnt " \
                    f"FROM {Cry}MD " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 63 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            cryad = smoothdat(np.asarray(Col), 6)

            plt.figure(figsize=(9, 5), dpi=400)
            plt.title(f"{Cry} Active Addresses", fontsize=8)
            plt.xticks(rotation=9, fontsize=8)
            plt.ylabel("Act. Address Count")
            plt.yticks(fontsize=6)
            plt.plot(Dates, cryad[-60:],linewidth=6)
            plt.savefig(fr"Plots\{Cry}ActAdd.png")
            plt.close()

            status = f"Chart of the day:\n" \
                     f"#{Cry} Active Addresses\n" \
                     f"Last 60 days\n" \
                     f"\n" \
                     f"#Crypto #Bitcoin #ETH #XRP #BNB #ADA #XMR"

            img = f"Plots\{Cry}ActAdd.png"
            api.update_with_media(img, status)

        elif Ndate.weekday() == 1:

            Cry = random.sample(["BTC", "ETH", "XMR", "XRP"], k=1)[0]
            if Cry=="BTC":
                Metr="Bitcoin, BTC"
                nm=2
            elif Cry=="ETH":
                Metr="ETH, Ethereum"
                nm=2
            elif Cry=="XMR":
                Metr="Monero"
                nm=1
            elif Cry=="XRP":
                Metr="Ripple_crypto, XRP"
                nm=2

            query = f"SELECT date " \
                    f"FROM {Cry}USDTd " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 60 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            Dates = np.asarray(Col)

            query = f"SELECT {Metr} " \
                    f"FROM GT_searches " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 63 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            GTdata = np.asarray(Col)

            Crygt = smoothdat(np.sum(GTdata, axis=1) / nm, 6)[-60:]

            plt.figure(figsize=(9, 5), dpi=400)
            plt.title("BTC Search Queries Index", fontsize=8)
            plt.xticks(rotation=9, fontsize=8)
            plt.yticks(fontsize=6)
            plt.plot(Dates, Crygt,linewidth=6)
            plt.savefig(fr"Plots\{Cry}GT.png")
            plt.close()

            status = f"Chart of the day:\n" \
                     f"#{Cry} Search Queries Index\n" \
                     f"Last 60 days\n" \
                     f"\n" \
                     f"#Crypto #ETH #XRP #BNB #ADA #DOGE #SOL"

            img = fr"Plots\{Cry}GT.png"
            api.update_with_media(img, status)

        elif Ndate.weekday() == 2:

            status = "Get ahead of the curve with the HC.dept Weekly Report, latest report plus first week free!  ;) " \
                     "https://buy.stripe.com/8wM002eIH0xIgzmcMO\n" \
                     "\n" \
                     "#Crypto #Bitcoin #ETH #XMR #XRP #BNB #ADA #DOGE #SOL"

            img = "Images\Tweetim.jfif"
            api.update_with_media(img, status)

        elif Ndate.weekday() == 3:
            cg = CoinGeckoAPI()
            CCata = sorted(cg.get_coins_categories(), key=lambda x: x["market_cap"])
            CCat = sorted(CCata[-20:], key=lambda x: x["market_cap_change_24h"], reverse=True)[:7]

            CCate = []
            Cpc = np.zeros(len(CCat))
            for i in range(len(CCat)):
                CCate += [CCat[i]["name"]]
                Cpc[i] += [CCat[i]["market_cap_change_24h"]]

            Cpc = np.asarray(Cpc)
            x_pos = np.asarray([i for i, _ in enumerate(CCate)])

            mask1 = Cpc >= 0
            mask2 = Cpc < 0

            plt.figure(figsize=(9, 6), dpi=400)
            plt.bar(x_pos[mask1], Cpc[mask1])
            plt.bar(x_pos[mask2], Cpc[mask2], color='tab:orange')
            plt.ylim(top=max(Cpc[mask1])+2)
            if Cpc[mask2]:
                plt.ylim(bottom=min(Cpc[mask2]) - 1)
            plt.ylabel("24h % change")
            plt.title("Top 7 categories by 24h % change")
            plt.xticks(x_pos, CCate)
            plt.xticks(rotation=15, fontsize=8)
            i = 0
            for index, value in enumerate(Cpc):
                plt.text(x=index - 0.25, y=value + np.sign(value) * 0.4,
                         s=str(np.round(Cpc[i] * 1000) / 1000)[:5] + "%",
                         va='center')
                i += 1

            plt.savefig("Plots\CCat.png")
            plt.close()

            status = "Chart of the day:\n" \
                     "Top 7 Biggest Movers (Crypto Categories)\n" \
                     "(Out of the top 20 Categories by Market Cap)\n" \
                     "24h % Change Moves\n" \
                     "\n" \
                     "#Crypto #Bitcoin #ETH #BNB #ADA #DOGE #SOL"

            img = "Plots\CCat.png"
            api.update_with_media(img, status)

        elif Ndate.weekday()==5:

            query = f"SELECT date, BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM Profit_Loss " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 168"
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            Profs = np.asarray(Col)
            TotalProfit= np.cumsum(np.sum(Profs[:, 1:], axis=1))
            Prdats = Profs[:, 0]

            query = f"SELECT value " \
                    f"FROM TotalFunds " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 168"
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            TotalFunds = np.asarray(Col)[0][0]

            plt.figure(figsize=(9, 5), dpi=400)
            plt.title("Briareos Profit", fontsize=8)
            plt.xticks(rotation=9, fontsize=8)
            plt.yticks(fontsize=6)
            plt.ylabel("% Profit")
            plt.plot(Prdats, TotalProfit/TotalFunds, linewidth=6)
            plt.savefig(fr"Plots\BriProf.png")
            plt.close()

            status = "Briareos % Profit (last 7 days)\n" \
                     "\n" \
                     "#Crypto #Bitcoin #ETH #XLM #XMR #XRP #LINK #NEO"

            img = "Plots\BriProf.png"
            api.update_with_media(img, status)


    elif Ndate.hour == 9 and Ndate.weekday()==5:
        status = "Weekly Reports Sent! Get yours today, latest report plus first week free!  ;) " \
                 "https://buy.stripe.com/8wM002eIH0xIgzmcMO\n" \
                 "\n" \
                 "#Crypto #Bitcoin #ETH #XMR #XRP #BNB #ADA #DOGE #SOL"

        img = "Images\Tweetim.jfif"
        api.update_with_media(img, status)