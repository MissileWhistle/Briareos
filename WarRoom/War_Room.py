# This module is responsible for creating a streamlit dashboard for monitoring data aquired and generated
# by the algo-trading system, divided by modules


# Import Modules

import matplotlib.pyplot as plt
import matlab.engine
import numpy as np
import math
import pickle
import mysql.connector
import pandas
import math as mt
from datetime import date, timedelta, datetime
import streamlit as st

# Connect to Database

Database = mysql.connector.connect(
    host="192.168.1.5",
    user="root",
    passwd="Briareos")

my_cursor = Database.cursor()

my_cursor.execute("USE briareos")

# Create Dashboard
st.sidebar.title("Briareos War Room")


# Gathered data

# Import Daily data

query = f"SELECT price " \
        f"FROM CryptoIndex " \
        f"ORDER BY date DESC " \
        f"LIMIT 280 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [item for sublist in [list(i) for i in col] for item in sublist]
list.reverse(Col)
mdfll = np.asarray(Col).reshape((280, 1))

Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
lPdcnp = np.zeros((len(mdfll), len(Cry_str)))
r = 0
for crypto in Cry_str:
    query = f"SELECT close " \
            f"FROM {crypto}d " \
            f"ORDER BY date DESC " \
            f"LIMIT 280 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [item for sublist in [list(i) for i in col] for item in sublist]
    list.reverse(Col)
    lPdcnp[:, r] = Col
    r += 1
Mpd = lPdcnp

query = f"SELECT EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, " \
        f"SPY, EWC, MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT, " \
        f"VDE, ERUS, XT, IAU, PICK, ICLN, ITA " \
        f"FROM worldindices " \
        f"ORDER BY date DESC " \
        f"LIMIT 280 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
Worldind = np.asarray(Col)

query = f"SELECT TSLA, MSFT, GOOGL, AAPL, IBM, AMZN, FB, HYMTF, VWAGY " \
        f"FROM stocks " \
        f"ORDER BY date DESC " \
        f"LIMIT 280 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
Stocks = np.asarray(Col)

query = f"SELECT BNB, IOTA, VET, ADA, LTC " \
        f"FROM cryptos " \
        f"ORDER BY date DESC " \
        f"LIMIT 280 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
Cryptos = np.asarray(Col)

Crypto_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo', 'gas', 'usdt', 'doge', 'ada', 'ltc']
for crypto in Crypto_str:
    query = f"SELECT * " \
            f"FROM {crypto}MD " \
            f"ORDER BY date DESC " \
            f"LIMIT 280 "
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
        f"LIMIT 280 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
GTdata = np.asarray(Col)

mdi = np.concatenate((CryptoND, GTdata, Worldind, Stocks, Cryptos, Mpd, mdfll), axis=1)

query = f"SELECT date " \
        f"FROM worldindices " \
        f"ORDER BY date DESC " \
        f"LIMIT 280 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [item for sublist in [list(i) for i in col] for item in sublist]
list.reverse(Col)
mddate = Col

# Daily data plots

