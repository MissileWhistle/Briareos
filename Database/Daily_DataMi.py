# This module gathers daily data used by the algorithm by accessing API's of several free market data providers and
# others like Google and CoinMetrics

from alpha_vantage.timeseries import TimeSeries
import coinmarketcapapi
import coinmetrics
from binance.client import Client
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import time
from datetime import date, timedelta, datetime
from HCtools import zerintpol
import mysql.connector as mysql
import sys


def DailyData():
    Excp = 0

    Database = mysql.connect(
        host="",
        user="",
        passwd="")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    # Database API feed

    MTsrecord = 'UPDATE Exception_Terminal SET DailyData = "Running" WHERE PK = "Status" '
    my_cursor.execute(MTsrecord)
    nowdat = datetime.now()
    Term = (f"{nowdat}\n"
            f"\n"
            f"Daily Data query Module Starting ...\n"
            f"\n"
            f"World Indices query Starting ...\n"
            f"\n")

    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    # World indices data (Alpha Vantage API)

    ts = TimeSeries(key='TIU73LH54TAARJU2', output_format='pandas')

    Windexstr = [['EWA', 'EWT', 'INDA', 'EWZ', 'EEM'], ['EWQ', 'EWM', 'EWU', 'EWG', 'SPY'],
                 ['EWC', 'MCHI', 'VEA', 'EIDO', 'EWS'], ['VGK', 'EWJ', 'IYW', 'VGT', 'VDE'],
                 ['ERUS', 'XT', 'IAU', 'PICK', 'ICLN'], ['ITA']]

    Nindex = 0
    length_Windex = len(Windexstr)
    for j in range(length_Windex):
        Nindex += len(Windexstr[j][:])

    WIprice = np.zeros(Nindex)
    j = 0
    for i in range(length_Windex):
        for index in Windexstr[i][:]:
            print(index)
            try:
                data, meta_data = ts.get_quote_endpoint(index)
                WIprice[j] = pd.DataFrame.to_numpy(data['05. price'])
            except:
                try:
                    time.sleep(3)
                    data, meta_data = ts.get_quote_endpoint(index)
                    WIprice[j] = pd.DataFrame.to_numpy(data['05. price'])
                except Exception as e:
                    WIprice[j] = 0

                    Termy = (f"{index} problematic\n"
                             f"\n"
                             f"Exception:\n"
                             f"\n"
                             f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                             f"{e}\n"
                             f"\n")
                    Term = Term + Termy
                    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
                    my_cursor.execute(MTrecord)
                    Database.commit()
                    Excp = 1

            print(WIprice[j])
            j += 1
        time.sleep(61)
    print(WIprice)

    Wi_record = "INSERT INTO worldindices (date, EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, SPY, EWC, " \
                "MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT, VDE, ERUS, XT, IAU, PICK, ICLN, ITA) VALUES (%s, " \
                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    Windex_name = ['EWA', 'EWT', 'INDA', 'EWZ', 'EEM', 'EWQ', 'EWM', 'EWU', 'EWG',
                   'SPY', 'EWC', 'MCHI', 'VEA', 'EIDO', 'EWS', 'VGK', 'EWJ', 'IYW', 'VGT',
                   'VDE', 'ERUS', 'XT', 'IAU', 'PICK', 'ICLN', 'ITA']

    valus = (date.strftime(date.today() - timedelta(days=1), "%Y-%m-%d"),)
    for i in range(len(Windex_name)):
        index = WIprice[i]
        if index == 0 or index == 'NaN':
            query = f"SELECT {Windex_name[i]} " \
                    f"FROM worldindices " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            index = my_cursor.fetchall()[0][0]

        valus += (float(index),)
    my_cursor.execute(Wi_record, valus)

    Database.commit()

    # Stocks data (Alpha Vantage API)


    Termy = (f"Stocks Data query Starting...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    ts = TimeSeries(key='TIU73LH54TAARJU2', output_format='pandas')

    Windexstr = [['TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM'], ['AMZN', 'FB', 'HYMTF', 'VWAGY']]

    Nindex = 0
    length_Windex = len(Windexstr)
    for j in range(length_Windex):
        Nindex += len(Windexstr[j][:])

    WIprice = np.zeros(Nindex)
    j = 0
    for i in range(length_Windex):
        for index in Windexstr[i][:]:
            print(index)
            try:
                data, meta_data = ts.get_quote_endpoint(index)
                WIprice[j] = pd.DataFrame.to_numpy(data['05. price'])
            except:
                try:
                    time.sleep(3)
                    data, meta_data = ts.get_quote_endpoint(index)
                    WIprice[j] = pd.DataFrame.to_numpy(data['05. price'])
                except Exception as e:
                    WIprice[j] = 0

                    Termy = (f"{index} problematic\n"
                             f"\n"
                             f"Exception:\n"
                             f"\n"
                             f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                             f"{e}\n"
                             f"\n")
                    Term = Term + Termy
                    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
                    my_cursor.execute(MTrecord)
                    Database.commit()
                    Excp = 1

            print(WIprice[j])
            j += 1
        time.sleep(61)
    print(WIprice)

    Wi_record = "INSERT INTO Stocks (date, TSLA, MSFT, GOOGL, AAPL, IBM, AMZN, FB, HYMTF, VWAGY) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    Windex_name = ['TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM', 'AMZN', 'FB', 'HYMTF', 'VWAGY']

    valus = (date.strftime(date.today() - timedelta(days=1), "%Y-%m-%d"),)
    for i in range(len(Windex_name)):
        index = WIprice[i]
        if index == 0 or index == 'NaN':
            query = f"SELECT {Windex_name[i]} " \
                    f"FROM Stocks " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            index = my_cursor.fetchall()[0][0]
        valus += (float(index),)
    my_cursor.execute(Wi_record, valus)

    Database.commit()

    # Crypto Market Index (CMC API(Total Market Cap excluding BTC))

    Termy = (f"Crypto Index Data query Starting...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    cmc = coinmarketcapapi.CoinMarketCapAPI('882524ed-0cbc-4507-85eb-71baca5ff3c3', sandbox=False)

    try:
        indx = cmc.global_metrics_quotes_latest()
        CIprice = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000
    except:
        try:
            time.sleep(3)
            indx = cmc.global_metrics_quotes_latest()
            CIprice = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000
        except Exception as e:
            CIprice = 0

            Termy = (f"Crypto Index problematic\n"
                     f"\n"
                     f"Exception:\n"
                     f"\n"
                     f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                     f"{e}\n"
                     f"\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()
            Excp = 1

    print(CIprice)

    CCi_record = "INSERT IGNORE INTO CryptoIndex (date, price) VALUES (%s, %s)"

    CCidate = date.strftime(date.today() - timedelta(days=1), "%Y-%m-%d")

    if CIprice == 0 or CIprice == 'NaN':
        query = f"SELECT price " \
                f"FROM CryptoIndex " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        CIprice = my_cursor.fetchall()[0][0]

    values = (CCidate, float(CIprice))
    my_cursor.execute(CCi_record, values)

    Database.commit()

    # Crypto Network data (CoinMetrics API)

    Termy = (f"Crypto Network Data query Starting ...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

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
                   ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'TxTfrValMedNtv', 'TxTfrValMeanNtv', 'FeeMeanNtv',
                    'DiffMean',
                    'BlkSizeMeanByte'],
                   ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'NDF', 'FeeMeanUSD', 'FeeMedNtv', 'BlkSizeMeanByte'],
                   ['TxCnt', 'AdrActCnt', 'TxTfrValAdjNtv', 'IssContUSD', 'FeeMeanNtv', 'DiffMean', 'BlkSizeMeanByte']]

    cm = coinmetrics.Community()
    i=0
    for crypto in Crypto_str:
        for metric in Cry_Metrics[i]:
            yesterday = date.today() - timedelta(days=1)
            yesterday_date = yesterday.strftime("%Y-%m-%d")
            print(crypto)
            print(metric)
            try:
                Cry_dt = cm.get_asset_metric_data(crypto, metric, yesterday_date, yesterday_date)
                Cry_pandas_data = coinmetrics.cm_to_pandas(Cry_dt)
                Cry_data = pd.DataFrame.to_numpy(Cry_pandas_data)
                if len(Cry_data) == 0:
                    vars()[f"{crypto}_{metric}"] = 0
                else:
                    vars()[f"{crypto}_{metric}"] = Cry_data
            except:
                try:
                    time.sleep(3)
                    Cry_dt = cm.get_asset_metric_data(crypto, metric, yesterday_date, yesterday_date)
                    Cry_pandas_data = coinmetrics.cm_to_pandas(Cry_dt)
                    Cry_data = pd.DataFrame.to_numpy(Cry_pandas_data)
                    if len(Cry_data) == 0:
                        vars()[f"{crypto}_{metric}"] = 0
                    else:
                        vars()[f"{crypto}_{metric}"] = Cry_data
                except Exception as e:
                    vars()[f"{crypto}_{metric}"] = 0
                    Termy = (f"{crypto} {metric} problematic\n"
                             f"\n"
                             f"Exception:\n"
                             f"\n"
                             f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                             f"{e}\n"
                             f"\n")
                    Term = Term + Termy
                    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
                    my_cursor.execute(MTrecord)
                    Database.commit()
                    Excp = 1
        i+=1

    i=0
    for crypto in Crypto_str:
        metrc = 'date'
        values = (date.strftime(date.today() - timedelta(days=1), "%Y-%m-%d"),)
        s = '%s'
        for metric in Cry_Metrics[i]:
            valus = vars()[f"{crypto}_{metric}"]
            if valus == 0 or np.isnan(valus[0]) == 1:
                query = f"SELECT {metric} " \
                        f"FROM {crypto}MD " \
                        f"ORDER BY date DESC " \
                        f"LIMIT 1 "
                my_cursor.execute(query)
                valus = my_cursor.fetchall()[0][0]
                Termy = (f"{crypto} {metric} problematic (empty or zero)\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()
                Excp = 1
            values += (float(valus),)
            metrc += f', {metric}'
            s += ', %s'
        i += 1
        MD_record = f"INSERT IGNORE INTO {crypto}MD ({metrc}) VALUES ({s})"
        my_cursor.execute(MD_record, values)

    Database.commit()

    # Google Trends data

    Termy = (f"Google Trends Data query Starting ...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    pytrends = TrendReq(hl='en-US', tz=0, retries=10, backoff_factor=0.5)

    GT_str = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple crypto', 'Stellar Lumens', 'ChainLink', 'NEO price',
              'XRP', 'blockchain', 'cryptocurrency', 'altcoin', 'Smart Contract', 'Binance']
    NGT = len(GT_str)

    query = f"SELECT Bitcoin, BTC, ETH, Ethereum, Monero, Ripple_crypto, Stellar_Lumens, ChainLink, NEO_price, XRP, " \
            f"blockchain, cryptocurrency, altcoin, Smart_Contract, Binance "\
            f"FROM GT_searches " \
            f"ORDER BY date DESC " \
            f"LIMIT 50 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    Col = [list(item) for item in col]
    GT_data = np.asarray(Col)

    past = datetime.now() - timedelta(days=7)
    yesterday = datetime.now()
    exerr = 0

    i = 0
    for search in GT_str:
        print(search)
        try:
            GT_dtaP = pytrends.get_historical_interest([search], cat=7, year_start=past.year, month_start=past.month,
                                                       day_start=past.day, hour_start=0, year_end=yesterday.year,
                                                       month_end=yesterday.month, day_end=yesterday.day,
                                                       hour_end=yesterday.hour, gprop='')

            vars()[f"{search}"] = zerintpol(
                pd.DataFrame.to_numpy(GT_dtaP[f"{search}"]))
        except:
            try:
                time.sleep(15)
                GT_dtaP = pytrends.get_historical_interest([search], cat=7, year_start=past.year,
                                                           month_start=past.month,
                                                           day_start=past.day, hour_start=0, year_end=yesterday.year,
                                                           month_end=yesterday.month, day_end=yesterday.day,
                                                           hour_end=yesterday.hour, gprop='')

                vars()[f"{search}"] = zerintpol(
                    pd.DataFrame.to_numpy(GT_dtaP[f"{search}"]))
            except Exception as e:
                exerr = 1
                Termy = (f"{search} problematic\n"
                         f"\n"
                         f"Exception:\n"
                         f"\n"
                         f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                         f"{e}\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()
                Excp = 1
        i += 1

    j = 0
    new_data = np.zeros(len(GT_data[0]))
    for search in GT_str:
        if exerr == 1:
            new_data[j] = GT_data[-1, j]
        else:
            pst = np.mean(vars()[f"{search}"][-48:-24])
            dbpast = GT_data[-1, j]
            xcor = dbpast / pst
            if np.isnan(xcor) == 1 or np.isinf(xcor) == 1:
                new_data[j] = GT_data[-1, j]
            else:
                new = np.mean(vars()[f"{search}"][-24:]) * xcor
                new_data[j] = new
        j += 1

    GT_dbname = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple_crypto', 'Stellar_Lumens', 'ChainLink', 'NEO_price',
                 'XRP', 'blockchain', 'cryptocurrency', 'altcoin', 'Smart_Contract', 'Binance' ]

    Cry_values = (date.strftime((date.today() - timedelta(days=1)), "%Y-%m-%d"),)
    Cry_col = 'date'
    s = '%s'
    for i in range(NGT):
        volume = new_data[i]
        Cry_values += (float(volume),)
        s += ', %s'
        Cry_col += f', {GT_dbname[i]}'

    CryM_record = f"INSERT IGNORE INTO GT_searches ({Cry_col}) VALUES ({s})"
    my_cursor.execute(CryM_record, Cry_values)

    Database.commit()


    # Crypto Price data (Binance API)

    Termy = (f"Cryptos Data query Starting ...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    client = Client("uG9j8juEPNHt5bFRMe58AYiqqWgnENFA04X9rWbOaYyqpj9p6IljHXaYYIp6FXCg",
                    "xpPOrjEJFW2rZiMrFnBAS08JxLnUBh6SxuMhVypzKUvBwdLe0EIgetFttiZSsfsj")

    Cry_str = ['BNBUSDT', 'IOTAUSDT', 'VETUSDT', 'ADAUSDT', 'LTCUSDT']
    Cry_strn = ['BNB', 'IOTA', 'VET', 'ADA', 'LTC']

    Cry_PDdata = np.zeros(len(Cry_str))
    j = 0
    for crypto in Cry_str:
        print(crypto)
        data = client.get_klines(symbol=crypto, interval=client.KLINE_INTERVAL_1DAY)
        Cry_PDdata[j] = data[-2][4]
        j += 1

    record = f"INSERT INTO Cryptos (date, BNB, IOTA, VET, ADA, LTC) VALUES (%s, %s, %s, %s, %s, %s)"
    valus = (date.today() - timedelta(days=1),)
    for i in range(len(Cry_str)):
        cryp = Cry_PDdata[i]
        if cryp == 0 or cryp == 'NaN':
            query = f"SELECT {Cry_strn[i]} " \
                    f"FROM Stocks " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            cryp = my_cursor.fetchall()[0][0]
        valus += (float(cryp),)

    my_cursor.execute(record, valus)
    Database.commit()

    Termy = (f"Daily_Data Module Execution Completed.\n"
             f"\n"
             f"{datetime.now()}")

    Term = Term + Termy

    MTrecord = f'UPDATE Exception_Terminal SET DailyData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)

    if Excp == 1:
        MTsrecord = 'UPDATE Exception_Terminal SET DailyData = "error" WHERE PK = "Status" '
        my_cursor.execute(MTsrecord)
        Database.commit()
    else:
        MTsrecord = 'UPDATE Exception_Terminal SET DailyData = "idle" WHERE PK = "Status" '
        my_cursor.execute(MTsrecord)
        Database.commit()
