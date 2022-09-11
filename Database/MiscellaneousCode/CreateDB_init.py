# This module was used to populate the database with all the necessary information to start the algorithm

from alpha_vantage.timeseries import TimeSeries
import coinmarketcapapi
import coinmetrics
from binance.client import Client
from pytrends.request import TrendReq
from pytrends import dailydata
import pandas as pd
import numpy as np
import time
from datetime import date, timedelta, datetime
from HCtools import dateintpol, zerintpol
import mysql.connector as mysql

Database = mysql.connect(
    host="",
    user="",
    passwd="")

my_cursor = Database.cursor()

my_cursor.execute("CREATE DATABASE briareos")

my_cursor.execute("USE briareos")


# Database API feed

# World indices data (Alpha Vantage API)

my_cursor.execute(
    "CREATE TABLE worldindices (date DATE PRIMARY KEY, EWA FLOAT, EWT FLOAT, "
    "INDA FLOAT, EWZ FLOAT, EEM FLOAT, EWQ FLOAT,  EWM FLOAT, EWU FLOAT, "
    "EWG FLOAT, SPY FLOAT, EWC FLOAT,  MCHI FLOAT, VEA FLOAT, EIDO FLOAT, "
    "EWS FLOAT, VGK FLOAT, EWJ FLOAT, IYW FLOAT, VGT FLOAT, VDE FLOAT, ERUS FLOAT, "
    "XT FLOAT)")

ts = TimeSeries(key='TIU73LH54TAARJU2', output_format='pandas')

Windexstr = [['EWA', 'EWT', 'INDA', 'EWZ', 'EEM'], ['EWQ', 'EWM', 'EWU', 'EWG', 'SPY'],
             ['EWC', 'MCHI', 'VEA', 'EIDO', 'EWS'], ['VGK', 'EWJ', 'IYW', 'VGT', 'VDE'],
             ['ERUS', 'XT']]

Windex_name = ['EWA', 'EWT', 'INDA', 'EWZ', 'EEM', 'EWQ', 'EWM', 'EWU', 'EWG',
               'SPY', 'EWC', 'MCHI', 'VEA', 'EIDO', 'EWS', 'VGK', 'EWJ', 'IYW', 'VGT',
               'VDE', 'ERUS', 'XT']

length_Windex = len(Windexstr)
Wi_startdate = []
j = 0
for i in range(length_Windex):
    for index in Windexstr[i][:]:
        print(index)
        try:
            data, meta_data = ts.get_daily(symbol=index, outputsize='full')
        except:
            time.sleep(7)
            data, meta_data = ts.get_daily(symbol=index, outputsize='full')
        print(data)
        Crydt = np.flip(pd.DataFrame.to_numpy(data['4. close']))
        Wi_dts = data.index.sort_values(True)
        Wi_date = (Wi_dts[0][:].to_pydatetime())
        Wi_ind = [index for index, value in enumerate(Wi_date) if value < (datetime.today() - timedelta(days=750))]
        Wi_intdate = Wi_dts[0][Wi_ind[-1]:]
        Wi_startdate.append(Wi_date[Wi_ind[-1]].date())
        print(Wi_startdate)
        Crydata = Crydt[Wi_ind[-1]:]
        FullDate = pd.date_range(Wi_startdate[j], (date.today() - timedelta(days=1)))
        Cry_zrdata = zerintpol(Crydata)
        vars()[f"{Windex_name[j]}_l"] = zerintpol(dateintpol(FullDate, Wi_intdate, Cry_zrdata))
        j += 1
    time.sleep(60)

j = 0
for i in range(length_Windex):
    for index in Windexstr[i][:]:
        price_data = vars()[f"{Windex_name[j]}_l"]
        vars()[f"{Windex_name[j]}"] = price_data[-750:]
        j += 1

Wi_record = "INSERT IGNORE INTO worldindices (date, EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, SPY, EWC," \
            " MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT, VDE, ERUS, XT) VALUES (%s, %s, %s, %s, %s, %s, %s," \
            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