if st.sidebar.checkbox('Daily Data'):
    st.title('Daily Market and Network Data')

    # Crypto index
    if st.checkbox('Crypto Index'):

        st.write('## Crypto Index')

        fig = plt.figure()
        plt.plot(mddate[-280:], mdfll[-280:])
        plt.xlabel("date")
        plt.ylabel("price")
        plt.title("CryptoIndex")
        st.plotly_chart(fig)

    # World Indexes
    if st.checkbox('World Indices'):

        st.write('## World Indices')

        WI_str = ['EWA', 'EWT', 'INDA', 'EWZ', 'EEM', 'EWQ', 'EWM', 'EWU', 'EWG',
                  'SPY', 'EWC', 'MCHI', 'VEA', 'EIDO', 'EWS', 'VGK', 'EWJ', 'IYW', 'VGT',
                  'VDE', 'ERUS', 'XT', 'IAU', 'PICK', 'ICLN', 'ITA']

        i = 0
        for index in WI_str:
            fig = plt.figure(i)
            plt.plot(mddate[-280:], Worldind[-280:, i])
            plt.xlabel("date")
            plt.ylabel("price")
            plt.title(f"{index}")
            st.plotly_chart(fig)
            i += 1

    # Stocks
    if st.checkbox('Stocks'):

        st.write('## Stocks')

        WI_str = ['TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM', 'AMZN', 'FB', 'HYMTF', 'VWAGY']

        i = 0
        for index in WI_str:
            fig = plt.figure(i)
            plt.plot(mddate[-280:], Stocks[-280:, i])
            plt.xlabel("date")
            plt.ylabel("price")
            plt.title(f"{index}")
            st.plotly_chart(fig)
            i += 1

    # Gt data
    if st.checkbox('Google Trends data'):

        st.write('## Google Trends data')

        GT_dbname = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple_crypto', 'Stellar_Lumens', 'ChainLink',
                     'NEO_price', 'XRP', 'blockchain', 'cryptocurrency', 'altcoin', 'Smart Contract', 'Binance']

        i = 0
        for index in GT_dbname:
            fig = plt.figure(i)
            plt.plot(mddate[-280:], GTdata[-280:, i])
            plt.xlabel("date")
            plt.ylabel("volume")
            plt.title(f"{index}")
            st.plotly_chart(fig)
            i += 1

    # Network Data
    if st.checkbox('Cryptos Network Data'):
        st.write('## Cryptos Network Data')
        Crypto_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo', 'gas', 'usdt', 'doge', 'ada', 'ltc']
        Cry_Metrics = [['TxCnt', 'IssContNtv', 'TxTfrValMedNtv', 'TxTfrValMedUSD', 'FeeMeanUSD', 'AdrActCnt', 'DiffMean',
                        'FlowTfrFromExCnt', 'FlowOutExNtv'],
                        ['TxCnt', 'IssContNtv', 'TxTfrValMedNtv', 'TxTfrValMedUSD', 'FeeMeanUSD', 'AdrActCnt', 'DiffMean',
                        'FlowTfrFromExCnt', 'FlowOutExNtv'],
                        ['TxCnt', 'TxTfrValAdjNtv', 'FeeMeanNtv'],
                        ['TxCnt', 'FeeMeanNtv', 'DiffMean', 'BlkSizeMeanByte'],
                        ['TxCnt', 'TxTfrValAdjNtv', 'AdrActCnt', 'CapMVRVFF', 'FeeMeanNtv'],
                        ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'SplyAct7d', 'NDF'],
                        ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'BlkSizeMeanByte'],
                        ['TxCnt', 'AdrActCnt'],
                        ['AdrActCnt', 'TxTfrValAdjNtv'],
                        ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'TxTfrValMedNtv', 'TxTfrValMeanNtv', 'FeeMeanNtv', 'DiffMean',
                         'BlkSizeMeanByte'],
                        ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'NDF', 'FeeMeanUSD', 'FeeMedNtv', 'BlkSizeMeanByte'],
                        ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'IssContUSD', 'FeeMeanNtv', 'DiffMean', 'BlkSizeMeanByte']]

        i = 0
        j = 0
        for crypto in Crypto_str:
            st.write(f'# {crypto}')
            for metric in Cry_Metrics[j]:
                fig = plt.figure(i)
                plt.plot(mddate[-280:], CryptoND[-280:, i])
                plt.xlabel("date")
                plt.ylabel("value")
                plt.title(f"{crypto}_{metric}")
                st.plotly_chart(fig)
                i += 1
            j += 1

    # Cryptos daily price
    if st.checkbox('Cryptos price'):
        st.write('## Cryptos daily price data')

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        Cry_str2 = ['BNBUSDT', 'IOTAUSDT', 'VETUSDT', 'ADAUSDT', 'LTCUSDT']
        i = 0
        for index in Cry_str:
            fig = plt.figure(i)
            plt.plot(mddate[-280:], Mpd[-280:, i])
            plt.xlabel("date")
            plt.ylabel("price")
            plt.title(f"{index}d")
            st.plotly_chart(fig)
            i += 1
        for index in Cry_str2:
            fig = plt.figure(i)
            plt.plot(mddate[-280:], Cryptos[-280:, i-len(Cry_str)])
            plt.xlabel("date")
            plt.ylabel("price")
            plt.title(f"{index}d")
            st.plotly_chart(fig)
            i += 1

