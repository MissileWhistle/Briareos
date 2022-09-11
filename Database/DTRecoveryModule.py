# This module is executed in case the Algorithm (or some specific module) has experiences downtime and as a results
# has not populated the database with the information it would otherwise, thus producing a desincronization of the
# information in the dabase. As such once that situation has ocurred this module is executed to gather and populate
# the database with the necessary information to assure correct data throughout the system.

from alpha_vantage.timeseries import TimeSeries
import coinmarketcapapi
import coinmetrics
from binance.client import Client
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import time
import math as mt
from datetime import date, timedelta, datetime
from HCtools import dateintpol, zerintpol
import mysql.connector as mysql


def DTRecovery():

    Database = mysql.connect(
        host="192.168.1.5",
        user="root",
        passwd="Briareos")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")


    # Database Downtime Recovery DB feed

    MTsrecord = 'UPDATE Exception_Terminal SET DTRecovery = "Running" WHERE PK = "Status" '
    my_cursor.execute(MTsrecord)
    Term = (f"{datetime.now()}\n"
            f"\n"
            f"Downtime Recovery Module Starting ...\n"
            f"\n")

    MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    # World indices data

    query = f"SELECT date " \
            f"FROM worldindices " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_days = mt.floor(Diff/24)

    if DT_days > 1 and datetime.now().hour > 8:

        Termy = (f"World Indices Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        ts = TimeSeries(key='TIU73LH54TAARJU2', output_format='pandas')

        Windexstr = [['EWA', 'EWT', 'INDA', 'EWZ', 'EEM'], ['EWQ', 'EWM', 'EWU', 'EWG', 'SPY'],
                    ['EWC', 'MCHI', 'VEA', 'EIDO', 'EWS'], ['VGK', 'EWJ', 'IYW', 'VGT', 'VDE'],
                    ['ERUS', 'XT', 'IAU', 'PICK', 'ICLN'], ['ITA']]

        Windex_name = ['EWA', 'EWT', 'INDA', 'EWZ', 'EEM', 'EWQ', 'EWM', 'EWU', 'EWG',
                      'SPY', 'EWC', 'MCHI', 'VEA', 'EIDO', 'EWS', 'VGK', 'EWJ', 'IYW', 'VGT',
                      'VDE', 'ERUS', 'XT', 'IAU', 'PICK', 'ICLN', 'ITA']

        length_Windex = len(Windexstr)
        Wi_startdate = []
        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                print(index)
                try:
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                except:
                    time.sleep(7)
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                print(data)
                Crydt = np.flip(pd.DataFrame.to_numpy(data['4. close']))
                print(Crydt)
                Wi_dts = data.index.sort_values(True)
                Wi_date = (Wi_dts[0][:].to_pydatetime())
                Wi_ind = [index for index, value in enumerate(Wi_date) if value <= (datetime.today() - timedelta(days=DT_days))]
                Wi_intdate = Wi_dts[0][Wi_ind[-1]:]
                Wi_startdate.append(Wi_date[Wi_ind[-1]].date())
                print(Wi_startdate)
                Crydata = Crydt[Wi_ind[-1]:]
                FullDate = pd.date_range(Wi_startdate[j], (date.today() - timedelta(days=1)))
                Cry_zrdata = zerintpol(Crydata)
                vars()[f"{Windex_name[j]}_l"] = zerintpol(dateintpol(FullDate, Wi_intdate, Cry_zrdata))
                j += 1
            time.sleep(61)

        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                price_data = vars()[f"{Windex_name[j]}_l"]
                vars()[f"{Windex_name[j]}"] = price_data[-DT_days+1:]
                print(vars()[f"{Windex_name[j]}"])
                j += 1

        Wi_record = "INSERT INTO worldindices (date, EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, SPY, EWC, " \
                    "MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT, VDE, ERUS, XT, IAU, PICK, ICLN, ITA) VALUES (%s, " \
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "


        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=1)))
        for j in range(DT_days-1):
            valus = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            for i in range(len(Windex_name)):
                index = vars()[f"{Windex_name[i]}"]
                valus += (float(index[j]),)
            my_cursor.execute(Wi_record, valus)

        Database.commit()

        Termy = (f"World Indices Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    elif DT_days > 2 and datetime.now().hour < 8:
        Termy = (f"World Indices Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        ts = TimeSeries(key='TIU73LH54TAARJU2', output_format='pandas')

        Windexstr = [['EWA', 'EWT', 'INDA', 'EWZ', 'EEM'], ['EWQ', 'EWM', 'EWU', 'EWG', 'SPY'],
                    ['EWC', 'MCHI', 'VEA', 'EIDO', 'EWS'], ['VGK', 'EWJ', 'IYW', 'VGT', 'VDE'],
                    ['ERUS', 'XT', 'IAU', 'PICK', 'ICLN'], ['ITA']]

        Windex_name = ['EWA', 'EWT', 'INDA', 'EWZ', 'EEM', 'EWQ', 'EWM', 'EWU', 'EWG',
                      'SPY', 'EWC', 'MCHI', 'VEA', 'EIDO', 'EWS', 'VGK', 'EWJ', 'IYW', 'VGT',
                      'VDE', 'ERUS', 'XT', 'IAU', 'PICK', 'ICLN', 'ITA']

        length_Windex = len(Windexstr)
        Wi_startdate = []
        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                print(index)
                try:
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                except:
                    time.sleep(7)
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                print(data)
                Crydt = np.flip(pd.DataFrame.to_numpy(data['4. close']))
                print(Crydt)
                Wi_dts = data.index.sort_values(True)
                Wi_date = (Wi_dts[0][:].to_pydatetime())
                Wi_ind = [index for index, value in enumerate(Wi_date) if value <= (datetime.today() - timedelta(days=DT_days))]
                Wi_intdate = Wi_dts[0][Wi_ind[-1]:]
                Wi_startdate.append(Wi_date[Wi_ind[-1]].date())
                print(Wi_startdate)
                Crydata = Crydt[Wi_ind[-1]:]
                FullDate = pd.date_range(Wi_startdate[j], (date.today() - timedelta(days=1)))
                Cry_zrdata = zerintpol(Crydata)
                vars()[f"{Windex_name[j]}_l"] = zerintpol(dateintpol(FullDate, Wi_intdate, Cry_zrdata))
                j += 1
            time.sleep(61)

        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                price_data = vars()[f"{Windex_name[j]}_l"]
                vars()[f"{Windex_name[j]}"] = price_data[-DT_days+1:]
                print(vars()[f"{Windex_name[j]}"])
                j += 1

        Wi_record = "INSERT INTO worldindices (date, EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, SPY, EWC, " \
                    "MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT, VDE, ERUS, XT, IAU, PICK, ICLN, ITA) VALUES (%s, " \
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=2)))
        for j in range(DT_days-2):
            valus = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            for i in range(len(Windex_name)):
                index = vars()[f"{Windex_name[i]}"]
                valus += (float(index[j]),)
            my_cursor.execute(Wi_record, valus)

        Database.commit()

        Termy = (f"World Indices Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    #Stocks Recovery

    query = f"SELECT date " \
            f"FROM Stocks " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_days = mt.floor(Diff/24)

    if DT_days > 1 and datetime.now().hour > 8:

        Termy = (f"Stocks Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        ts = TimeSeries(key='TIU73LH54TAARJU2', output_format='pandas')

        Windexstr = [['TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM'], ['AMZN', 'FB', 'HYMTF', 'VWAGY']]

        Windex_name = ['TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM', 'AMZN', 'FB', 'HYMTF', 'VWAGY']

        length_Windex = len(Windexstr)
        Wi_startdate = []
        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                print(index)
                try:
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                except:
                    time.sleep(7)
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                print(data)
                Crydt = np.flip(pd.DataFrame.to_numpy(data['4. close']))
                print(Crydt)
                Wi_dts = data.index.sort_values(True)
                Wi_date = (Wi_dts[0][:].to_pydatetime())
                Wi_ind = [index for index, value in enumerate(Wi_date) if value <= (datetime.today() - timedelta(days=DT_days))]
                Wi_intdate = Wi_dts[0][Wi_ind[-1]:]
                Wi_startdate.append(Wi_date[Wi_ind[-1]].date())
                print(Wi_startdate)
                Crydata = Crydt[Wi_ind[-1]:]
                FullDate = pd.date_range(Wi_startdate[j], (date.today() - timedelta(days=1)))
                Cry_zrdata = zerintpol(Crydata)
                vars()[f"{Windex_name[j]}_l"] = zerintpol(dateintpol(FullDate, Wi_intdate, Cry_zrdata))
                j += 1
            time.sleep(61)

        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                price_data = vars()[f"{Windex_name[j]}_l"]
                vars()[f"{Windex_name[j]}"] = price_data[-DT_days+1:]
                print(vars()[f"{Windex_name[j]}"])
                j += 1

        Wi_record = "INSERT INTO Stocks (date, TSLA, MSFT, GOOGL, AAPL, IBM, AMZN, FB, HYMTF, VWAGY) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "


        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=1)))
        for j in range(DT_days-1):
            valus = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            for i in range(len(Windex_name)):
                index = vars()[f"{Windex_name[i]}"]
                valus += (float(index[j]),)
            my_cursor.execute(Wi_record, valus)

        Database.commit()

        Termy = (f"Stocks Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    elif DT_days > 2 and datetime.now().hour < 8:
        Termy = (f"Stocks Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        ts = TimeSeries(key='TIU73LH54TAARJU2', output_format='pandas')

        Windexstr = [['TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM'], ['AMZN', 'FB', 'HYMTF', 'VWAGY']]

        Windex_name = ['TSLA', 'MSFT', 'GOOGL', 'AAPL', 'IBM', 'AMZN', 'FB', 'HYMTF', 'VWAGY']

        length_Windex = len(Windexstr)
        Wi_startdate = []
        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                print(index)
                try:
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                except:
                    time.sleep(7)
                    data, meta_data = ts.get_daily(symbol=index, outputsize='compact')
                print(data)
                Crydt = np.flip(pd.DataFrame.to_numpy(data['4. close']))
                print(Crydt)
                Wi_dts = data.index.sort_values(True)
                Wi_date = (Wi_dts[0][:].to_pydatetime())
                Wi_ind = [index for index, value in enumerate(Wi_date) if value <= (datetime.today() - timedelta(days=DT_days))]
                Wi_intdate = Wi_dts[0][Wi_ind[-1]:]
                Wi_startdate.append(Wi_date[Wi_ind[-1]].date())
                print(Wi_startdate)
                Crydata = Crydt[Wi_ind[-1]:]
                FullDate = pd.date_range(Wi_startdate[j], (date.today() - timedelta(days=1)))
                Cry_zrdata = zerintpol(Crydata)
                vars()[f"{Windex_name[j]}_l"] = zerintpol(dateintpol(FullDate, Wi_intdate, Cry_zrdata))
                j += 1
            time.sleep(61)

        j = 0
        for i in range(length_Windex):
            for index in Windexstr[i][:]:
                price_data = vars()[f"{Windex_name[j]}_l"]
                vars()[f"{Windex_name[j]}"] = price_data[-DT_days+1:]
                print(vars()[f"{Windex_name[j]}"])
                j += 1

        Wi_record = "INSERT INTO Stocks (date, TSLA, MSFT, GOOGL, AAPL, IBM, AMZN, FB, HYMTF, VWAGY) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=2)))
        for j in range(DT_days-2):
            valus = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            for i in range(len(Windex_name)):
                index = vars()[f"{Windex_name[i]}"]
                valus += (float(index[j]),)
            my_cursor.execute(Wi_record, valus)

        Database.commit()

        Termy = (f"Socks Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()


    # Crypto Market Index Recovery

    query = f"SELECT date " \
            f"FROM CryptoIndex " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_days = mt.floor(Diff/24)

    if DT_days > 1 and datetime.now().hour > 8:

        Termy = (f"Crypto Index Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        cmc = coinmarketcapapi.CoinMarketCapAPI('882524ed-0cbc-4507-85eb-71baca5ff3c3', sandbox=False)

        query = f"SELECT price " \
                f"FROM CryptoIndex " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        CIpriceo = my_cursor.fetchall()[0][0]

        try:
            indx = cmc.global_metrics_quotes_latest()
            CIpricen = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000
        except:
            time.sleep(7)
            indx = cmc.global_metrics_quotes_latest()
            CIpricen = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000

        CIdata= np.ndarray.tolist(np.hstack(((CIpriceo), np.zeros((DT_days-1)), (CIpricen))))
        Ci_startdate = DBdate
        FullDate = pd.date_range(Ci_startdate + timedelta(days=1), (date.today() - timedelta(days=1)))
        CMC = zerintpol(CIdata)[1:-1]

        CCi_record = "INSERT IGNORE INTO CryptoIndex (date, price) VALUES (%s, %s) "
        for j in range(DT_days-1):
            values = (datetime.strftime(FullDate[j], "%Y-%m-%d"), float(CMC[j]))
            my_cursor.execute(CCi_record, values)

        Database.commit()

        Termy = (f"Crypto Index Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    elif DT_days > 2 and datetime.now().hour < 8:

        Termy = (f"Crypto Index Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        cmc = coinmarketcapapi.CoinMarketCapAPI('882524ed-0cbc-4507-85eb-71baca5ff3c3', sandbox=False)

        query = f"SELECT price " \
                f"FROM CryptoIndex " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        CIpriceo = my_cursor.fetchall()[0][0]

        try:
            indx = cmc.global_metrics_quotes_latest()
            CIpricen = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000
        except:
            time.sleep(7)
            indx = cmc.global_metrics_quotes_latest()
            CIpricen = indx.data['quote']['USD']['altcoin_market_cap'] / 10000000

        CIdata= np.ndarray.tolist(np.hstack(((CIpriceo), np.zeros((DT_days-1)), (CIpricen))))
        Ci_startdate = DBdate
        FullDate = pd.date_range(Ci_startdate + timedelta(days=1), (date.today() - timedelta(days=2)))
        CMC = zerintpol(CIdata)[1:-1]

        CCi_record = "INSERT IGNORE INTO CryptoIndex (date, price) VALUES (%s, %s) "
        for j in range(DT_days-2):
            values = (datetime.strftime(FullDate[j], "%Y-%m-%d"), float(CMC[j]))
            my_cursor.execute(CCi_record, values)

        Database.commit()

        Termy = (f"Crypto Index Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    # Crypto Network data

    query = f"SELECT date " \
            f"FROM ltcMD " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_days = mt.floor(Diff/24)

    if DT_days > 1 and datetime.now().hour > 8:

        Termy = (f"Crypto's Network Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        Crypto_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo', 'gas', 'usdt', 'doge', 'ada', 'ltc']

        Cry_Metrics = [
            ['TxCnt', 'IssContNtv', 'TxTfrValMedNtv', 'TxTfrValMedUSD', 'FeeMeanUSD', 'AdrActCnt', 'DiffMean',
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
        i = 0
        for crypto in Crypto_str:
            for metric in Cry_Metrics[i]:
                print(crypto)
                print(metric)
                old_dt = date.today() - timedelta(days=DT_days-1)
                yesterday = date.today() - timedelta(days=-1)
                yesterday_date = yesterday.strftime("%Y-%m-%d")
                old_date = old_dt.strftime("%Y-%m-%d")
                try:
                    Cry_dt = cm.get_asset_metric_data(crypto, metric, old_date, yesterday_date)
                except:
                    time.sleep(10)
                    Cry_dt = cm.get_asset_metric_data(crypto, metric, old_date, yesterday_date)
                Cry_pandas_data = coinmetrics.cm_to_pandas(Cry_dt)
                vars()[f"{crypto}_{metric}"] = zerintpol(pd.DataFrame.to_numpy(Cry_pandas_data))
            i += 1

        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=1)))

        for j in range(DT_days-1):
            i=0
            for crypto in Crypto_str:
                metrc = 'date'
                values = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
                s = '%s'
                for metric in Cry_Metrics[i]:
                    valus = vars()[f"{crypto}_{metric}"]
                    values += (float(valus[j]),)
                    metrc += f', {metric}'
                    s += ', %s'
                i += 1

                MD_record = f"INSERT IGNORE INTO {crypto}MD ({metrc}) VALUES ({s})"
                my_cursor.execute(MD_record, values)

        Database.commit()

        Termy = (f"Crypto's Network Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    elif DT_days > 2 and datetime.now().hour < 8:

        Termy = (f"Crypto's Network Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        Crypto_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo', 'gas', 'usdt', 'doge', 'ada', 'ltc']

        Cry_Metrics = [
            ['TxCnt', 'IssContNtv', 'TxTfrValMedNtv', 'TxTfrValMedUSD', 'FeeMeanUSD', 'AdrActCnt', 'DiffMean',
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
        i = 0
        for crypto in Crypto_str:
            for metric in Cry_Metrics[i]:
                print(crypto)
                print(metric)
                old_dt = date.today() - timedelta(days=DT_days-1)
                yesterday = date.today() - timedelta(days=-2)
                yesterday_date = yesterday.strftime("%Y-%m-%d")
                old_date = old_dt.strftime("%Y-%m-%d")
                try:
                    Cry_dt = cm.get_asset_metric_data(crypto, metric, old_date, yesterday_date)
                except:
                    time.sleep(10)
                    Cry_dt = cm.get_asset_metric_data(crypto, metric, old_date, yesterday_date)
                Cry_pandas_data = coinmetrics.cm_to_pandas(Cry_dt)
                vars()[f"{crypto}_{metric}"] = zerintpol(pd.DataFrame.to_numpy(Cry_pandas_data))
            i += 1

        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=2)))

        for j in range(DT_days-2):
            i = 0
            for crypto in Crypto_str:
                metrc = 'date'
                values = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
                s = '%s'
                for metric in Cry_Metrics[i]:
                    valus = vars()[f"{crypto}_{metric}"]
                    values += (float(valus[j]),)
                    metrc += f', {metric}'
                    s += ', %s'
                i += 1

                MD_record = f"INSERT IGNORE INTO {crypto}MD ({metrc}) VALUES ({s})"
                my_cursor.execute(MD_record, values)

        Database.commit()

        Termy = (f"Crypto's Network Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    # Google Trends data

    query = f"SELECT date "\
            f"FROM GT_searches " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_days = mt.floor(Diff/24)

    if DT_days > 1 and datetime.now().hour > 8:

        Termy = (f"Google Trends Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        pytrends = TrendReq(hl='en-US', tz=0, retries=10, backoff_factor=0.5)

        GT_str = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple crypto', 'Stellar Lumens', 'ChainLink', 'NEO price',
              'XRP', 'blockchain', 'cryptocurrency', 'altcoin', 'Smart Contract', 'Binance']

        NGT = len(GT_str)

        if DT_days < 50:
            past = date.today() - timedelta(days=50)
        else:
            past = date.today() - timedelta(days=DT_days)
        past_dateP = past.strftime("%Y-%m-%d")
        yesterday = date.today() - timedelta(days=1)
        yesterday_date = yesterday.strftime("%Y-%m-%d")

        for search in GT_str:
            print(search)
            try:
                pytrends.build_payload(kw_list=[search], cat=7, timeframe=f"{past_dateP} {yesterday_date}", gprop='')
                GT_dtaP = pytrends.interest_over_time()
            except:
                time.sleep(20)
                pytrends.build_payload(kw_list=[search], cat=7, timeframe=f"{past_dateP} {yesterday_date}", gprop='')
                GT_dtaP = pytrends.interest_over_time()
            FulldateC = pd.date_range(pd.to_datetime(GT_dtaP.index)[0], (date.today() - timedelta(days=1)))
            vars()[f"{search}"] = zerintpol(dateintpol(FulldateC, pd.to_datetime(GT_dtaP.index),
                                                       pd.DataFrame.to_numpy(GT_dtaP[f"{search}"])))

        query = f"SELECT Bitcoin, BTC, ETH, Ethereum, Monero, Ripple_crypto, Stellar_Lumens, ChainLink, NEO_price, XRP, " \
                f"blockchain, cryptocurrency, altcoin, Smart_Contract, Binance "\
                f"FROM GT_searches " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        GT_data = np.asarray(Col)

        j = 0
        new_data = np.zeros((DT_days-1, len(GT_data[0])))
        for search in GT_str:
            pst = vars()[f"{search}"][-DT_days]
            new = vars()[f"{search}"][-DT_days+1:]
            dbpast = GT_data[0, j]
            new_data[:, j] = np.asarray(new) * (dbpast / pst)
            j += 1

        GT_dbname = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple_crypto', 'Stellar_Lumens', 'ChainLink', 'NEO_price',
                     'XRP', 'blockchain', 'cryptocurrency', 'altcoin', 'Smart_Contract', 'Binance' ]
        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=1)))
        for j in range(DT_days-1):
            Cry_values = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            Cry_col = 'date'
            s = '%s'
            for r in range(NGT):
                Cry_values += (float(new_data[j, r]),)
                s += ', %s'
                Cry_col += f', {GT_dbname[r]}'
            CryM_record = f"INSERT IGNORE INTO GT_searches ({Cry_col}) VALUES ({s})"
            my_cursor.execute(CryM_record, Cry_values)

        Database.commit()

        Termy = (f"Google Trends Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    elif DT_days > 2 and datetime.now().hour < 8:
        Termy = (f"Google Trends Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        pytrends = TrendReq(hl='en-US', tz=0, retries=10, backoff_factor=0.5)

        GT_str = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple crypto', 'Stellar Lumens', 'ChainLink', 'NEO price',
                  'XRP', 'blockchain', 'cryptocurrency', 'altcoin', 'Smart Contract', 'Binance']
        NGT = len(GT_str)

        for search in GT_str:
            print(search)
            if DT_days <= 50:
                past = date.today() - timedelta(days=50)
            else:
                past = date.today() - timedelta(days=DT_days)
            past_dateP = past.strftime("%Y-%m-%d")
            yesterday = date.today() - timedelta(days=1)
            yesterday_date = yesterday.strftime("%Y-%m-%d")
            try:
                pytrends.build_payload(kw_list=[search], cat=7, timeframe=f"{past_dateP} {yesterday_date}", gprop='')
                GT_dtaP = pytrends.interest_over_time()
            except:
                time.sleep(20)
                pytrends.build_payload(kw_list=[search], cat=7, timeframe=f"{past_dateP} {yesterday_date}", gprop='')
                GT_dtaP = pytrends.interest_over_time()
            print(GT_dtaP)
            vars()[f"{search}"] = zerintpol(
                pd.DataFrame.to_numpy(GT_dtaP[f"{search}"]))

        query = f"SELECT Bitcoin, BTC, ETH, Ethereum, Monero, Ripple_crypto, Stellar_Lumens, ChainLink, NEO_price, XRP, " \
                f"blockchain, cryptocurrency, altcoin, Smart_Contract, Binance "\
                f"FROM GT_searches " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        GT_data = np.asarray(Col)

        j = 0
        new_data = np.zeros((DT_days-1, len(GT_data[0])))
        for search in GT_str:
            pst = vars()[f"{search}"][-DT_days]
            new = vars()[f"{search}"][-DT_days+1:]
            dbpast = GT_data[0, j]
            new_data[:, j] = np.asarray(new) * (dbpast / pst)
            j += 1

        GT_dbname = ["Bitcoin", "BTC", "ETH", "Ethereum", "Monero", 'Ripple_crypto', 'Stellar_Lumens', 'ChainLink', 'NEO_price',
                     'XRP', 'blockchain', 'cryptocurrency', 'altcoin', 'Smart_Contract', 'Binance' ]
        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=2)))
        for j in range(DT_days-2):
            Cry_values = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            Cry_col = 'date'
            s = '%s'
            for r in range(NGT):
                Cry_values += (float(new_data[j, r]),)
                s += ', %s'
                Cry_col += f', {GT_dbname[r]}'
            CryM_record = f"INSERT IGNORE INTO GT_searches ({Cry_col}) VALUES ({s})"
            my_cursor.execute(CryM_record, Cry_values)

        Database.commit()

        Termy = (f"Google Trends Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    # Cryptos

    query = f"SELECT date " \
            f"FROM Cryptos " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    Diff = mt.floor(24 * (datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds / 3600)
    DT_days = mt.floor(Diff / 24)

    if DT_days > 1 and datetime.now().hour > 8:

        Termy = (f"Cryptos Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        client = Client("uG9j8juEPNHt5bFRMe58AYiqqWgnENFA04X9rWbOaYyqpj9p6IljHXaYYIp6FXCg",
                        "xpPOrjEJFW2rZiMrFnBAS08JxLnUBh6SxuMhVypzKUvBwdLe0EIgetFttiZSsfsj")

        Cry_str = ['BNBUSDT', 'IOTAUSDT', 'VETUSDT', 'ADAUSDT', 'LTCUSDT']

        for crypto in Cry_str:
            print(crypto)
            try:
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            except:
                time.sleep(7)
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            data_np = np.asarray(data)
            vars()[f"{crypto}d"] = data_np[:-1, 4]

        Cr_record = f"INSERT INTO Cryptos (date, BNB, IOTA, VET, ADA, LTC) VALUES (%s, %s, %s, %s, %s, %s)"
        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days - 1)), (date.today() - timedelta(days=1)))
        for j in range(DT_days - 1):
            valus = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            for i in range(len(Cry_str)):
                index = vars()[f"{Cry_str[i]}d"]
                valus += (float(index[j]),)
            my_cursor.execute(Cr_record, valus)

        Database.commit()

        Termy = (f"Cryptos Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    elif DT_days > 2 and datetime.now().hour < 8:

        Termy = (f"Cryptos Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        client = Client("uG9j8juEPNHt5bFRMe58AYiqqWgnENFA04X9rWbOaYyqpj9p6IljHXaYYIp6FXCg",
                        "xpPOrjEJFW2rZiMrFnBAS08JxLnUBh6SxuMhVypzKUvBwdLe0EIgetFttiZSsfsj")

        Cry_str = ['BNBUSDT', 'IOTAUSDT', 'VETUSDT', 'ADAUSDT', 'LTCUSDT']

        for crypto in Cry_str:
            print(crypto)
            try:
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            except:
                time.sleep(7)
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            data_np = np.asarray(data)
            vars()[f"{crypto}d"] = data_np[:-1, 4]

        Cr_record = f"INSERT INTO Cryptos (date, BNB, IOTA, VET, ADA, LTC) VALUES (%s, %s, %s, %s, %s, %s)"
        Fulldate = pd.date_range((date.today() - timedelta(days=DT_days-1)), (date.today() - timedelta(days=2)))
        for j in range(DT_days - 2):
            valus = (datetime.strftime(Fulldate[j], "%Y-%m-%d"),)
            for i in range(len(Cry_str)):
                index = vars()[f"{Cry_str[i]}d"]
                valus += (float(index[j]),)
            my_cursor.execute(Cr_record, valus)

        Database.commit()

        Termy = (f"Crypto's daily price Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()


    # P.Crypto Price data
    # Daily

    query = f"SELECT date "\
            f"FROM BTCUSDTd " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_days = mt.floor(Diff/24)

    if DT_days > 1 and datetime.now().hour > 0:

        Termy = (f"Crypto's daily price Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        client = Client("uG9j8juEPNHt5bFRMe58AYiqqWgnENFA04X9rWbOaYyqpj9p6IljHXaYYIp6FXCg",
                        "xpPOrjEJFW2rZiMrFnBAS08JxLnUBh6SxuMhVypzKUvBwdLe0EIgetFttiZSsfsj")

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']

        for crypto in Cry_str:
            print(crypto)
            try:
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            except:
                time.sleep(7)
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            print(data)
            data_np = np.asarray(data)
            vars()[f"{crypto}d"] = data_np[:-1, 0:6]
            print(vars()[f"{crypto}d"])

        for crypto in Cry_str:
            for j in range(DT_days-1):
                dte = vars()[f"{crypto}d"][j, 0]
                Cdate = [datetime.fromtimestamp(int(dte) / 1000)]
                pdata = [float(i) for i in vars()[f"{crypto}d"][j, 1:6]]
                valus = [Cdate, pdata]
                values = tuple([item for sublist in valus for item in sublist])
                record = f"INSERT IGNORE INTO {crypto}d (date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
                my_cursor.execute(record, values)

        Database.commit()

        Termy = (f"Crypto's daily price Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    elif DT_days > 2 and datetime.now().hour == 0:

        Termy = (f"Crypto's daily price Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        client = Client("uG9j8juEPNHt5bFRMe58AYiqqWgnENFA04X9rWbOaYyqpj9p6IljHXaYYIp6FXCg",
                        "xpPOrjEJFW2rZiMrFnBAS08JxLnUBh6SxuMhVypzKUvBwdLe0EIgetFttiZSsfsj")

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']

        for crypto in Cry_str:
            print(crypto)
            try:
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            except:
                time.sleep(7)
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, f"{DT_days} days ago UTC")
            print(data)
            data_np = np.asarray(data)
            vars()[f"{crypto}d"] = data_np[:-1, 0:6]
            print(vars()[f"{crypto}d"])

        for crypto in Cry_str:
            for j in range(DT_days-2):
                dte = vars()[f"{crypto}d"][j, 0]
                Cdate = [datetime.fromtimestamp(int(dte) / 1000)]
                pdata = [float(i) for i in vars()[f"{crypto}d"][j, 1:6]]
                valus = [Cdate, pdata]
                values = tuple([item for sublist in valus for item in sublist])
                record = f"INSERT IGNORE INTO {crypto}d (date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
                my_cursor.execute(record, values)

        Database.commit()

        Termy = (f"Crypto's daily price Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    # Hourly

    query = f"SELECT date "\
            f"FROM BTCUSDTh " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DBdate = datetime(DBdate.year, DBdate.month, DBdate.day, DBdate.hour)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_days = mt.ceil(Diff/24)

    if Diff > 2:

        Termy = (f"Crypto's hourly price Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        client = Client("uG9j8juEPNHt5bFRMe58AYiqqWgnENFA04X9rWbOaYyqpj9p6IljHXaYYIp6FXCg",
                        "xpPOrjEJFW2rZiMrFnBAS08JxLnUBh6SxuMhVypzKUvBwdLe0EIgetFttiZSsfsj")

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']

        for crypto in Cry_str:
            print(crypto)
            try:
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1HOUR, f"{DT_days} days ago UTC")
            except:
                time.sleep(7)
                data = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1HOUR, f"{DT_days} days ago UTC")
            print(data)
            data_np = np.asarray(data)
            vars()[f"{crypto}h"] = data_np[-Diff:-1, 0:6]
            print(vars()[f"{crypto}h"])

        for crypto in Cry_str:
            for j in range(Diff-2):
                dte = vars()[f"{crypto}h"][j, 0]
                Cdate = [datetime.fromtimestamp(int(dte) / 1000)]
                pdata = [float(i) for i in vars()[f"{crypto}h"][j, 1:6]]
                valus = [Cdate, pdata]
                values = tuple([item for sublist in valus for item in sublist])
                record = f"INSERT IGNORE INTO {crypto}h ( date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
                my_cursor.execute(record, values)

        Database.commit()

        Termy = (f"Crypto's hourly price Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    # Funds

    query = f"SELECT date "\
            f"FROM Port_values " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DBdate = datetime(DBdate.year, DBdate.month, DBdate.day, DBdate.hour)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    if Diff > 1:
        Termy = (f"Funds Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        def trunc8(x):
            a = np.trunc(x * 100000000) / 100000000
            return a

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        prices = np.zeros((Diff, len(Cry_str)))
        j = 0
        for crypto in Cry_str:
            query = f"SELECT close " \
                    f"FROM {crypto}h " \
                    f"ORDER BY date DESC " \
                    f"LIMIT {Diff} "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [item for sublist in [list(i) for i in col] for item in sublist]
            list.reverse(Col)
            prices[:, j] = Col[-Diff:]
            j += 1

        Cry_strn = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO', 'USDT']

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO, USDT " \
                f"FROM Port_values " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Avals = np.asarray(Col)[0]

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO, USDT " \
                f"FROM Port_values_Short " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        SAvals = np.asarray(Col)[0]

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO, USDT " \
                f"FROM Port_values_Long " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        LAvals = np.asarray(Col)[0]

        pricesr = ((prices-prices[0, :])/prices[0, :]) + 1
        pricesr = pricesr[1:, :]
        prices = prices[1:, :]

        TF_record = "INSERT IGNORE INTO totalfunds (date, value) VALUES (%s, %s)"
        record = " INSERT INTO Port_values VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Srecord = " INSERT INTO Port_values_short VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Lrecord = " INSERT INTO Port_values_long VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        nowr = datetime.now() - timedelta(hours=1)
        Fulldate = pd.date_range(start=DBdate + timedelta(hours=1), end=datetime(nowr.year, nowr.month, nowr.day,
                                                                                 nowr.hour), freq='1H')
        for j in np.arange(len(Fulldate)):
            TotalFunds = 0
            tva = []
            sva = []
            lva = []
            for i in range(len(Cry_strn)):
                if i == len(Cry_strn)-1:
                    va = trunc8(Avals[i])
                    tva += [va]
                    sva += [va]
                    lva += [va]
                else:
                    va = trunc8(Avals[i] * pricesr[j, i])
                    tva += [va]
                    svas = SAvals[i]*pricesr[j, i]
                    lvas = LAvals[i]*pricesr[j, i]

                    prc = np.asarray([svas / (svas + lvas), lvas / (svas + lvas)])
                    prc[(np.isnan(prc)) | (np.isinf(prc))] = 0
                    sva += [prc[0] * va]
                    lva += [prc[1] * va]
                TotalFunds += va
            values = (Fulldate[j], float(TotalFunds))
            tvalues = [Fulldate[j]] + tva
            svalues = [Fulldate[j]] + sva
            lvalues = [Fulldate[j]] + lva
            my_cursor.execute(TF_record, values)
            my_cursor.execute(record, tuple(tvalues))
            my_cursor.execute(Srecord, tuple(svalues))
            my_cursor.execute(Lrecord, tuple(lvalues))

        Database.commit()

        Termy = (f"Funds Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    # Profit Loss Recovery

    query = f"SELECT date "\
            f"FROM profit_loss " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DBdate = datetime(DBdate.year, DBdate.month, DBdate.day, DBdate.hour)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    if Diff > 1:
        Termy = (f"Profit-Loss Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']

        record = " INSERT INTO profit_loss VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
        Srecord = " INSERT INTO profit_loss_short VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
        Lrecord = " INSERT INTO profit_loss_long VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
        nowr = datetime.now() - timedelta(hours=1)
        Fulldate = pd.date_range(start=DBdate + timedelta(hours=1), end=datetime(nowr.year, nowr.month, nowr.day,
                                                                                 nowr.hour), freq='1H')

        for j in np.arange(len(Fulldate)):
            values = [Fulldate[j]] + np.ndarray.tolist(np.zeros((1,len(Cry_str)))[0])
            my_cursor.execute(record, tuple(values))
            my_cursor.execute(Srecord, tuple(values))
            my_cursor.execute(Lrecord, tuple(values))

        Database.commit()

        Termy = (f"Profit-Loss Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()


    # Trading Signals

    # Hourly Trading

    query = f"SELECT date "\
            f"FROM ShortTradingSig " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DBdate = datetime(DBdate.year, DBdate.month, DBdate.day, DBdate.hour)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    if Diff > 1:
        Termy = (f"Trading Signals (hourly) Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM ShortTradingSig " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        STSg = list(my_cursor.fetchall()[0])

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM ShortTradingSigR " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        STSRg = list(my_cursor.fetchall()[0])

        SGS_record = "INSERT IGNORE INTO ShortTradingSig (date, BTC, ETH, XLM, XMR, XRP, LINK, NEO) VALUES (%s, %s," \
                     " %s, %s, %s, %s, %s, %s)"
        SGSR_record = "INSERT IGNORE INTO ShortTradingSigR (date, BTC, ETH, XLM, XMR, XRP, LINK, NEO) VALUES (%s, %s," \
                      " %s, %s, %s, %s, %s, %s)"
        nowr = datetime.now() - timedelta(hours=1)
        Fulldate = pd.date_range(start=DBdate + timedelta(hours=1),
                                 end=datetime(nowr.year, nowr.month, nowr.day, nowr.hour), freq='1H')
        for j in range(Diff - 1):
            values = [Fulldate[j]] + STSg
            valuesR = [Fulldate[j]] + STSRg
            my_cursor.execute(SGS_record, tuple(values))
            my_cursor.execute(SGSR_record, tuple(valuesR))

        Database.commit()

        Termy = (f"Trading Signals (hourly) Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()


    # Daily Trading (hourly)

    query = f"SELECT date "\
            f"FROM LongTradingSig " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DBdate = datetime(DBdate.year, DBdate.month, DBdate.day, DBdate.hour)
    Diff = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    if Diff > 1:
        Termy = (f"Trading Signals (daily) Recovery Process Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM LongTradingSig " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        LTSg = list(my_cursor.fetchall()[0])

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM LongTradingSigR " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        LTSRg = list(my_cursor.fetchall()[0])

        LGS_record = "INSERT IGNORE INTO LongTradingSig (date, BTC, ETH, XLM, XMR, XRP, LINK, NEO) VALUES (%s, %s," \
                     " %s, %s, %s, %s, %s, %s)"
        LGSR_record = "INSERT IGNORE INTO LongTradingSigR (date, BTC, ETH, XLM, XMR, XRP, LINK, NEO) VALUES (%s, %s," \
                      " %s, %s, %s, %s, %s, %s)"
        nowr = datetime.now() - timedelta(hours=1)
        Fulldate = pd.date_range(start=DBdate + timedelta(hours=1), end=datetime(nowr.year, nowr.month, nowr.day, nowr.hour), freq='1H')
        for j in range(Diff - 1):
            values = [Fulldate[j]] + LTSg
            valuesR = [Fulldate[j]] + LTSRg
            my_cursor.execute(LGS_record, tuple(values))
            my_cursor.execute(LGSR_record, tuple(valuesR))

        Database.commit()

        Termy = (f"Trading Signals (daily) Recovery Process Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    Termy = (f"Down Time Recovery Module Completed Successfully.\n"
             f"\n"
             f"{datetime.now()}")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET DTRecovery = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    MTsrecord = 'UPDATE Exception_Terminal SET DTRecovery = "idle" WHERE PK = "Status" '
    my_cursor.execute(MTsrecord)
    Database.commit()