Fulldate = pd.date_range((date.today() - timedelta(days=750)), (date.today() - timedelta(days=1)))
for j in range(750):
    valus = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
    for i in range(len(Windex_name)):
        index = vars()[f"{Windex_name[i]}"]
        valus += (float(index[j]),)
    my_cursor.execute(Wi_record, valus)

Database.commit()


# Crypto Market Index (CMC API) (Total MarketCap excluding BTC)
# TODO: cci30 : CCi30 scaling not tested

cmc = coinmarketcapapi.CoinMarketCapAPI('882524ed-0cbc-4507-85eb-71baca5ff3c3', sandbox=False)

my_cursor.execute("CREATE TABLE CryptoIndex (date DATE PRIMARY KEY, price FLOAT)")

CCi30_xls = pd.read_excel(r'C:\Users\Machine1\Desktop\HCdeptBriareos\Database\Historical_DB_Data\cci30.xls',
                          index_col="Date")

cci30 = CCi30_xls[-750:]

cci30_dts = cci30.index
cci30_date = (cci30_dts.to_pydatetime())
cci30_ind = [index for index, value in enumerate(cci30_date) if value < (datetime.today() - timedelta(days=750))]
cci30_intdate = cci30_dts[cci30_ind[-1]:]
cci30_startdate = (cci30_date[cci30_ind[-1]].date())
print(cci30_startdate)
Fulldate = pd.date_range(cci30_startdate, (date.today() - timedelta(days=1)))
data = dateintpol(Fulldate, cci30_intdate, zerintpol(pd.DataFrame.to_numpy(cci30['Price'])))
CCi30 = data[-750:]


try:
    indx = cmc.global_metrics_quotes_latest()
    CIprice = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000
except:
    time.sleep(7)
    indx = cmc.global_metrics_quotes_latest()
    CIprice = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000

CMC = np.ndarray.tolist(CIprice/float(CCi30[-1])*np.asarray(CCi30))

CCi_record = "INSERT INTO CryptoIndex (date, price) VALUES (%s, %s ) "
for j in range(750):
    CCidate = datetime.strftime(Fulldate[j], "%Y-%m-%d")
    prce = CMC[j]
    CCidata = float(prce)
    values = (CCidate, CCidata)
    my_cursor.execute(CCi_record, values)

Database.commit()


# Crypto Network data (CoinMetrics API)

my_cursor.execute(
    "CREATE TABLE btcMD (date DATE PRIMARY KEY, AdrActCnt FLOAT, DiffMean FLOAT, TxCnt FLOAT, TxTfrValMedUSD FLOAT)")
my_cursor.execute(
    "CREATE TABLE ethMD (date DATE PRIMARY KEY, AdrActCnt FLOAT, DiffMean FLOAT, TxCnt FLOAT, TxTfrValMedUSD FLOAT)")
my_cursor.execute(
    "CREATE TABLE xlmMD (date DATE PRIMARY KEY, AdrActCnt FLOAT, TxCnt FLOAT, TxTfrValMedUSD FLOAT)")
my_cursor.execute(
    "CREATE TABLE xmrMD (date DATE PRIMARY KEY, DiffMean FLOAT, TxCnt FLOAT)")
my_cursor.execute(
    "CREATE TABLE xrpMD (date DATE PRIMARY KEY, AdrActCnt FLOAT, TxCnt FLOAT, TxTfrValMedUSD FLOAT)")
my_cursor.execute(
    "CREATE TABLE linkMD (date DATE PRIMARY KEY, AdrActCnt FLOAT, TxCnt FLOAT, TxTfrValMedUSD FLOAT)")
my_cursor.execute(
    "CREATE TABLE neoMD (date DATE PRIMARY KEY, AdrActCnt FLOAT, TxCnt FLOAT, TxTfrValMedUSD FLOAT)")