# Import Hourly data

Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
metric = ['high', 'low']
Mvar = ['lPdh', 'lPdl']
lPdhnp = np.zeros((100, len(Cry_str)))
lPdlnp = np.zeros((100, len(Cry_str)))
j = 0
for metrc in metric:
    r = 0
    for crypto in Cry_str:
        query = f"SELECT {metrc} " \
                f"FROM {crypto}h " \
                f"ORDER BY date DESC " \
                f"LIMIT 100 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [item for sublist in [list(i) for i in col] for item in sublist]
        list.reverse(Col)
        vars()[f"{Mvar[j]}np"][:, r] = Col
        r += 1
    j += 1
Mph = (lPdhnp + lPdlnp) * (1 / 2)

query = f"SELECT date " \
        f"FROM btcusdth " \
        f"ORDER BY date DESC " \
        f"LIMIT 100 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [item for sublist in [list(i) for i in col] for item in sublist]
list.reverse(Col)
Pddateh = Col

# Plot Hourly Data

if st.sidebar.checkbox('Hourly Data'):
    st.title('Hourly Cryptos Market Prices')

    i = 0
    for index in Cry_str:
        fig = plt.figure(i)
        plt.plot(Pddateh, Mph[:, i])
        plt.xlabel("date")
        plt.ylabel("price")
        plt.title(f"{index}h")
        st.plotly_chart(fig)
        i += 1


# Predictions Module

# Predictions Module data

query = f"SELECT t " \
        f"FROM Miscellaneous " \
        f"LIMIT 1 "
my_cursor.execute(query)
col = my_cursor.fetchall()
pret = int(col[0][0])

with open(r"\\WIN-PLGN6Q5V4CA\Users\Machine2\Desktop\PickleFiles\predvars.pickle", "rb") as f:
    CFTA, MdR, MdRvar, MdRExp, MEMpredid, Pdr1, Pdr2, Pdr3, \
    Pdr4, Pdr5, Pdr6, Pdr7, PDvar, PDExp, PPMpredid, Predicts, n = pickle.load(f)

query = f"SELECT CryptoIndexR, BTCR, ETHR, " \
        f"XLMR, XMRR, XRPR, LINKR, NEOR " \
        f"FROM Predictions " \
        f"ORDER BY date DESC " \
        f"LIMIT 40 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
Predict = np.asarray(Col)

query = f"SELECT date " \
        f"FROM Predictions " \
        f"ORDER BY date DESC " \
        f"LIMIT 40 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [item for sublist in [list(i) for i in col] for item in sublist]
list.reverse(Col)
pretdate = np.asarray(Col)

query = f"SELECT date " \
        f"FROM portfolioopts " \
        f"ORDER BY date DESC " \
        f"LIMIT 1 "
my_cursor.execute(query)
col = my_cursor.fetchall()
dbdate = col[0][0]
dbdt = datetime(dbdate.year, dbdate.month, dbdate.day)
pretcount = (datetime.now() - dbdt).days

