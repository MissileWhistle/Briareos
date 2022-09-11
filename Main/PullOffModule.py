# This module liquidates the portfolios the algorithm manages

def PullOffModule():

    import mysql.connector as mysql
    import traceback
    import sys

    Database = mysql.connect(
        host="",
        user="",
        passwd="")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    MTrecord = 'UPDATE Exception_Terminal SET Trad_OEM = "Running" WHERE PK = "Status" '
    my_cursor.execute(MTrecord)
    Database.commit()

    Term = ""

    try:
        import matlab.engine
        import numpy as np
        from datetime import datetime
        import pandas
        from binance.client import Client
        import smtplib
        import ssl
        from email.message import EmailMessage

        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = ""
        receiver_email = ""
        password = ''

        eng = matlab.engine.start_matlab()

        eng.cd(r'C:\Users\Machine3\Desktop\Matlab Code', nargout=0)
        eng.ls(nargout=0)

        client = Client("",
                        "")

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

        Termy = ("PullOff Process Starting ...\n"
                 "\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        Cry_strO = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']

        truncatefunc = [trunc6, trunc5, trunc1, trunc5, trunc1, trunc2, trunc3]

        # (Selling)

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM BuyValues " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        lstb = np.asarray(Col)[0]

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM BuyValues_Short " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Slstb = np.asarray(Col)[0]

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM BuyValues_Long " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Llstb = np.asarray(Col)[0]

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM BuyPrices_Short " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Slstbp = np.asarray(Col)[0]

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM BuyPrices_Long " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Llstbp = np.asarray(Col)[0]

        lserr = []
        lserrval = []
        vals = np.zeros((1, len(Cry_str)))[0]
        Svals = np.zeros((1, len(Cry_str)))[0]
        Lvals = np.zeros((1, len(Cry_str)))[0]
        valsp = np.zeros((1, len(Cry_str)))[0]
        Svalsp = np.zeros((1, len(Cry_str)))[0]
        Lvalsp = np.zeros((1, len(Cry_str)))[0]
        for i in range(len(Cry_str)):
            ordbk = pandas.DataFrame(client.get_orderbook_tickers())
            ordbk = ordbk.set_index('symbol')
            bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
            sprices = float(bidaskprice.loc[f'{Cry_strO[i]}', 'bidPrice'])
            ordS = truncatefunc[i](lstb[i])
            if ordS * sprices > 10:
                try:
                    Bdtao = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                    order = client.order_market_sell(symbol=Cry_strO[i], quantity=ordS)
                    ordIdo = Bdtao[0]['orderId']
                    orders = 0
                    while orders != []:
                        orders = client.get_open_orders(symbol=Cry_strO[i])

                    Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                    dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                    sde = Bdta[0]['side']
                    ordId = ordIdo
                    while [dttm.year, dttm.month, dttm.day, dttm.hour] != \
                            [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour] \
                            or sde != 'SELL' or ordId == ordIdo:
                        Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                        dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                        ordId = Bdta[0]['orderId']
                        sde = Bdta[0]['side']

                    Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                    vals[i] = float(Bdta[0]['executedQty'])
                    Svals[i] = (Slstb[i] / (Slstb[i] + Llstb[i])) * vals[i]
                    Lvals[i] = (Llstb[i] / (Slstb[i] + Llstb[i])) * vals[i]
                    valsp[i] = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                    Svalsp[i] = (Slstb[i] / (Slstb[i] + Llstb[i])) * valsp[i]
                    Lvalsp[i] = (Llstb[i] / (Slstb[i] + Llstb[i])) * valsp[i]
                except Exception as e:
                    msg = EmailMessage()
                    msg.set_content(f"PullOff Trading order resulted in error.\n"
                                    f"Sell Order scrubbed for {Cry_strO[i]}_SL.\n"
                                    f"\n"
                                    f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                    f"{e}\n"
                                    f"\n"
                                    f"\n"
                                    f"Traceback:\n"
                                    f"\n"
                                    f"{traceback.format_exc()}"
                                    f"\n")

                    msg['Subject'] = "Briareos.binance PullOff Trading Error"
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.send_message(msg)

                    Termy = (f"Sell Order scrubbed for {Cry_strO[i]}_SL. Check Email for more information.\n"
                             f"\n")
                    Term = Term + Termy
                    MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                    my_cursor.execute(MTrecord)
                    Database.commit()
            else:
                lserr += [Cry_str[i]]
                lserrval += [ordS]

        bupdt = lstb - vals
        Sbupdt = Slstb - Svals
        Lbupdt = Llstb - Lvals

        buyper = abs(vals / lstb)
        sbuyper = abs(Svals / Slstb)
        lbuyper = abs(Lvals / Llstb)
        buyper[(np.isnan(buyper)) | (np.isinf(buyper))] = 0
        sbuyper[(np.isnan(sbuyper)) | (np.isinf(sbuyper))] = 0
        lbuyper[(np.isnan(lbuyper)) | (np.isinf(lbuyper))] = 0

        Sbupdtp = Slstbp * (1 - sbuyper)
        Lbupdtp = Llstbp * (1 - lbuyper)
        bupdtp = Sbupdtp + Lbupdtp

        Sprofit = -Slstbp * sbuyper + Svalsp
        Lprofit = -Llstbp * lbuyper + Lvalsp
        profit = Sprofit + Lprofit

        precord = " INSERT INTO Profit_Loss VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
        sprecord = " INSERT INTO Profit_Loss_Short VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
        lprecord = " INSERT INTO Profit_Loss_Long VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
        nowr = datetime.now()
        pvals = [nowr] + np.ndarray.tolist(profit)
        Spvals = [nowr] + np.ndarray.tolist(Sprofit)
        Lpvals = [nowr] + np.ndarray.tolist(Lprofit)
        my_cursor.execute(precord, tuple(pvals))
        my_cursor.execute(sprecord, tuple(Spvals))
        my_cursor.execute(lprecord, tuple(Lpvals))
        Database.commit()

        EMrecord = f"UPDATE BuyValues SET BTC={bupdt[0]}, ETH={bupdt[1]}, XLM={bupdt[2]}, XMR={bupdt[3]}," \
                   f" XRP={bupdt[4]}, LINK={bupdt[5]}, NEO={bupdt[6]}"
        SEMrecord = f"UPDATE BuyValues_short SET BTC={Sbupdt[0]}, ETH={Sbupdt[1]}, XLM={Sbupdt[2]}, XMR={Sbupdt[3]}," \
                    f" XRP={Sbupdt[4]}, LINK={Sbupdt[5]}, NEO={Sbupdt[6]}"
        LEMrecord = f"UPDATE BuyValues_long SET BTC={Lbupdt[0]}, ETH={Lbupdt[1]}, XLM={Lbupdt[2]}, XMR={Lbupdt[3]}," \
                    f" XRP={Lbupdt[4]}, LINK={Lbupdt[5]}, NEO={Lbupdt[6]}"
        my_cursor.execute(EMrecord)
        my_cursor.execute(SEMrecord)
        my_cursor.execute(LEMrecord)
        Database.commit()

        EMrecord = f"UPDATE BuyPrices SET BTC={bupdtp[0]}, ETH={bupdtp[1]}, XLM={bupdtp[2]}, XMR={bupdtp[3]}," \
                   f" XRP={bupdtp[4]}, LINK={bupdtp[5]}, NEO={bupdtp[6]}"
        SEMrecord = f"UPDATE BuyPrices_short SET BTC={Sbupdtp[0]}, ETH={Sbupdtp[1]}, XLM={Sbupdtp[2]}, XMR={Sbupdtp[3]}," \
                    f" XRP={Sbupdtp[4]}, LINK={Sbupdtp[5]}, NEO={Sbupdtp[6]}"
        LEMrecord = f"UPDATE BuyPrices_long SET BTC={Lbupdtp[0]}, ETH={Lbupdtp[1]}, XLM={Lbupdtp[2]}, XMR={Lbupdtp[3]}," \
                    f" XRP={Lbupdtp[4]}, LINK={Lbupdtp[5]}, NEO={Lbupdtp[6]}"
        my_cursor.execute(EMrecord)
        my_cursor.execute(SEMrecord)
        my_cursor.execute(LEMrecord)
        Database.commit()

        if lserr != []:
            msg = EmailMessage()
            msg.set_content(f"PullOff Module:\n"
                            f"\n"
                            f"Some (Trading) Selling Transaction where lower than 10$.\n"
                            f"\n"
                            f"Assets:\n"
                            f"{lserr}\n"
                            f"\n"
                            f"Values:\n"
                            f"{lserrval}\n"
                            f"\n")
            msg['Subject'] = " Briareos PullOff Trade Scrubbed"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)

        # Trading Signals

        # Short-Term Trading

        record = "INSERT INTO ShortTradingSig VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        recordR = "INSERT INTO ShortTradingSigR VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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

        record = "INSERT INTO LongTradingSig VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        recordR = "INSERT INTO LongTradingSigR VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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

        nowdat = datetime.now()

        Termy = (f"Execution of PullOff Module Has Completed Successfully.\n"
                 f"\n"
                 f"{nowdat}")

        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        MTrecord2 = 'UPDATE Exception_Terminal SET Trad_OEM = "idle" WHERE PK = "Status" '
        my_cursor.execute(MTrecord2)

        Database.commit()

    except Exception as e:
        import smtplib
        import ssl
        from email.message import EmailMessage

        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = ""
        receiver_email = ""
        password = ''

        errstr = (f"Exception:\n"
                  f"\n"
                  f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                  f"{e}\n"
                  f"\n"
                  f"\n"
                  f"Traceback:\n"
                  f"\n"
                  f"{traceback.format_exc()}\n"
                  f"\n")

        Term = Term + errstr

        msg = EmailMessage()

        msg.set_content(f"PullOfModule.py is experiencing Problems.\n"
                        f"\n"
                        f"Report:\n"
                        f"\n"
                        f"{Term}\n"
                        f"\n")

        msg['Subject'] = "Briareos Module Error"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)

        MTrecord = f"UPDATE Exception_Terminal SET Trad_OEM = '{Term}' WHERE PK = 'Terminal'"
        my_cursor.execute(MTrecord)

        MTrecord2 = 'UPDATE Exception_Terminal SET Trad_OEM = "error" WHERE PK = "Status" '
        my_cursor.execute(MTrecord2)

        Database.commit()