Crypto_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo']
Cry_Metrics = ['AdrActCnt', 'DiffMean', 'TxCnt', 'TxTfrValMedUSD']
Fulldate = pd.date_range((date.today() - timedelta(days=750)), (date.today() - timedelta(days=1)))
cm = coinmetrics.Community()
for crypto in Crypto_str:
    for metric in Cry_Metrics:
        print(crypto)
        print(metric)
        old_dt = date.today() - timedelta(days=750)
        yesterday = date.today() - timedelta(days=1)
        yesterday_date = yesterday.strftime("%Y-%m-%d")
        old_date = old_dt.strftime("%Y-%m-%d")
        if (crypto == 'xlm' or crypto == 'xrp' or crypto == 'link' or crypto == 'neo') and metric == 'DiffMean':
            continue
        elif crypto == 'xmr' and (metric == 'AdrActCnt' or metric == 'TxTfrValMedUSD'):
            continue
        else:
            try:
                Cry_dt = cm.get_asset_metric_data(crypto, metric, old_date, yesterday_date)
            except:
                time.sleep(10)
                Cry_dt = cm.get_asset_metric_data(crypto, metric, old_date, yesterday_date)
            print(Cry_dt)
            Cry_pandas_data = coinmetrics.cm_to_pandas(Cry_dt)
            dte = pd.to_datetime(Cry_pandas_data.index).tz_convert(None)
            print(Cry_pandas_data)
            vars()[f"{crypto}_{metric}"] = zerintpol(dateintpol(Fulldate,dte,pd.DataFrame.to_numpy(Cry_pandas_data)))
        print(vars()[f"{crypto}_{metric}"])


for j in range(750):
    for crypto in Crypto_str:
        metrc = 'date'
        values = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
        s = '%s'
        for metric in Cry_Metrics:
            if (crypto == 'xlm' or crypto == 'xrp' or crypto == 'link' or crypto == 'neo') and metric == 'DiffMean':
                continue
            elif crypto == 'xmr' and (metric == 'AdrActCnt' or metric == 'TxTfrValMedUSD'):
                continue
            else:
                valus = vars()[f"{crypto}_{metric}"]
                values += (float(valus[j]),)
                metrc += f', {metric}'
                s += ', %s'

        MD_record = f"INSERT INTO {crypto}MD ({metrc}) VALUES ({s})"
        my_cursor.execute(MD_record, values)

Database.commit()


# Google Trends data

my_cursor.execute(
    f"CREATE TABLE GT_searches (date DATE PRIMARY KEY, Bitcoin FLOAT, BTC FLOAT, ETH FLOAT, Ethereum FLOAT, "
    f"Monero FLOAT, Ripple_crypto FLOAT, Stellar_Lumens FLOAT, ChainLink FLOAT, NEO_price FLOAT, XRP FLOAT)")

pytrends = TrendReq(hl='en-US', tz=0, retries=10, backoff_factor=0.5)

GT_str = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple crypto', 'Stellar Lumens', 'ChainLink', 'NEO price',
          'XRP']
NGT = len(GT_str)

for search in GT_str:
    print(search)
    yester = date.today() - timedelta(days=1)
    past = date.today() - timedelta(days=780)
    try:
        GT_dtaO = dailydata.get_daily_data(search, past.year, past.month, yester.year, yester.month)
    except:
        time.sleep(15)
        GT_dtaO = dailydata.get_daily_data(search, past.year, past.month, yester.year, yester.month)
    vars()[f"{search}"] = zerintpol(
        pd.DataFrame.to_numpy(GT_dtaO[f"{search}"][-750:]))
    # data requirements
    print(vars()[f"{search}"])
    time.sleep(30)

Fulldate = pd.date_range((date.today() - timedelta(days=750)), (date.today() - timedelta(days=1)))

GT_dbname = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple_crypto', 'Stellar_Lumens', 'ChainLink', 'NEO_price',
             'XRP']