Cry_str0 = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
MDI_str = ['BTC_TxCnt', 'BTC_IssContNtv', 'BTC_TxTfrValMedNtv', 'BTC_TxTfrValMedUSD', 'BTC_FeeMeanUSD', 'BTC_AdrActCnt',
           'BTC_DiffMean', 'BTC_FlowTfrFromExCnt', 'BTC_FlowOutExNtv',
           'ETH_TxCnt', 'ETH_IssContNtv', 'ETH_TxTfrValMedNtv', 'ETH_TxTfrValMedUSD', 'ETH_FeeMeanUSD', 'ETH_AdrActCnt',
           'ETH_DiffMean', 'ETH_FlowTfrFromExCnt', 'ETH_FlowOutExNtv',
           'XLM_TxCnt', 'XLM_TxTfrValAdjNtv', 'XLM_FeeMeanNtv', 'XMR_TxCnt', 'XMR_FeeMeanNtv', 'XMR_DiffMean',
           'XMR_BlkSizeMeanByte', 'XRP_TxCnt', 'XRP_TxTfrValAdjNtv',
           'XRP_AdrActCnt', 'XRP_CapMVRVFF', 'XRP_FeeMeanNtv', 'LINK_TxCnt',
           'LINK_AdrActCnt', 'LINK_TxTfrValAdjNtv', 'LINK_SplyAct7d', 'LINK_NDF', 'NEO_TxCnt',
           'NEO_AdrActCnt', 'NEO_TxTfrValAdjNtv', 'NEO_BlkSizeMeanByte', 'Gas_TxCnt', 'Gas_AdrActCnt',
           'USDT_AdrActCnt', 'USDT_TxTfrValAdjNtv', 'Doge_TxCnt', 'Doge_AdrActCnt',
           'Doge_TxTfrValAdjNtv', 'Doge_TxTfrValMedNtv', 'Doge_TxTfrValMeanNtv', 'Doge_FeeMeanNtv', 'Doge_DiffMean',
           'Doge_BlkSizeMeanByte', 'ADA_TxCnt', 'ADA_AdrActCnt', 'ADA_TxTfrValAdjNtv', 'ADA_NDF', 'ADA_FeeMeanUSD',
           'ADA_FeeMedNtv', 'ADA_BlkSizeMeanByte', 'LTC_TxCnt', 'LTC_AdrActCnt', 'LTC_TxTfrValAdjNtv', 'LTC_IssContUSD',
           'LTC_FeeMeanNtv', 'LTC_DiffMean', 'LTC_BlkSizeMeanByte', "GT_Bitcoin", "GT_BTC", "GT_ETH", "GT_Ethereum",
           "GT_Monero", 'GT_Ripple_crypto', 'GT_Stellar_Lumens', 'GT_ChainLink', 'GT_NEO_price', 'GT_XRP',
           'GT_blockchain', 'GT_cryptocurrency', 'GT_altcoin', 'GT_Smart Contract', 'GT_Binance',
           'EWA', 'EWT', 'INDA', 'EWZ', 'EEM', 'EWQ', 'EWM', 'EWU', 'EWG',
           'SPY', 'EWC', 'MCHI', 'VEA', 'EIDO', 'EWS', 'VGK', 'EWJ', 'IYW', 'VGT',
           'VDE', 'ERUS', 'XT', 'IAU', 'PICK', 'ICLN', 'ITA',
           'TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM', 'AMZN', 'FB', 'HYMTF', 'VWAGY', 'BNBUSDT', 'IOTAUSDT',
           'VETUSDT', 'ADAUSDT', 'LTCUSDT', 'BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT',
           'NEOUSDT', 'CryptoIndex']

MCn = int(n)

