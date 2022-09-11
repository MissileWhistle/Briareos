# This module is used to liquidate the portfolio and clear all information about the portfolios accounting in the
# database, then it repopulates it wih the current values from the Exchange, thus restarting completely the
# trading process. It's used in case an error in the portfolios accounting is found

import mysql.connector as mysql
from datetime import datetime, date
import time
import numpy as np
import pandas
from binance.client import Client

Database = mysql.connect(
    host="",
    user="",
    passwd="")

my_cursor = Database.cursor()

my_cursor.execute("USE briareos")


def trunc1(x):
    a = np.trunc(x * 10) / 10
    return a


def trunc2(x):
    a = np.trunc(x * 100) / 100
    return a


def trunc3(x):
    a = np.trunc(x * 1000) / 1000
    return a


def trunc5(x):
    a = np.trunc(x * 100000) / 100000
    return a


def trunc6(x):
    a = np.trunc(x * 1000000) / 1000000
    return a

def trunc8(x):
    a = np.trunc(x * 100000000) / 100000000
    return a

truncatefunc = [trunc6, trunc5, trunc1, trunc5, trunc1, trunc2, trunc3]

# Trading Module (System 3)

# Short-Term Trading

delrec = " DELETE FROM ShortTradingSig ORDER BY date DESC LIMIT 1"
delrecr = " DELETE FROM ShortTradingSigR ORDER BY date DESC LIMIT 1"
my_cursor.execute(delrec)
my_cursor.execute(delrecr)
Database.commit()

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

delrec = " DELETE FROM LongTradingSig ORDER BY date DESC LIMIT 1"
delrecr = " DELETE FROM LongTradingSigR ORDER BY date DESC LIMIT 1"
my_cursor.execute(delrec)
my_cursor.execute(delrecr)
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

my_cursor.execute("DELETE FROM totalfunds")

Database.commit()

# Miscellaneous

my_cursor.execute("DELETE FROM miscellaneous")

record = "INSERT INTO Miscellaneous (t, MinPort, SavRate, Inception_Date) VALUES ( %s, %s, %s, %s)"
values = (35, 450, 0.3, date.today())  # MinPort related to inception Portfolio values
my_cursor.execute(record, values)
Database.commit()

Database.commit()

# Trading data

my_cursor.execute("DELETE FROM BuyPrices")

my_cursor.execute("DELETE FROM BuyPrices_Short")

my_cursor.execute("DELETE FROM BuyPrices_Long")

my_cursor.execute("DELETE FROM BuyValues")

my_cursor.execute("DELETE FROM BuyValues_Short")

my_cursor.execute("DELETE FROM BuyValues_Long")

my_cursor.execute("DELETE FROM Profit_Loss")

my_cursor.execute("DELETE FROM Profit_Loss_Short")

my_cursor.execute("DELETE FROM Profit_Loss_Long")

my_cursor.execute("DELETE FROM Port_values")

my_cursor.execute("DELETE FROM Port_values_short")

my_cursor.execute("DELETE FROM Port_values_long")

my_cursor.execute("DELETE FROM PayOut")

my_cursor.execute("DELETE FROM TotalFunds")

Database.commit()


client = Client("",
                "")

Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
Cry_strn = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO', 'USDT']

for i in range(len(Cry_str)):
    ordbk = pandas.DataFrame(client.get_orderbook_tickers())
    ordbk = ordbk.set_index('symbol')
    bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
    sprices = float(bidaskprice.loc[f'{Cry_str[i]}', 'bidPrice'])
    vap = client.get_asset_balance(asset=Cry_strn[i])
    ordS = truncatefunc[i](float(vap['free']))
    if ordS * sprices > 10:
        order = client.order_market_sell(symbol=Cry_str[i], quantity=ordS)

time.sleep(30)

nowr = datetime.now()

i = 0
TotalFunds = 0
bprices=[]
AVals = np.zeros((1, len(Cry_strn)))[0]
LAvals = np.zeros((1, len(Cry_strn)))[0]
lstb = np.zeros((1, len(Cry_strn)-1))[0]
Llstb = np.zeros((1, len(Cry_strn)-1))[0]
Llstbp = np.zeros((1, len(Cry_strn)-1))[0]
ordbk = pandas.DataFrame(client.get_orderbook_tickers())
ordbk = ordbk.set_index('symbol')
bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
for crypto in Cry_strn:
    if crypto == 'USDT':
        vap = client.get_asset_balance(asset=crypto)
        va = float(vap['free'])
    else:
        bprices += [float(bidaskprice.loc[f'{Cry_str[i]}', 'askPrice'])]
        vap = client.get_asset_balance(asset=crypto)
        vas = (float(vap['free']) + float(vap['locked']))
        va = (float(vap['free']) + float(vap['locked'])) * bprices[i]
        lstb[i] = vas
    AVals[i] = trunc8(va)
    i += 1

SAvals = AVals
LAvals[-1] = AVals[-1]
lstbp = AVals[:-1]
Slstbp = AVals[:-1]
Slstb = lstb

record = " INSERT INTO Port_values VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
srecord = " INSERT INTO Port_values_short VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
lrecord = " INSERT INTO Port_values_long VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
precord = " INSERT INTO PayOut VALUES ( %s, %s)"
values = [nowr] + np.ndarray.tolist(AVals)
svalues = [nowr] + np.ndarray.tolist(SAvals)
lvalues = [nowr] + np.ndarray.tolist(LAvals)
values = tuple(values)
pvals = (nowr, 0)
my_cursor.execute(record, values)
my_cursor.execute(srecord, svalues)
my_cursor.execute(lrecord, lvalues)
my_cursor.execute(precord, pvals)

record = " INSERT INTO BuyValues VALUES ( %s, %s, %s, %s, %s, %s, %s)"
srecord = " INSERT INTO BuyValues_Short VALUES ( %s, %s, %s, %s, %s, %s, %s)"
lrecord = " INSERT INTO BuyValues_Long VALUES ( %s, %s, %s, %s, %s, %s, %s)"
dat = lstb
sdat = Slstb
ldat = Llstb
values = tuple(dat)
svalues = tuple(sdat)
lvalues = tuple(ldat)
my_cursor.execute(record, values)
my_cursor.execute(srecord, svalues)
my_cursor.execute(lrecord, lvalues)

record = " INSERT INTO BuyPrices VALUES ( %s, %s, %s, %s, %s, %s, %s)"
srecord = " INSERT INTO BuyPrices_Short VALUES ( %s, %s, %s, %s, %s, %s, %s)"
lrecord = " INSERT INTO BuyPrices_Long VALUES ( %s, %s, %s, %s, %s, %s, %s)"
dat = lstbp
sdat = Slstbp
ldat = Llstbp
values = tuple(dat)
svalues = tuple(sdat)
lvalues = tuple(ldat)
my_cursor.execute(record, values)
my_cursor.execute(srecord, svalues)
my_cursor.execute(lrecord, lvalues)

record = " INSERT INTO profit_loss VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
srecord = " INSERT INTO profit_loss_short VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
lrecord = " INSERT INTO profit_loss_long VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
dat = [datetime.now()] + np.ndarray.tolist(np.zeros((1, 7))[0])
values = tuple(dat)
my_cursor.execute(record, values)
my_cursor.execute(srecord, values)
my_cursor.execute(lrecord, values)

record = f"INSERT IGNORE INTO TotalFunds ( date, value) VALUES (%s, %s) "
values = (datetime.now(), sum(AVals))
my_cursor.execute(record, values)
Database.commit()

Database.commit()