for j in range(750):
    Cry_values = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
    Cry_col = 'date'
    s = '%s'
    i = 0
    for search in GT_str:
        volume = vars()[f"{search}"]
        Cry_values += (float(volume[j]),)
        s += ', %s'
        Cry_col += f', {GT_dbname[i]}'
        i += 1
    CryM_record = f"INSERT INTO GT_searches ({Cry_col}) VALUES ({s})"
    my_cursor.execute(CryM_record, Cry_values)

Database.commit()


# Crypto Price data (Binance API)

client = Client("",
                "")

Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']

# Hourly data

for crypto in Cry_str:
    my_cursor.execute(f"CREATE TABLE {crypto}h (date DATETIME PRIMARY KEY, open FLOAT, high FLOAT, low FLOAT, close "
                      f"FLOAT, volume FLOAT )")

for crypto in Cry_str:
    print(crypto)
    data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1HOUR, "63 days ago UTC")
    print(data)
    data_np = np.asarray(data)
    vars()[f"{crypto}h"] = data_np[-1501:-1, 0:6]
    print(vars()[f"{crypto}h"])

for crypto in Cry_str:
    for j in range(1500):
        dte = vars()[f"{crypto}h"][j, 0]
        Cdate = [datetime.fromtimestamp(int(dte) / 1000)]
        pdata = [float(i) for i in vars()[f"{crypto}h"][j, 1:6]]
        valus = [Cdate, pdata]
        values = tuple([item for sublist in valus for item in sublist])
        record = f"INSERT INTO {crypto}h ( date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
        my_cursor.execute(record, values)

Database.commit()

# Daily data
# TODO: update excel data (expires 18-06-2020)

for crypto in Cry_str:
    my_cursor.execute(f"CREATE TABLE {crypto}d ( date DATE PRIMARY KEY, open FLOAT, high FLOAT, low FLOAT, close "
                      f"FLOAT, volume FLOAT )")

for crypto in Cry_str:
    print(crypto)
    data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, "751 days ago UTC")
    print(data)
    data_np = np.asarray(data)
    vars()[f"{crypto}d"] = data_np[-751:-1, 0:6]
    print(vars()[f"{crypto}d"])

inc_cry = ['XLMUSD', 'XMRUSD', 'XRPUSD', 'LINKUSD']

for crypto in inc_cry:
    xls_dta = pd.read_excel(fr'C:\Users\Machine1\Desktop\HCdeptBriareos\Database\Historical_DB_Data\{crypto}.xls',
                            index_col="Date")
    xls_data = xls_dta.loc[date.strftime(date.today() - timedelta(days=750), "%Y-%m-%d"):
                           date.strftime(date.today() - timedelta(days=len(vars()[f"{crypto}Td"])), "%Y-%m-%d")]
    cci30_dts = xls_data.index[:]
    vars()[f"{crypto}Td_dates"] = (cci30_dts.to_pydatetime())
    vars()[f"{crypto}Tdxls"] = pd.DataFrame.to_numpy(xls_data.iloc[:, 0:5])

for crypto in Cry_str:
    if len(vars()[f"{crypto}d"]) < 750:
        for j in range(750):
            if (750 - len(vars()[f"{crypto}d"]) - 1) > 0 and j < (750 - len(vars()[f"{crypto}d"])):
                Cdate = [vars()[f"{crypto}d_dates"][j]]
                pdata = [float(i) for i in vars()[f"{crypto}dxls"][j]]
                valus = [Cdate, pdata]
                values = tuple([item for sublist in valus for item in sublist])
                record = f"INSERT INTO {crypto}d ( date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
                my_cursor.execute(record, values)
            else:
                j = j - (750 - len(vars()[f"{crypto}d"]))
                dte = vars()[f"{crypto}d"][j, 0]
                Cdate = [datetime.fromtimestamp(int(dte) / 1000)]
                pdata = [float(i) for i in vars()[f"{crypto}d"][j, 1:6]]
                valus = [Cdate, pdata]
                values = tuple([item for sublist in valus for item in sublist])
                record = f"INSERT INTO {crypto}d ( date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
                my_cursor.execute(record, values)
    else:
        for j in range(750):
            dte = vars()[f"{crypto}d"][j, 0]
            Cdate = [datetime.fromtimestamp(int(dte) / 1000)]
            pdata = [float(i) for i in vars()[f"{crypto}d"][j, 1:6]]
            valus = [Cdate, pdata]
            values = tuple([item for sublist in valus for item in sublist])
            record = f"INSERT INTO {crypto}d ( date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
            my_cursor.execute(record, values)