if st.sidebar.checkbox('Predictions Module'):
    st.title('Predictions Module Data')

    Rdates = pandas.date_range(pretdate[-1] - timedelta(days=35 + 49 + pretcount),
                               pretdate[-1] - timedelta(days=pretcount))

    # M.C. Regressions

    if st.checkbox('Regressions'):
        st.header('M.C.Regressions')

        # Crypto index Regressions Plot
        st.subheader('Crypto Index')

        MdRnp = np.asarray(MdR)

        Rdata = np.zeros((pret + 50, MCn))
        for s in range(MCn):
            Rdata[:, s] = np.hstack((mdfll[-(50+pretcount+1):-(pretcount+1), 0], MdRnp[:, s]))
        plt.plot(Rdates, Rdata, color="tab:orange")
        plt.plot(Rdates, np.mean(Rdata,axis=1), color="tab:blue")
        plt.xticks(rotation=9)
        plt.xlabel("date")
        plt.ylabel("price")
        plt.title("R_CryptoIndex")
        st.pyplot()

        st.write('### CryptoIndex Stats. (7d)')
        metdta = {'std': math.sqrt(MdRvar), 'Exp': MdRExp}
        Mdmetdta = pandas.DataFrame(data=metdta, index=['CryptoIndexR'])
        st.table(Mdmetdta)

        # Cryptos price Regressions Plots
        st.subheader('Cryptos Prices (Port)')

        PdRdate = Rdates
        PdR_str = ['Pdr1', 'Pdr2', 'Pdr3', 'Pdr4', 'Pdr5', 'Pdr6', 'Pdr7']
        for reg in PdR_str:
            vars()[f"{reg}np"] = np.asarray(vars()[f"{reg}"])

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        i = 0
        for index in Cry_str:
            Rdata = np.zeros((pret + 50, MCn))
            for s in range(MCn):
                Rdata[:, s] = np.hstack((Mpd[-(50+pretcount+1):-(pretcount+1), i],
                                            vars()[f"{PdR_str[i]}np"][: ,s]))
            plt.plot(PdRdate, Rdata, color="tab:orange")
            plt.plot(PdRdate, np.mean(Rdata, axis=1), color="tab:blue")
            plt.xticks(rotation=9)
            plt.xlabel("date")
            plt.ylabel("price")
            plt.title(f"R_{index}")
            st.pyplot()
            i += 1

        st.write('### Cryptos Stats. (7d)')
        metdta = {'PDstd': np.sqrt(PDvar[0]), 'PDExp': PDExp[0]}
        Pdmetdta = pandas.DataFrame(metdta, index=Cry_str)
        st.table(Pdmetdta)

        st.write('### Cryptos Movement Pred. (7d)')
        metdtam = {'Predict': Predicts[0]}
        Pdmetdtam = pandas.DataFrame(metdtam, index=Cry_str)
        st.table(Pdmetdtam)

    # Regressions at t prediction Plots

    if st.checkbox('Regress. at dt'):
        st.header('Regressions Predictions at +dt')

        Predlen = len(Predict[0])
        preddate = pandas.date_range(date.today() - timedelta(days=35 * 7 + pretcount),
                                     date.today() - timedelta(days=1 + pretcount))

        # R Crypto index pred
        st.write('## Crypto Index (7 days)')
        fig = plt.figure()
        plt.plot(preddate, mdfll[-(35*7 + pretcount + 1):-(pretcount+1), 0])
        plt.plot(pretdate, Predict[:, 0])
        plt.xlabel("date")
        plt.ylabel("price")
        plt.title("R_CryptoIndex_tpred")
        st.plotly_chart(fig)

        # R Cryptos price pred
        st.subheader('Crypto prices (7 days) )')

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        r = 0
        i = 1
        for index in Cry_str:
            fig = plt.figure(i)
            plt.plot(preddate, Mpd[-(35*7 + pretcount + 1):-(pretcount+1), r])
            plt.plot(pretdate, Predict[:, i])
            plt.xlabel("date")
            plt.ylabel("price")
            plt.title(f"R_{index}_tpred")
            st.plotly_chart(fig)
            i += 1
            r += 1


    # Curve fitting Plots
    if st.checkbox('Curve Fit'):
        st.header('Curve Fit Predictions')

        i = 0
        dtdates = pandas.date_range(date.today() - timedelta(days=2 * pret + pretcount - 1),
                                    date.today() - timedelta(days=pretcount))
        cfdates = pandas.date_range(date.today() - timedelta(days=2 * pret + pretcount - 1),
                                    date.today() + timedelta(days=pret - pretcount))
        for ts in MDI_str:
            cfdata = np.asarray(CFTA)[:, i]
            MDIdata = mdi[-(2*pret + pretcount + 1):-(pretcount+1), i]
            fig = plt.figure(i)
            plt.plot(dtdates, MDIdata, color="tab:blue")
            plt.plot(cfdates, cfdata, color="tab:orange")
            plt.xlabel("date")
            plt.ylabel("price")
            plt.title(f"{ts}")
            st.plotly_chart(fig)
            i += 1

# Portfolio optimization data

if st.sidebar.checkbox('Port.Opt. Module'):
    st.title('Portfolio Optimization Data')
    # Portfolio optimization data
    st.header('Short Term Portfolio')
    SPort = pandas.read_sql(f"SELECT * "
                            f"FROM PortfolioOptS "
                            f"ORDER BY date DESC "
                            f"LIMIT 8 ", con=Database)
    st.table(SPort.set_index('date'))
    st.header('Long Term Portfolio')
    LPort = pandas.read_sql(f"SELECT * "
                            f"FROM PortfolioOptL "
                            f"ORDER BY date DESC "
                            f"LIMIT 8 ", con=Database)
    st.table(LPort.set_index('date'))