Database.commit()


# Briareos Modules output data tables

# Optimization Module (System 1)

# Short-Term Trading Opt.

Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']

dta = ['SvarMACD', 'SvarOBV', 'SvarADL', 'SvarOSC', 'SStrt']

for crypto in Cry_str:
    for data in dta:
        if data == 'SvarOSC':
            my_cursor.execute(
                f"CREATE TABLE {crypto}_{data} (date DATETIME PRIMARY KEY, alpha FLOAT, a INT, b INT)")
        elif data == 'SStrt':
            my_cursor.execute(
                f"CREATE TABLE {crypto}_{data} (date DATE PRIMARY KEY, alpha FLOAT, a INT, b INT, c INT, d INT,"
                f" e INT, f INT, g INT, h INT, i INT, j INT, k INT, l INT, m INT, n INT)")
        else:
            my_cursor.execute(f"CREATE TABLE {crypto}_{data} (date DATE PRIMARY KEY, alpha FLOAT, a INT, b INT,"
                              f" c INT)")

Database.commit()

# Long-Term Trading Opt.

dta = ['LvarMACD', 'LvarOBV', 'LvarADL', 'LvarOSC', 'LStrt']

for crypto in Cry_str:
    for data in dta:
        if data == 'LvarOSC':
            my_cursor.execute(
                f"CREATE TABLE {crypto}_{data} (date DATETIME PRIMARY KEY, alpha FLOAT, a INT, b INT)")
        elif data == 'LStrt':
            my_cursor.execute(
                f"CREATE TABLE {crypto}_{data} (date DATETIME PRIMARY KEY, alpha FLOAT, a INT, b INT, c INT, d INT,"
                f" e INT, f INT, g INT, h INT, i INT, j INT, k INT, l INT, m INT, n INT, o INT, p INT, q INT"
                f", r INT)")
        else:
            my_cursor.execute(f"CREATE TABLE {crypto}_{data} (date DATETIME PRIMARY KEY, alpha FLOAT, a INT, b INT,"
                              f" c INT)")

my_cursor.execute(f"CREATE TABLE Rt (date DATETIME PRIMARY KEY, alpha FLOAT, BTC INT, ETH INT, XLM INT, XMR INT,"
                  f" XRP INT, LINK INT, NEO INT)")
Database.commit()

# Predictions and Portfolio Management Module (System 2)

# Predictions Module

my_cursor.execute("CREATE TABLE Predictions (date DATE PRIMARY KEY, BTCAdc FLOAT, BTCdiff FLOAT, BTCtxc FLOAT,"
                  " BTCtxv FLOAT, ETHAdc FLOAT, ETHdiff FLOAT, ETHtxc FLOAT, ETHtxv FLOAT, XLMAdc FLOAT, XLMtxc FLOAT,"
                  " XLMtxv FLOAT, XMRdiff FLOAT, XMRtxc FLOAT, XRPAdc FLOAT, XRPtxc FLOAT, XRPtxv FLOAT, LINKAdc FLOAT,"
                  " LINKtxc FLOAT, LINKtxv FLOAT, NEOAdc FLOAT, NEOtxc FLOAT, NEOtxv FLOAT, BitcoinGT FLOAT,"
                  " BTCGT FLOAT, ETHGT FLOAT, EthereumGT FLOAT, MoneroGT FLOAT, Ripple_cryptoGT FLOAT,"
                  " Stellar_LumensGT FLOAT, ChainLinkGT FLOAT, NEO_priceGT FLOAT, XRPGT FLOAT,"
                  " EWA FLOAT, EWT FLOAT, INDA FLOAT, EWZ FLOAT, EEM FLOAT, EWQ FLOAT, EWM FLOAT, EWU FLOAT, EWG FLOAT,"
                  " SPY FLOAT, EWC FLOAT, MCHI FLOAT, VEA FLOAT, EIDO FLOAT, EWS FLOAT, VGK FLOAT, EWJ FLOAT,"
                  " IYW FLOAT, VGT FLOAT, VDE FLOAT, ERUS FLOAT, XT FLOAT, BTC FLOAT, ETH FLOAT, XLM FLOAT,"
                  " XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT, CryptoIndex FLOAT, CryptoIndexR FLOAT, BTCR FLOAT,"
                  " ETHR FLOAT, XLMR FLOAT, XMRR FLOAT, XRPR FLOAT, LINKR FLOAT, NEOR FLOAT)")
Database.commit()


# Portfolio Management Module

my_cursor.execute(f"CREATE TABLE PortfolioOptS (date DATE PRIMARY KEY, SPortstd FLOAT, SPort FLOAT, BTCSP FLOAT,"
                  f" ETHSP FLOAT, XLMSP FLOAT, XMRSP FLOAT, XRPSP FLOAT, LINKSP FLOAT, NEOSP FLOAT)")

my_cursor.execute(f"CREATE TABLE PortfolioOptL (date DATE PRIMARY KEY, LPortstd FLOAT, LPort FLOAT, BTCLP FLOAT,"
                  f" ETHLP FLOAT, XLMLP FLOAT, XMRLP FLOAT, XRPLP FLOAT, LINKLP FLOAT, NEOLP FLOAT)")

Database.commit()


# Trading Module (System 3)

# Short-Term Trading

my_cursor.execute(f"CREATE TABLE ShortTradingSig (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE ShortTradingSigR (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT)")

Database.commit()

record = "INSERT IGNORE INTO ShortTradingSig VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
recordR = "INSERT IGNORE INTO ShortTradingSigR VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
nowr = datetime.now()
dat = datetime(nowr.year, nowr.month, nowr.day, nowr.hour)
val = [float(i) for i in [0, 0, 0, 0, 0, 0, 0]]
valR = [float(i) for i in [0, 0, 0, 0, 0, 0, 0]]
valu = [dat] + val
valuR = [dat] + valR
value = tuple(valu)
valueR = tuple(valuR)
my_cursor.execute(record, value)
my_cursor.execute(recordR, valueR)
Database.commit()

# Long-Term Trading

my_cursor.execute(f"CREATE TABLE LongTradingSig (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE LongTradingSigR (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT)")

Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
for cry in Cry_str:
    my_cursor.execute(f"CREATE TABLE {cry}_RegressTpredi (date DATE PRIMARY KEY, price FLOAT)")

Database.commit()

record = "INSERT IGNORE INTO LongTradingSig VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
recordR = "INSERT IGNORE INTO LongTradingSigR VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
nowr = datetime.now()
dat = datetime(nowr.year, nowr.month, nowr.day, nowr.hour)
val = [float(i) for i in [0, 0, 0, 0, 0, 0, 0]]
valR = [float(i) for i in [0, 0, 0, 0, 0, 0, 0]]
valu = [dat] + val
valuR = [dat] + valR
value = tuple(valu)
valueR = tuple(valuR)
my_cursor.execute(record, value)
my_cursor.execute(recordR, valueR)
Database.commit()


# TotalFunds

my_cursor.execute(f"CREATE TABLE totalfunds (date DATETIME PRIMARY KEY, value FLOAT)")

Database.commit()


# Miscellaneous

my_cursor.execute(f"CREATE TABLE Miscellaneous (t FLOAT, MinPort FLOAT, SavRate FLOAT,"
                  f" Inception_Date DATE)")
Database.commit()