# Trading optimization data
if st.sidebar.checkbox('Trading Opt. Module'):
    # Short-Term Opt
    st.header('Short-Term Opt.')
    Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
    dta = ['SvarMACD', 'SvarOBV', 'SvarADL', 'SvarATR', 'SvarOSC', 'SvarCCI', 'SStrt']
    for crypto in Cry_str:
        st.header(f'{crypto}')
        for data in dta:
            st.write(f'#### {data}')
            vars()[f"{crypto}_{data}S"] = pandas.read_sql(f"SELECT * "
                                                          f"FROM {crypto}_{data} "
                                                          f"ORDER BY date DESC "
                                                          f"LIMIT 3 ", con=Database)
            st.table(vars()[f"{crypto}_{data}S"].set_index('date'))

    # Long-Term Opt
    st.header('Long-Term Opt.')
    Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
    dta = ['LvarMACD', 'LvarOBV', 'LvarADL', 'LvarATR', 'LvarOSC', 'LvarCCI', 'LStrt']
    for crypto in Cry_str:
        st.header(f'{crypto}')
        for data in dta:
            st.write(f'#### {data}')
            vars()[f"{crypto}_{data}L"] = pandas.read_sql(f"SELECT * "
                                                          f"FROM {crypto}_{data} "
                                                          f"ORDER BY date DESC "
                                                          f"LIMIT 3 ", con=Database)
            st.table(vars()[f"{crypto}_{data}L"].set_index('date'))


# Trading Data

query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
        f"FROM Profit_Loss " \
        f"ORDER BY date DESC "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
TotalProfit = np.asarray(Col)

query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
        f"FROM Profit_Loss_Short " \
        f"ORDER BY date DESC " \
        f"LIMIT 1200 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
ShortProfit = np.asarray(Col)

query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
        f"FROM Profit_Loss_Long " \
        f"ORDER BY date DESC " \
        f"LIMIT 1200 "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
LongProfit = np.asarray(Col)

query = f"SELECT * " \
        f"FROM TotalFunds " \
        f"ORDER BY date DESC "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
data = np.asarray(Col)
TotalFunds = data[:, 1]
TFdat = data[:, 0]

query = f"SELECT * " \
        f"FROM Payout " \
        f"ORDER BY date DESC "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [list(item) for item in col]
list.reverse(Col)
data = np.asarray(Col)
Payout = data[:, 1]
POdat = data[:, 0]

query = f"SELECT date " \
        f"FROM Profit_Loss " \
        f"ORDER BY date DESC "
my_cursor.execute(query)
col = my_cursor.fetchall()
Col = [item for sublist in [list(i) for i in col] for item in sublist]
list.reverse(Col)
prdate = Col


# Profit Plots
dcn = len(prdate)
Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']