record = "INSERT INTO Miscellaneous (t, MinPort, SavRate, Inception_Date) VALUES ( %s, %s, %s, %s)"
values = (35, 450, 0.3, date.today()+timedelta(days=1))  # MinPort related to inception Portfolio values
my_cursor.execute(record, values)
Database.commit()


# Module Execution Comfirmation

my_cursor.execute(f"CREATE TABLE ExecutionCom (payout INT, adjust INT)")
Database.commit()
record = " INSERT INTO ExecutionCom VALUES( %s, %s)"
values = (0, 0)
my_cursor.execute(record, values)
Database.commit()


# Trading data

my_cursor.execute(f"CREATE TABLE BuyPrices (BTC FLOAT, ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT,"
                  f" NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE BuyPrices_Short (BTC FLOAT, ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT,"
                  f" NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE BuyPrices_Long (BTC FLOAT, ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT,"
                  f" NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE Profit_Loss (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE Profit_Loss_Short (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE Profit_Loss_Long (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT)")

my_cursor.execute(f"CREATE TABLE Port_values (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT, USDT FLOAT)")

my_cursor.execute(f"CREATE TABLE Port_values_short (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT, USDT FLOAT)")

my_cursor.execute(f"CREATE TABLE Port_values_long (date DATETIME PRIMARY KEY, BTC FLOAT,"
                  f" ETH FLOAT, XLM FLOAT, XMR FLOAT, XRP FLOAT, LINK FLOAT, NEO FLOAT, USDT FLOAT)")

my_cursor.execute(f"CREATE TABLE PayOut (date DATETIME PRIMARY KEY, value FLOAT)")

Database.commit()

# backtest init Funds values
# TODO: Will have to be changed by actual Exchange init. Port Values

record = " INSERT INTO Port_values VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
srecord = " INSERT INTO Port_values_short VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
lrecord = " INSERT INTO Port_values_long VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
precord = " INSERT INTO PayOut VALUES ( %s, %s)"
nowr = datetime.now()
data = np.zeros((1, 8))[0]
data[-1] = 500
values = [nowr] + np.ndarray.tolist(data)
values = tuple(values)
pvals= (nowr, 0)
my_cursor.execute(record, values)
my_cursor.execute(srecord, values)
my_cursor.execute(lrecord, values)
my_cursor.execute(precord, pvals)

record = " INSERT INTO BuyPrices VALUES ( %s, %s, %s, %s, %s, %s, %s)"
srecord = " INSERT INTO BuyPrices_Short VALUES ( %s, %s, %s, %s, %s, %s, %s)"
lrecord = " INSERT INTO BuyPrices_Long VALUES ( %s, %s, %s, %s, %s, %s, %s)"
data = np.zeros((1, 7))[0]
values = tuple(data)
my_cursor.execute(record, values)
my_cursor.execute(srecord, values)
my_cursor.execute(lrecord, values)

record = " INSERT INTO profit_loss VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
srecord = " INSERT INTO profit_loss_short VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
lrecord = " INSERT INTO profit_loss_long VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
data = [datetime.now()] + np.ndarray.tolist(np.zeros((1, 7))[0])
values = tuple(data)
my_cursor.execute(record, values)
my_cursor.execute(srecord, values)
my_cursor.execute(lrecord, values)

Database.commit()


# Exception Management

my_cursor.execute(f"CREATE TABLE Exception_Terminal (PK CHAR(10) PRIMARY KEY, TradingData TEXT, DailyData TEXT,"
                  f" DTRecovery TEXT, TOptModule TEXT, Pred_PMM TEXT, Trad_OEM TEXT, Bri_Terminal TEXT)")

MTrecord = " INSERT INTO Exception_Terminal VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
values = ("Status", "Null", "Null", "Null", "Null", "Null", "Null", "Null")
my_cursor.execute(MTrecord, values)
values = ("Terminal", "Null", "Null", "Null", "Null", "Null", "Null", "Null")
my_cursor.execute(MTrecord, values)
Database.commit()