if st.sidebar.checkbox('Trading Module'):

    if st.checkbox('Assets moment profits'):
        # Assets moment profits
        st.header('Assets Moment Profits')
        i = 0
        for index in Cry_str:
            if dcn < 720:
                fig = plt.figure(i)
                plt.plot(prdate, TotalProfit[:, i])
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_TProfit")
                st.plotly_chart(fig)
                i += 1
            else:
                fig = plt.figure(i)
                plt.plot(prdate[-720:], TotalProfit[-720:, i])
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_TProfit")
                st.plotly_chart(fig)
                i += 1

        st.subheader('Total Port. M. Profits')
        if dcn < 720:
            fig = plt.figure(i)
            plt.plot(prdate, np.sum(TotalProfit, axis=1))
            plt.xlabel("date")
            plt.ylabel("return$")
            plt.title(f"TotalPort Profit")
            st.plotly_chart(fig)
        else:
            fig = plt.figure(i)
            plt.plot(prdate[-720:], np.sum(TotalProfit[-720:, :], axis=1))
            plt.xlabel("date")
            plt.ylabel("return$")
            plt.title(f"TotalPort Profit")
            st.plotly_chart(fig)

    # Assets and total cumulative profit
    if st.checkbox('Assets and Total Port. Cumulative Profit'):

        # Short cumsum
        st.header('Short Term Port.')
        i = 0
        for index in Cry_str:
            if dcn < 720:
                fig = plt.figure(i)
                plt.plot(prdate, np.cumsum(ShortProfit[:, i]))
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_cSProfit")
                st.plotly_chart(fig)
                i += 1
            else:
                fig = plt.figure(i)
                plt.plot(prdate[-720:], np.cumsum(ShortProfit[-720:, i]))
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_cSProfit")
                st.plotly_chart(fig)
                i += 1

        st.subheader('Total (Sum) Short Port. ')
        if dcn < 720:
            fig = plt.figure(i)
            plt.plot(prdate, np.cumsum(np.sum(ShortProfit, axis=1)))
            plt.xlabel("date")
            plt.ylabel("return$")
            plt.title(f"Short Port Total cProfit")
            st.plotly_chart(fig)
        else:
            fig = plt.figure(i)
            plt.plot(prdate[-720:], np.cumsum(np.sum(ShortProfit[-720:, :], axis=1)))
            plt.xlabel("date")
            plt.ylabel("return$")
            plt.title(f"Short Port Total cProfit")
            st.plotly_chart(fig)

        # Long cumsum
        st.header('Long Term Port.')
        i = 0
        for index in Cry_str:
            if dcn < 720:
                fig = plt.figure(i)
                plt.plot(prdate, np.cumsum(LongProfit[:, i]))
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_cLProfit")
                st.plotly_chart(fig)
                i += 1
            else:
                fig = plt.figure(i)
                plt.plot(prdate[-720:], np.cumsum(LongProfit[-720:, i]))
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_cLProfit")
                st.plotly_chart(fig)
                i += 1

        st.subheader('Total (Sum) Long Port. ')
        if dcn < 720:
            fig = plt.figure(i)
            plt.plot(prdate, np.cumsum(np.sum(LongProfit, axis=1)))
            plt.xlabel("date")
            plt.ylabel("return$")
            plt.title(f"Long Port Total cProfit")
            st.plotly_chart(fig)
        else:
            fig = plt.figure(i)
            plt.plot(prdate[-720:], np.cumsum(np.sum(LongProfit[-720:, :], axis=1)))
            plt.xlabel("date")
            plt.ylabel("return$")
            plt.title(f"Long Port Total cProfit")
            st.plotly_chart(fig)

        # Total Port cumsum
        st.header('Total Port.')
        i = 0
        for index in Cry_str:
            if dcn < 720:
                fig = plt.figure(i)
                plt.plot(prdate, np.cumsum(TotalProfit[:, i]))
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_cTProfit")
                st.plotly_chart(fig)
                i += 1
            else:
                fig = plt.figure(i)
                plt.plot(prdate[-720:], np.cumsum(TotalProfit[-720:, i]))
                plt.xlabel("date")
                plt.ylabel("return$")
                plt.title(f"{index}_cTProfit")
                st.plotly_chart(fig)
                i += 1

        st.subheader('Total Port. (Sum)')
        fig = plt.figure(i)
        plt.plot(prdate, np.cumsum(np.sum(TotalProfit, axis=1)))
        plt.xlabel("date")
        plt.ylabel("return$")
        plt.title(f"Total Port Total cProfit")
        st.plotly_chart(fig)

        # Alpha and Sharpe

        TFr = np.cumsum(np.sum(TotalProfit, axis=1)) + TotalFunds[0]  # TotalFunds[0]  depends on alpha/sharpe lookback (0=max lookback)
        TFprc = (TFr[1:]-TFr[0])/TFr[0]
        CCI = mdfll[-mt.floor((len(TFr)+24)/24):]
        CCr = (CCI[1:]-CCI[0])/CCI[0]
        Alpha = TFprc[-1]-CCr[-1]

        st.write('#### Total Port. Metrics')
        metdta = {'Alpha_%': Alpha, 'Sharpe': TFprc[-1]/(np.std((TFr[1:]-TFr[0:-1])/TFr[0:-1])*mt.sqrt(len(TFr))),
                  'Ret_%': TFprc[-1]}
        Pdmetdta = pandas.DataFrame(metdta, index=["TotalPort"])
        st.table(Pdmetdta)


# Funds Plots

if st.sidebar.checkbox('Funds M.M.'):
    st.header('Funds Management Module')

    # TotalFunds
    st.subheader('Total Funds (in Port.)')
    fig = plt.figure()
    plt.plot(TFdat, TotalFunds)
    plt.xlabel("date")
    plt.ylabel("value$")
    plt.title(f"TotalFunds")
    st.plotly_chart(fig)

    # Payout
    st.subheader('PayOut')
    fig = plt.figure()
    plt.bar(POdat, Payout)
    plt.xlabel("date")
    plt.ylabel("value$")
    plt.title(f"Payout")
    st.plotly_chart(fig)
