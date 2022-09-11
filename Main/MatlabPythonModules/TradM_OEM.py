# This module is responsible for generating and executing trading orders (Buy\sell), thus earning the name Order
# Execution Module. It guarantees the proper accounting of two separate portfolios that are in fact a single portfolio
# on an exchange (here binance). IT also executes the scheduled withdrawal of part fo the total funds on the Exchange

def tradingmodule():

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
        import math as mt
        from datetime import date, timedelta, datetime
        import pandas
        from binance.client import Client
        from binance.exceptions import BinanceAPIException
        import time
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

        def trunc1(x):
            a = np.trunc(x * 10) / 10
            return a

        def trunc2(x):
            a = np.trunc(x * 100) / 100
            return a

        def trunc3(x):
            a = np.trunc(x * 1000) / 1000
            return a

        def trunc4(x):
            a = np.trunc(x * 10000) / 10000
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

        query = f"SELECT adjust, payout " \
                f"FROM ExecutionCom " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        adjust = col[0][0]
        payt = col[0][1]

        # Trading Module (System 3)

        # Short-Term Trading
        nowdat = datetime.now()
        Term = (f"{nowdat}\n"
                f"\n"
                f"Trading Signals Modules Running ...\n"
                f"\n"
                f"Short Term Trading Running ...\n"
                f"\n")

        MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM= "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        metric = ['close', 'high', 'low', 'volume']
        Mvar = ['sPdc', 'sPdh', 'sPdl', 'sPdvol']
        sPdcnp = np.zeros((1100, len(Cry_str)))
        sPdhnp = np.zeros((1100, len(Cry_str)))
        sPdlnp = np.zeros((1100, len(Cry_str)))
        sPdvolnp = np.zeros((1100, len(Cry_str)))
        j = 0
        for metrc in metric:
            r = 0
            for crypto in Cry_str:
                query = f"SELECT {metrc} " \
                        f"FROM {crypto}h " \
                        f"ORDER BY date DESC " \
                        f"LIMIT 1100 "
                my_cursor.execute(query)
                col = my_cursor.fetchall()
                Col = [item for sublist in [list(i) for i in col] for item in sublist]
                list.reverse(Col)
                vars()[f"{Mvar[j]}np"][:, r] = Col
                r += 1
            j += 1

        sPdc = matlab.double(np.ndarray.tolist(sPdcnp))
        sPdh = matlab.double(np.ndarray.tolist(sPdhnp))
        sPdl = matlab.double(np.ndarray.tolist(sPdlnp))
        sPdvol = matlab.double(np.ndarray.tolist(sPdvolnp))

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        dta = ['SvarMACD', 'SvarOBV', 'SvarADL', 'SvarATR', 'SvarOSC', 'SvarCCI', 'SStrt']
        SvarOSCnp = np.zeros((7, 2))
        SvarMACDnp = np.zeros((7, 3))
        SvarOBVnp = np.zeros((7, 3))
        SvarADLnp = np.zeros((7, 3))
        SvarATRnp = np.zeros((7, 3))
        SvarCCInp = np.zeros((7, 2))
        SStrtnp = np.zeros((7, 22))
        for data in dta:
            j = 0
            for crypto in Cry_str:
                if  data == 'SvarOSC' or data == 'SvarCCI':
                    query = f"SELECT a, b "\
                            f"FROM {crypto}_{data} "\
                            f"ORDER BY date DESC "\
                            f"LIMIT 1 "
                    my_cursor.execute(query)
                    col = my_cursor.fetchall()
                    Col = [list(item) for item in col]
                    vars()[f"{data}np"][j, :] = np.asarray(Col)
                    j += 1
                elif data == 'SStrt':
                    query = f"SELECT a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v "\
                            f"FROM {crypto}_{data} "\
                            f"ORDER BY date DESC "\
                            f"LIMIT 1 "
                    my_cursor.execute(query)
                    col = my_cursor.fetchall()
                    Col = [list(item) for item in col]
                    SStrtnp[j, :] = np.asarray(Col)
                    j += 1
                else:
                    query = f"SELECT a, b, c "\
                            f"FROM {crypto}_{data} "\
                            f"ORDER BY date DESC "\
                            f"LIMIT 1 "
                    my_cursor.execute(query)
                    col = my_cursor.fetchall()
                    Col = [list(item) for item in col]
                    vars()[f"{data}np"][j, :] = np.asarray(Col)
                    j += 1

        SvarOSC = matlab.double(np.ndarray.tolist(SvarOSCnp))
        SvarMACD = matlab.double(np.ndarray.tolist(SvarMACDnp))
        SvarOBV = matlab.double(np.ndarray.tolist(SvarOBVnp))
        SvarADL = matlab.double(np.ndarray.tolist(SvarADLnp))
        SvarATR = matlab.double(np.ndarray.tolist(SvarATRnp))
        SvarCCI = matlab.double(np.ndarray.tolist(SvarCCInp))
        SStrt = matlab.double(np.ndarray.tolist(SStrtnp))

        query = f"SELECT SPort, BTCSP, ETHSP, XLMSP, XMRSP, XRPSP, LINKSP, NEOSP "\
                f"FROM PortfolioOptS " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Port = np.asarray(Col[0])
        SPort = matlab.double([Port[0]])
        SAPort = matlab.double(np.ndarray.tolist(Port[1:]))

        [ShortGSignal, RShortGSignal] = eng.ShortTrading(sPdc, sPdh, sPdl, sPdvol, SvarMACD, SvarOBV, SvarADL, SvarATR,
                                                         SvarOSC, SvarCCI, SStrt, SPort, SAPort, nargout=2)

        record = "INSERT IGNORE INTO ShortTradingSig VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        recordR = "INSERT IGNORE INTO ShortTradingSigR VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        nowr = datetime.now()
        dat = datetime(nowr.year, nowr.month, nowr.day, nowr.hour)
        val = [float(i) for i in ShortGSignal[0]]
        valR = [float(i) for i in RShortGSignal[0]]
        valu = [dat] + val
        valuR = [dat] + valR
        value = tuple(valu)
        valueR = tuple(valuR)
        my_cursor.execute(record, value)
        my_cursor.execute(recordR, valueR)
        Database.commit()


        # Long-Term Trading

        TermTS = "Short Term Trading Signals Generated"
        TermTL1 = "Long Term Trading Starting ..."
        Term = (f"{nowdat}\n"
                f"\n"
                f"Trading Signals Modules Running ...\n"
                f"\n"
                f"Short Term Trading Running ...\n"
                f"\n"
                f"{TermTS}\n"
                f"\n"
                f"\n"
                f"{TermTL1}\n"
                f"\n")

        MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        if datetime.now().hour == 0 or adjust == 1:

            Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
            metric = ['close', 'high', 'low', 'volume']
            Mvar = ['lPdc', 'lPdh', 'lPdl', 'lPdvol']
            lPdcnp = np.zeros((650, len(Cry_str)))
            lPdhnp = np.zeros((650, len(Cry_str)))
            lPdlnp = np.zeros((650, len(Cry_str)))
            lPdvolnp = np.zeros((650, len(Cry_str)))
            j = 0
            for metrc in metric:
                r = 0
                for crypto in Cry_str:
                    query = f"SELECT {metrc} " \
                            f"FROM {crypto}d " \
                            f"ORDER BY date DESC " \
                            f"LIMIT 650 "
                    my_cursor.execute(query)
                    col = my_cursor.fetchall()
                    Col = [item for sublist in [list(i) for i in col] for item in sublist]
                    list.reverse(Col)
                    vars()[f"{Mvar[j]}np"][:, r] = Col
                    r += 1
                j += 1

            lPdc = matlab.double(np.ndarray.tolist(lPdcnp))
            lPdh = matlab.double(np.ndarray.tolist(lPdhnp))
            lPdl = matlab.double(np.ndarray.tolist(lPdlnp))
            lPdvol = matlab.double(np.ndarray.tolist(lPdvolnp))


            Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
            dta = ['LvarMACD', 'LvarOBV', 'LvarADL', 'LvarATR', 'LvarOSC', 'LvarCCI', 'LStrt']
            LvarOSCnp = np.zeros((7, 2))
            LvarMACDnp = np.zeros((7, 3))
            LvarOBVnp = np.zeros((7, 3))
            LvarADLnp = np.zeros((7, 3))
            LvarATRnp = np.zeros((7, 3))
            LvarCCInp = np.zeros((7, 2))
            LStrtnp = np.zeros((7, 22))
            for data in dta:
                j = 0
                for crypto in Cry_str:
                    if  data == 'LvarOSC' or data == 'LvarCCI':
                        query = f"SELECT a, b "\
                                f"FROM {crypto}_{data} "\
                                f"ORDER BY date DESC "\
                                f"LIMIT 1 "
                        my_cursor.execute(query)
                        col = my_cursor.fetchall()
                        Col = [list(item) for item in col]
                        vars()[f"{data}np"][j, :] = np.asarray(Col)
                    elif data == 'LStrt':
                        query = f"SELECT a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v "\
                                f"FROM {crypto}_{data} "\
                                f"ORDER BY date DESC "\
                                f"LIMIT 1 "
                        my_cursor.execute(query)
                        col = my_cursor.fetchall()
                        Col = [list(item) for item in col]
                        LStrtnp[j, :] = np.asarray(Col)
                    else:
                        query = f"SELECT a, b, c "\
                                f"FROM {crypto}_{data} "\
                                f"ORDER BY date DESC "\
                                f"LIMIT 1 "
                        my_cursor.execute(query)
                        col = my_cursor.fetchall()
                        Col = [list(item) for item in col]
                        vars()[f"{data}np"][j, :] = np.asarray(Col)
                    j += 1

            LvarOSC = matlab.double(np.ndarray.tolist(LvarOSCnp))
            LvarMACD = matlab.double(np.ndarray.tolist(LvarMACDnp))
            LvarOBV = matlab.double(np.ndarray.tolist(LvarOBVnp))
            LvarADL = matlab.double(np.ndarray.tolist(LvarADLnp))
            LvarATR = matlab.double(np.ndarray.tolist(LvarATRnp))
            LvarCCI = matlab.double(np.ndarray.tolist(LvarCCInp))
            LStrt = matlab.double(np.ndarray.tolist(LStrtnp))

            query = f"SELECT LPort, BTCLP, ETHLP, XLMLP, XMRLP, XRPLP, LINKLP, NEOLP "\
                    f"FROM PortfolioOptL " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            Port = np.asarray(Col)[0]
            LPort = matlab.double([Port[0]])
            LAPort = matlab.double(np.ndarray.tolist(Port[1:]))

            query = f"SELECT Inception_Date " \
                    f"FROM Miscellaneous " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            inceptdate = col[0][0]
            daycount = matlab.double([(date.today() - inceptdate).days])

            [LongGSignal, RLongGSignal] = eng.LongTrading(lPdc, lPdh, lPdl, lPdvol,
                                                          LvarMACD, LvarOBV, LvarADL, LvarATR, LvarOSC, LvarCCI,
                                                          LStrt, LPort, LAPort, nargout=2)

            record = "INSERT IGNORE INTO LongTradingSig VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            recordR = "INSERT IGNORE INTO LongTradingSigR VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            nowr = datetime.now()
            dat = datetime(nowr.year, nowr.month, nowr.day, nowr.hour)
            val = [float(i) for i in LongGSignal[0]]
            valR = [float(i) for i in RLongGSignal[0]]
            valu = [dat] + val
            valuR = [dat] + valR
            value = tuple(valu)
            valueR = tuple(valuR)
            my_cursor.execute(record, value)
            my_cursor.execute(recordR, valueR)

            Database.commit()

        else:

            query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM LongTradingSig " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            LSIG = my_cursor.fetchall()

            query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM LongTradingSigR " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            LSIGR = my_cursor.fetchall()

            record = "INSERT IGNORE INTO LongTradingSig VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            recordR = "INSERT IGNORE INTO LongTradingSigR VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            nowr = datetime.now()
            dat = datetime(nowr.year, nowr.month, nowr.day, nowr.hour)
            value = (dat,) + LSIG[0]
            valueR = (dat,) + LSIGR[0]
            my_cursor.execute(record, value)
            my_cursor.execute(recordR, valueR)
            Database.commit()

        time.sleep(7)

        TermTL2 = "Long Term Trading Signal Generated"
        Term = (f"{nowdat}\n"
                f"\n"
                f"Trading Signals Modules Running ...\n"
                f"\n"
                f"Short Term Trading Running ...\n"
                f"\n"
                f"{TermTS}\n"
                f"\n"
                f"\n"
                f"{TermTL1}\n"
                f"\n"
                f"{TermTL2}\n"
                f"\n"
                f"\n"
                f"Execution of Trading Signals Modules Completed Successfully\n"
                f"\n"
                f"\n"
                f"Starting Order Execution Module ...\n"
                f"\n")

        MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()


        # Order Execution Module

        Termy = ("Trading Starting ...\n"
                 "\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        client = Client("",
                        "")

        # Data
        query = f"SELECT LPort, BTCLP, ETHLP, XLMLP, XMRLP, XRPLP, LINKLP, NEOLP " \
                f"FROM PortfolioOptL " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Port = np.asarray(Col)[0]
        LPort = Port[0]

        query = f"SELECT SPort, BTCSP, ETHSP, XLMSP, XMRSP, XRPSP, LINKSP, NEOSP " \
                f"FROM PortfolioOptS " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Port = np.asarray(Col)[0]
        SPort = Port[0]

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM ShortTradingSig " \
                f"ORDER BY date DESC " \
                f"LIMIT 2 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Port = np.asarray(Col)
        SSign = np.ndarray.tolist(Port[0, :])
        SSigo = np.ndarray.tolist(Port[1, :])

        query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                f"FROM LongTradingSig " \
                f"ORDER BY date DESC " \
                f"LIMIT 2 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        Port = np.asarray(Col)
        LSign = np.ndarray.tolist(Port[0, :])
        LSigo = np.ndarray.tolist(Port[1, :])

        ln = len(LSign)

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        Cry_strn = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO', 'USDT']
        Cry_strO = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']

        truncatefunc = [trunc5, trunc4, np.floor, trunc3, np.floor, trunc2, trunc2]

        # Port-Adjuster Sub-Module (Selling):

        if adjust == 1:

            Termy = ("Portfolio Adjuster Sub-Module Running ...\n"
                     "\n"
                     "Port-Adjust Selling Process Starting ...\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

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
                    f"FROM BuyPrices " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            lstbp = np.asarray(Col)[0]

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

            # (Selling)
            lserr=[]
            lserrval=[]
            vals = np.zeros((1, len(Cry_str)))[0]
            Svals = np.zeros((1, len(Cry_str)))[0]
            Lvals = np.zeros((1, len(Cry_str)))[0]
            valsp = np.zeros((1, len(Cry_str)))[0]
            Svalsp = np.zeros((1, len(Cry_str)))[0]
            Lvalsp = np.zeros((1, len(Cry_str)))[0]
            for i in range(ln):
                sprices = []
                s = 0
                TotalFunds = 0
                ordbk = pandas.DataFrame(client.get_orderbook_tickers())
                ordbk = ordbk.set_index('symbol')
                bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
                for crypto in Cry_strn:
                    if crypto == 'USDT':
                        vap = client.get_asset_balance(asset=crypto)
                        vas = float(vap['free'])
                        USDTF = vas
                    else:
                        sprices += [float(bidaskprice.loc[f'{Cry_strO[s]}', 'bidPrice'])]
                        vap = client.get_asset_balance(asset=crypto)
                        vas = (float(vap['free']) + float(vap['locked'])) * sprices[s]
                    TotalFunds += trunc8(vas)
                    s += 1
                lpri = np.asarray(Llstb[i]*sprices[i]/TotalFunds)
                spri = np.asarray(Slstb[i]*sprices[i]/TotalFunds)

                if (SSign[i] != SSigo[i]) and (LSign[i] == LSigo[i]):
                    sigpri = SSign[i]/spri
                    if np.isnan(sigpri) == 1 or np.isinf(sigpri) == 1:
                        sigpri = 0
                    OV=Slstb[i]*(sigpri-1)
                    ordS = truncatefunc[i](abs(OV))
                    if OV<0 and ordS*sprices[i] > 10:
                        try:
                            order = client.order_market_sell(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                    [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'SELL':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty'])
                            Svals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                            Svalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Sell Order scrubbed for {Cry_strO[i]}_S.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Sell Order scrubbed for {Cry_strO[i]}_S. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [ordS]
                elif (SSign[i] != SSigo[i]) and (LSign[i] != LSigo[i]):
                    lVa=0
                    lVap=0
                    sVa=0
                    sVap=0
                    sigpri = SSign[i]/spri
                    if np.isnan(sigpri) == 1 or np.isinf(sigpri) == 1:
                        sigpri = 0
                    OVs=truncatefunc[i](Slstb[i]*(sigpri-1))
                    sigpri = LSign[i]/lpri
                    if np.isnan(sigpri) == 1 or np.isinf(sigpri) == 1:
                        sigpri = 0
                    OVl=truncatefunc[i](Llstb[i]*(sigpri-1))
                    sordS = abs(OVs)
                    lordS = abs(OVl)
                    ordId1 = []
                    if OVs < 0 and sordS * sprices[i] > 10:
                        try:
                            order = client.order_market_sell(symbol=Cry_strO[i], quantity=sordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'SELL':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                ordId1 = Bdta[0]['orderId']
                                sde = Bdta[0]['side']

                            sVa = float(Bdta[0]['executedQty'])
                            Svals[i] = sVa
                            sVap = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                            Svalsp[i] = sVap
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Sell Order scrubbed for {Cry_strO[i]}_S.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Sell Order scrubbed for {Cry_strO[i]}_S. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [sordS]

                    if OVl<0 and lordS*sprices[i] > 10:
                        try:
                            order = client.order_market_sell(symbol=Cry_strO[i], quantity=lordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            if ordId1:
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']
                                while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                       [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                        or sde != 'SELL':
                                    time.sleep(0.5)
                                    Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                    dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                    sde = Bdta[0]['side']
                            else:
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                ordId = Bdta[0]['orderId']
                                while ordId==ordId1:
                                    time.sleep(0.5)
                                    Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                    ordId = Bdta[0]['orderId']

                            lVa = float(Bdta[0]['executedQty'])
                            Lvals[i] = lVa
                            lVap = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                            Lvalsp[i] = lVap
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Sell Order scrubbed for {Cry_strO[i]}_L.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Sell Order scrubbed for {Cry_strO[i]}_L. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [trunc8(lordS)]

                    vals[i] = sVa + lVa
                    valsp[i] = sVap + lVap
                elif (SSign[i] == SSigo[i]) and (LSign[i] != LSigo[i]):
                    sigpri = LSign[i]/lpri
                    if np.isnan(sigpri) == 1 or np.isinf(sigpri) == 1:
                        sigpri = 0
                    OV=Llstb[i]*(sigpri-1)
                    ordS = truncatefunc[i](abs(OV))
                    if OV<0 and ordS*sprices[i] > 10:
                        try:
                            order = client.order_market_sell(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                    [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour])  \
                                    or sde != 'SELL':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty'])
                            Lvals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                            Lvalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Sell Order scrubbed for {Cry_strO[i]}_L.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Sell Order scrubbed for {Cry_strO[i]}_L. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [trunc8(ordS)]


            bupdt = lstb - vals
            Sbupdt = Slstb - Svals
            Lbupdt = Llstb - Lvals

            buyper = abs(vals/lstb)
            sbuyper = abs(Svals/Slstb)
            lbuyper = abs(Lvals/Llstb)
            buyper[(np.isnan(buyper)) | (np.isinf(buyper))] = 0
            sbuyper[(np.isnan(sbuyper)) | (np.isinf(sbuyper))] = 0
            lbuyper[(np.isnan(lbuyper)) | (np.isinf(lbuyper))] = 0

            Sbupdtp = Slstbp * (1-sbuyper)
            Lbupdtp = Llstbp * (1-lbuyper)
            bupdtp = Sbupdtp + Lbupdtp

            Sprofit = -Slstbp*sbuyper + Svalsp
            Lprofit = -Llstbp*lbuyper + Lvalsp
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

            EMrecord = f"UPDATE BuyValues SET BTC={bupdt[0]}, ETH={bupdt[1]}, XLM={bupdt[2]}, XMR={bupdt[3]}," \
                       f" XRP={bupdt[4]}, LINK={bupdt[5]}, NEO={bupdt[6]}"
            SEMrecord = f"UPDATE BuyValues_short SET BTC={Sbupdt[0]}, ETH={Sbupdt[1]}, XLM={Sbupdt[2]}, XMR={Sbupdt[3]}," \
                        f" XRP={Sbupdt[4]}, LINK={Sbupdt[5]}, NEO={Sbupdt[6]}"
            LEMrecord = f"UPDATE BuyValues_long SET BTC={Lbupdt[0]}, ETH={Lbupdt[1]}, XLM={Lbupdt[2]}, XMR={Lbupdt[3]}," \
                        f" XRP={Lbupdt[4]}, LINK={Lbupdt[5]}, NEO={Lbupdt[6]}"
            my_cursor.execute(EMrecord)
            my_cursor.execute(SEMrecord)
            my_cursor.execute(LEMrecord)

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

            Termy = ("Port-Adjust Selling Process Executed.\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)

            Database.commit()

            # Buying

            Termy = ("Port-Adjust Buying Process Starting ...\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

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
                    f"FROM BuyPrices " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            lstbp = np.asarray(Col)[0]

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
            for i in range(ln):
                bprices = []
                s = 0
                TotalFunds = 0
                ordbk = pandas.DataFrame(client.get_orderbook_tickers())
                ordbk = ordbk.set_index('symbol')
                bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
                for crypto in Cry_strn:
                    if crypto == 'USDT':
                        vap = client.get_asset_balance(asset=crypto)
                        vas = float(vap['free'])
                        USDTF = vas-0.5
                    else:
                        bprices += [float(bidaskprice.loc[f'{Cry_strO[s]}', 'askPrice'])]
                        vap = client.get_asset_balance(asset=crypto)
                        vas = (float(vap['free']) + float(vap['locked'])) * bprices[s]
                    if vas > 10:
                        TotalFunds += trunc8(vas)
                    else:
                        TotalFunds += 0
                    s += 1

                if (SSign[i] != SSigo[i]) and (LSign[i] == LSigo[i]):
                    OV = truncatefunc[i]((SSign[i]*TotalFunds/bprices[i])-Slstb[i])
                    if OV > 0 and OV * bprices[i] > 10:
                        s = 0
                        bprices[i] = 0
                        iordS = 0
                        ordS = 0
                        pordS = 0
                        tbprices = 0
                        ORDBK = client.get_order_book(symbol=f'{Cry_strO[i]}', limit=10)
                        bORDBK = ORDBK['asks']
                        while ordS < OV:
                            ords = float(bORDBK[s][1])
                            pords = float(bORDBK[s][0])
                            iordS += ords
                            if iordS > OV:
                                tbprices += ((USDTF - pordS) / USDTF) * pords
                                pordS += (OV - ordS) * pords
                                bprices[i] += ((OV - ordS) / OV) * pords
                                ordS += OV - ordS
                            else:
                                pordS += ords * pords
                                ordS += ords
                                bprices[i] += (ords / OV) * pords
                                tbprices += (ords * pords * pords) / USDTF
                            s += 1
                        ordS = truncatefunc[i](ordS)
                        if trunc8(pordS) > USDTF:
                            bprices[i] = tbprices
                            ordS = truncatefunc[i](USDTF / bprices[i])
                        try:
                            order = client.order_market_buy(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                    [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'BUY':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty']) * 0.999
                            Svals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty'])
                            Svalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Buy Order scrubbed for {Cry_strO[i]}_S.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Buy Order scrubbed for {Cry_strO[i]}_S. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [ordS*bprices[i]]
                elif (SSign[i] != SSigo[i]) and (LSign[i] != LSigo[i]):
                    lVa = 0
                    lVap = 0
                    sVa = 0
                    sVap = 0
                    OVs = truncatefunc[i]((SSign[i] * TotalFunds / bprices[i]) - Slstb[i])
                    OVl = truncatefunc[i]((LSign[i] * TotalFunds / bprices[i]) - Llstb[i])
                    ordId1 = []
                    if OVs > 0 and OVs * bprices[i] > 10:
                        s = 0
                        bprices[i] = 0
                        iordS = 0
                        sordS = 0
                        spordS = 0
                        tbprices = 0
                        ORDBK = client.get_order_book(symbol=f'{Cry_strO[i]}', limit=10)
                        bORDBK = ORDBK['asks']
                        while sordS < OVs:
                            ords = float(bORDBK[s][1])
                            pords = float(bORDBK[s][0])
                            iordS += ords
                            if iordS > OVs:
                                tbprices += ((USDTF - spordS) / USDTF) * pords
                                spordS += (OVs - sordS) * pords
                                bprices[i] += ((OVs - sordS) / OVs) * pords
                                sordS += OVs - sordS
                            else:
                                spordS += ords * pords
                                sordS += ords
                                bprices[i] += (ords / OVs) * pords
                                tbprices += (ords * pords * pords) / USDTF
                            s += 1
                        sordS = truncatefunc[i](sordS)
                        if trunc8(spordS) > USDTF:
                            bprices[i] = tbprices
                            sordS = truncatefunc[i](USDTF / bprices[i])
                        try:
                            order = client.order_market_buy(symbol=Cry_strO[i], quantity=sordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'BUY':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                ordId1 = Bdta[0]['orderId']
                                sde = Bdta[0]['side']

                            sVa = float(Bdta[0]['executedQty']) * 0.999
                            Svals[i] = sVa
                            sVap = float(Bdta[0]['cummulativeQuoteQty'])
                            Svalsp[i] = sVap
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Buy Order scrubbed for {Cry_strO[i]}_S.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Buy Order scrubbed for {Cry_strO[i]}_S. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [sordS*bprices[i]]
                    vap = client.get_asset_balance(asset=crypto)
                    USDTF = float(vap['free'])-0.5
                    if OVl > 0 and OVl * bprices[i] > 10:
                        s = 0
                        bprices[i] = 0
                        iordS = 0
                        lordS = 0
                        lpordS = 0
                        tbprices = 0
                        ORDBK = client.get_order_book(symbol=f'{Cry_strO[i]}', limit=10)
                        bORDBK = ORDBK['asks']
                        while lordS < OVl:
                            ords = float(bORDBK[s][1])
                            pords = float(bORDBK[s][0])
                            iordS += ords
                            if iordS > OVl:
                                tbprices += ((USDTF - lpordS) / USDTF) * pords
                                lpordS += (OVl - lordS) * pords
                                bprices[i] += ((OVl - lordS) / OVl) * pords
                                lordS += OVl - lordS
                            else:
                                lpordS += ords * pords
                                lordS += ords
                                bprices[i] += (ords / OVl) * pords
                                tbprices += (ords * pords * pords) / USDTF
                            s += 1
                        lordS = truncatefunc[i](lordS)
                        if trunc8(lpordS) > USDTF:
                            bprices[i] = tbprices
                            lordS = truncatefunc[i](USDTF / bprices[i])
                        try:
                            order = client.order_market_buy(symbol=Cry_strO[i], quantity=lordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            if ordId1:
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']
                                while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                       [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                        or sde != 'BUY':
                                    time.sleep(0.5)
                                    Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                    dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                    sde = Bdta[0]['side']
                            else:
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                ordId = Bdta[0]['orderId']
                                while ordId==ordId1:
                                    time.sleep(0.5)
                                    Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                    ordId = Bdta[0]['orderId']

                            lVa = float(Bdta[0]['executedQty']) * 0.999
                            Lvals[i] = lVa
                            lVap = float(Bdta[0]['cummulativeQuoteQty'])
                            Lvalsp[i] = lVap
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Buy Order scrubbed for {Cry_strO[i]}_L.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Buy Order scrubbed for {Cry_strO[i]}_L. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [lordS*bprices[i]]

                    vals[i] = sVa + lVa
                    valsp[i] = sVap + lVap
                elif (SSign[i] == SSigo[i]) and (LSign[i] != LSigo[i]):
                    OV = truncatefunc[i]((LSign[i] * TotalFunds / bprices[i]) - Llstb[i])
                    if OV > 0 and OV * bprices[i] > 10:
                        s = 0
                        bprices[i] = 0
                        iordS = 0
                        ordS = 0
                        pordS = 0
                        tbprices = 0
                        ORDBK = client.get_order_book(symbol=f'{Cry_strO[i]}', limit=10)
                        bORDBK = ORDBK['asks']
                        while ordS < OV:
                            ords = float(bORDBK[s][1])
                            pords = float(bORDBK[s][0])
                            iordS += ords
                            if iordS > OV:
                                tbprices += ((USDTF - pordS) / USDTF) * pords
                                pordS += (OV - ordS) * pords
                                bprices[i] += ((OV - ordS) / OV) * pords
                                ordS += OV - ordS
                            else:
                                pordS += ords * pords
                                ordS += ords
                                bprices[i] += (ords / OV) * pords
                                tbprices += (ords * pords * pords) / USDTF
                            s += 1
                        ordS = truncatefunc[i](ordS)
                        if trunc8(pordS) > USDTF:
                            bprices[i] = tbprices
                            ordS = truncatefunc[i](USDTF / bprices[i])
                        try:
                            order = client.order_market_buy(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'BUY':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty']) * 0.999
                            Lvals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty'])
                            Lvalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Buy Order scrubbed for {Cry_strO[i]}_L.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Buy Order scrubbed for {Cry_strO[i]}_L. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [ordS*bprices[i]]

            bupdt = lstb + vals
            Sbupdt = Slstb + Svals
            Lbupdt = Llstb + Lvals

            bupdtp = lstbp + valsp
            Sbupdtp = Slstbp + Svalsp
            Lbupdtp = Llstbp + Lvalsp

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

            EMrecord = "UPDATE ExecutionCom SET adjust = 0"
            my_cursor.execute(EMrecord)

            Termy = ("Port-Adjust Buying Process Executed. \n"
                     "\n"
                     "Portfolio Adjuster Sub-Module Executed Successfully.\n"
                     "\n"
                     "Trading Process Executed Successfully.\n"
                     "\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)

            Database.commit()

        else:

            Termy = ("Selling Process Starting ...\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

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
                    f"FROM BuyPrices " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            lstbp = np.asarray(Col)[0]

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

            lserr=[]
            lserrval=[]
            vals = np.zeros((1, len(Cry_str)))[0]
            Svals = np.zeros((1, len(Cry_str)))[0]
            Lvals = np.zeros((1, len(Cry_str)))[0]
            valsp = np.zeros((1, len(Cry_str)))[0]
            Svalsp = np.zeros((1, len(Cry_str)))[0]
            Lvalsp = np.zeros((1, len(Cry_str)))[0]
            for i in range(ln):
                ordbk = pandas.DataFrame(client.get_orderbook_tickers())
                ordbk = ordbk.set_index('symbol')
                bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
                sprices = float(bidaskprice.loc[f'{Cry_strO[i]}', 'bidPrice'])
                if (SSign[i] == 0 and SSigo[i] != 0) and (LSign[i] != 0 or LSigo[i] == 0):
                    ordS = truncatefunc[i](Slstb[i])
                    if ordS*sprices > 10:
                        try:
                            order = client.order_market_sell(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour])\
                                    or sde != 'SELL':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty'])
                            Svals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                            Svalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Sell Order scrubbed for {Cry_strO[i]}_S.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Sell Order scrubbed for {Cry_strO[i]}_S. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [ordS]
                elif (SSign[i] == 0 and SSigo[i] != 0) and (LSign[i] == 0 and LSigo[i] != 0):
                    ordS = truncatefunc[i](lstb[i])
                    if ordS*sprices > 10:
                        try:
                            order = client.order_market_sell(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'SELL':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty'])
                            Svals[i] = (Slstb[i]/(Slstb[i]+Llstb[i])) * vals[i]
                            Lvals[i] = (Llstb[i]/(Slstb[i]+Llstb[i])) * vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                            Svalsp[i] = (Slstb[i]/(Slstb[i]+Llstb[i])) * valsp[i]
                            Lvalsp[i] = (Llstb[i]/(Slstb[i]+Llstb[i])) * valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
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

                            msg['Subject'] = "Briareos.binance Trading Error"
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
                elif (SSign[i] != 0 or SSigo[i] == 0) and (LSign[i] == 0 and LSigo[i] != 0):
                    ordS = truncatefunc[i](Llstb[i])
                    if ordS*sprices > 10:
                        try:
                            order = client.order_market_sell(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'SELL':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty'])
                            Lvals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                            Lvalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Sell Order scrubbed for {Cry_strO[i]}_L.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Sell Order scrubbed for {Cry_strO[i]}_L. Check Email for more information.\n"
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

            buyper = abs(vals/lstb)
            sbuyper = abs(Svals/Slstb)
            lbuyper = abs(Lvals/Llstb)
            buyper[(np.isnan(buyper)) | (np.isinf(buyper))] = 0
            sbuyper[(np.isnan(sbuyper)) | (np.isinf(sbuyper))] = 0
            lbuyper[(np.isnan(lbuyper)) | (np.isinf(lbuyper))] = 0

            Sbupdtp = Slstbp * (1-sbuyper)
            Lbupdtp = Llstbp * (1-lbuyper)
            bupdtp = Sbupdtp + Lbupdtp

            Sprofit = -Slstbp*sbuyper + Svalsp
            Lprofit = -Llstbp*lbuyper + Lvalsp
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
                msg.set_content(f"\n"
                                f"\n"
                                f"Some (Trading) Selling Transaction where lower than 10$.\n"
                                f"\n"
                                f"Assets:\n"
                                f"{lserr}\n"
                                f"\n"
                                f"Values:\n"
                                f"{lserrval}\n"
                                f"\n"
                                f"Signals:\n"
                                f"S (o-n):\n"
                                f"{SSigo}\n"
                                f"{SSign}\n"
                                f"\n"
                                f"L (o-n):\n"
                                f"{LSigo}\n"
                                f"{SSign}\n"
                                f"\n")
                msg['Subject'] = " Briareos Trade Scrubbed"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)

            Termy = ("Selling Process Executed.\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)

            Database.commit()

            # Buying:

            Termy = ("Buying Process Starting ...\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)

            Database.commit()

            query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM BuyPrices " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            lstbp = np.asarray(Col)[0]

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

            lserr = []
            lserrval = []
            vals = np.zeros((1, len(Cry_str)))[0]
            Svals = np.zeros((1, len(Cry_str)))[0]
            Lvals = np.zeros((1, len(Cry_str)))[0]
            valsp = np.zeros((1, len(Cry_str)))[0]
            Svalsp = np.zeros((1, len(Cry_str)))[0]
            Lvalsp = np.zeros((1, len(Cry_str)))[0]
            for i in range(ln):
                bprices = []
                s = 0
                TotalFunds = 0
                ordbk = pandas.DataFrame(client.get_orderbook_tickers())
                ordbk = ordbk.set_index('symbol')
                bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
                for crypto in Cry_strn:
                    if crypto == 'USDT':
                        vap = client.get_asset_balance(asset=crypto)
                        vas = float(vap['free'])
                        USDTF = vas-0.5
                    else:
                        bprices += [float(bidaskprice.loc[f'{Cry_strO[s]}', 'askPrice'])]
                        vap = client.get_asset_balance(asset=crypto)
                        vas = (float(vap['free']) + float(vap['locked'])) * bprices[s]
                    if vas > 10:
                        TotalFunds += trunc8(vas)
                    else:
                        TotalFunds += 0
                    s += 1
                if (SSign[i] != 0 and SSigo[i] == 0) and not (LSign[i] != 0 and LSigo[i] == 0):
                    OV = truncatefunc[i](SSign[i] * TotalFunds / bprices[i])
                    s = 0
                    bprices[i] = 0
                    iordS = 0
                    ordS = 0
                    pordS = 0
                    tbprices = 0
                    ORDBK = client.get_order_book(symbol=f'{Cry_strO[i]}', limit=10)
                    bORDBK = ORDBK['asks']
                    while ordS < OV:
                        ords = float(bORDBK[s][1])
                        pords = float(bORDBK[s][0])
                        iordS += ords
                        if iordS > OV:
                            tbprices += ((USDTF-pordS)/USDTF) * pords
                            pordS += (OV - ordS) * pords
                            bprices[i] += ((OV - ordS) / OV) * pords
                            ordS += OV - ordS
                        else:
                            pordS += ords * pords
                            ordS += ords
                            bprices[i] += (ords / OV) * pords
                            tbprices += (ords*pords*pords)/USDTF
                        s += 1
                    ordS = truncatefunc[i](ordS)
                    if trunc8(pordS) > USDTF:
                        bprices[i] = tbprices
                        ordS = truncatefunc[i](USDTF / bprices[i])
                        pordS = ordS * bprices[i]
                    if pordS > 10:
                        try:
                            order = client.order_market_buy(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour])\
                                    or sde != 'BUY':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty']) * 0.999
                            Svals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty'])
                            Svalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Buy Order scrubbed for {Cry_strO[i]}_S.\n"
                                            f"\n"
                                            f"value= {trunc8(pordS)} | {ordS}.\n"
                                            f"\n"
                                            f"USDTF= {USDTF}.\n"
                                            f"\n"
                                            f"totalfunds= {TotalFunds}.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Buy Order scrubbed for {Cry_strO[i]}_S. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [trunc8(pordS)]
                elif (SSign[i] != 0 and SSigo[i] == 0) and (LSign[i] != 0 and LSigo[i] == 0):
                    OV = truncatefunc[i]((SSign[i] + LSign[i]) * TotalFunds / bprices[i])
                    s = 0
                    bprices[i] = 0
                    iordS = 0
                    ordS = 0
                    pordS = 0
                    tbprices = 0
                    ORDBK = client.get_order_book(symbol=f'{Cry_strO[i]}', limit=10)
                    bORDBK = ORDBK['asks']
                    while ordS < OV:
                        ords = float(bORDBK[s][1])
                        pords = float(bORDBK[s][0])
                        iordS += ords
                        if iordS > OV:
                            tbprices += ((USDTF-pordS)/USDTF) * pords
                            pordS += (OV - ordS) * pords
                            bprices[i] += ((OV - ordS) / OV) * pords
                            ordS += OV - ordS
                        else:
                            pordS += ords * pords
                            ordS += ords
                            bprices[i] += (ords / OV) * pords
                            tbprices += (ords*pords*pords)/USDTF
                        s += 1
                    ordS = truncatefunc[i](ordS)
                    if trunc8(pordS) > USDTF:
                        bprices[i] = tbprices
                        ordS = truncatefunc[i](USDTF / bprices[i])
                        pordS = ordS * bprices[i]
                    if pordS > 10:
                        try:
                            order = client.order_market_buy(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'BUY':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty']) * 0.999
                            Svals[i] = SPort * vals[i]
                            Lvals[i] = LPort * vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty'])
                            Svalsp[i] = SPort * valsp[i]
                            Lvalsp[i] = LPort * valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Buy Order scrubbed for {Cry_strO[i]}_SL.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Buy Order scrubbed for {Cry_strO[i]}_SL. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [trunc8(pordS)]
                elif (LSign[i] != 0 and LSigo[i] == 0) and not (SSign[i] != 0 and SSigo[i] == 0):
                    OV = truncatefunc[i](LSign[i] * TotalFunds / bprices[i])
                    s = 0
                    bprices[i] = 0
                    iordS = 0
                    ordS = 0
                    pordS = 0
                    tbprices = 0
                    ORDBK = client.get_order_book(symbol=f'{Cry_strO[i]}', limit=10)
                    bORDBK = ORDBK['asks']
                    while ordS < OV:
                        ords = float(bORDBK[s][1])
                        pords = float(bORDBK[s][0])
                        iordS += ords
                        if iordS > OV:
                            tbprices += ((USDTF-pordS)/USDTF) * pords
                            pordS += (OV - ordS) * pords
                            bprices[i] += ((OV - ordS) / OV) * pords
                            ordS += OV - ordS
                        else:
                            pordS += ords * pords
                            ordS += ords
                            bprices[i] += (ords / OV) * pords
                            tbprices += (ords*pords*pords)/USDTF
                        s += 1
                    ordS = truncatefunc[i](ordS)
                    if trunc8(pordS) > USDTF:
                        bprices[i] = tbprices
                        ordS = truncatefunc[i](USDTF / bprices[i])
                        pordS = ordS * bprices[i]
                    if pordS > 10:
                        try:
                            order = client.order_market_buy(symbol=Cry_strO[i], quantity=ordS)

                            orders = 0
                            while orders != []:
                                orders = client.get_open_orders(symbol=Cry_strO[i])

                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            sde = Bdta[0]['side']
                            while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                                   [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                    or sde != 'BUY':
                                time.sleep(0.5)
                                Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                                dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                                sde = Bdta[0]['side']

                            vals[i] = float(Bdta[0]['executedQty']) * 0.999
                            Lvals[i] = vals[i]
                            valsp[i] = float(Bdta[0]['cummulativeQuoteQty'])
                            Lvalsp[i] = valsp[i]
                        except Exception as e:
                            msg = EmailMessage()
                            msg.set_content(f"Trading order resulted in error.\n"
                                            f"Buy Order scrubbed for {Cry_strO[i]}_L.\n"
                                            f"\n"
                                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                            f"{e}\n"
                                            f"\n"
                                            f"\n"
                                            f"Traceback:\n"
                                            f"\n"
                                            f"{traceback.format_exc()}"
                                            f"\n")

                            msg['Subject'] = "Briareos.binance Trading Error"
                            msg['From'] = sender_email
                            msg['To'] = receiver_email
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.send_message(msg)

                            Termy = (f"Buy Order scrubbed for {Cry_strO[i]}_L. Check Email for more information.\n"
                                     f"\n")
                            Term = Term + Termy
                            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                            my_cursor.execute(MTrecord)
                            Database.commit()
                    else:
                        lserr += [Cry_str[i]]
                        lserrval += [trunc8(pordS)]

            bupdt = lstb + vals
            Sbupdt = Slstb + Svals
            Lbupdt = Llstb + Lvals

            bupdtp = lstbp + valsp
            Sbupdtp = Slstbp + Svalsp
            Lbupdtp = Llstbp + Lvalsp

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
                msg.set_content(f"\n"
                                f"\n"
                                f"Some (Trading) Buying Transaction where lower than 10$.\n"
                                f"\n"
                                f"Assets:\n"
                                f"{lserr}\n"
                                f"\n"
                                f"Values:\n"
                                f"{lserrval}\n"
                                f"\n"
                                f"Signals:\n"
                                f"S (o-n):\n"
                                f"{SSigo}\n"
                                f"{SSign}\n"
                                f"\n"
                                f"L (o-n):\n"
                                f"{LSigo}\n"
                                f"{SSign}\n"
                                f"\n")
                msg['Subject'] = " Briareos Trade Scrubbed"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)

            Termy = ("Buying Process Executed.\n"
                     "\n"
                     "Trading Process Executed Successfully ...\n"
                     "\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)

            Database.commit()

        # Funds Management Module

        if payt == 1:

            Termy = ("Funds Management Module Triggered.\n"
                     "\n"
                     "Pay Out Process Starting ...\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)

            Database.commit()

            query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM profit_loss " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 720 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            ProfitCS= np.cumsum(np.sum(np.asarray(Col), axis=1))
            Profitn = ProfitCS[-1]

            query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM BuyPrices " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            lstbp = np.asarray(Col)[0]

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
                    f"FROM profit_loss " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            prolo = np.asarray(Col)[0]

            query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM profit_loss_short " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            prolos = np.asarray(Col)[0]

            query = f"SELECT BTC, ETH, XLM, XMR, XRP, LINK, NEO " \
                    f"FROM profit_loss_long " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            prolol = np.asarray(Col)[0]

            query = f"SELECT MinPort, SavRate " \
                    f"FROM Miscellaneous " \
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            MinPort = Col[0][0]
            PPrft = Col[0][1]

            s = 0
            TotalFunds = 0
            ordbk = pandas.DataFrame(client.get_orderbook_tickers())
            ordbk = ordbk.set_index('symbol')
            bidaskprice = ordbk.loc[:, ['bidPrice', 'askPrice']]
            sprices = []
            for crypto in Cry_strn:
                if crypto == 'USDT':
                    vap = client.get_asset_balance(asset=crypto)
                    vas = float(vap['free'])
                else:
                    sprices += [float(bidaskprice.loc[f'{Cry_strO[s]}', 'bidPrice'])]
                    vap = client.get_asset_balance(asset=crypto)
                    vas = (float(vap['free']) + float(vap['locked'])) * sprices[s]
                TotalFunds += vas
                s += 1

            OOrds = []
            for i in range(len(Cry_str)):
                val = float(client.get_asset_balance(asset=Cry_str[i])['free'])
                if val == [] or val*sprices[i] < 10:
                    OOrds += [0]
                else:
                    OOrds += [val]
            ln = len(OOrds)
            tpPrft = Profitn
            OPrft = trunc1(PPrft * tpPrft)
            POPrft = OPrft / TotalFunds

            if tpPrft > 0:
                aclr = np.ones((1, len(Cry_str)))[0]
                for i in range(ln):
                    if OOrds[i] != 0:
                        SV = truncatefunc[i](POPrft * OOrds[i])
                        if (SV * sprices[i]) > 10 and ((OOrds[i] - SV) * sprices[i]) > 25:
                            aclr[i] = 1
                        else:
                            aclr[i] = 0
                ALclr = np.prod(aclr)
            else:
                ALclr = 0

            if tpPrft > 0 and ALclr == 1 and TotalFunds > (MinPort + OPrft) and OPrft > 10:
                vals = np.zeros((1, len(Cry_str) + 1))[0]
                Svals = np.zeros((1, len(Cry_str) + 1))[0]
                Lvals = np.zeros((1, len(Cry_str) + 1))[0]
                valsp = np.zeros((1, len(Cry_str) + 1))[0]
                Svalsp = np.zeros((1, len(Cry_str) + 1))[0]
                Lvalsp = np.zeros((1, len(Cry_str) + 1))[0]
                for i in range(ln):
                    if OOrds[i] != 0:
                        Scpr = (Slstb[i] / (Slstb[i] + Llstb[i]))
                        if np.isnan(Scpr) == 1 or np.isinf(Scpr) == 1:
                            Scpr = 0
                        Lcpr = (Llstb[i] / (Slstb[i] + Llstb[i]))
                        if np.isnan(Lcpr) == 1 or np.isinf(Lcpr) == 1:
                            Lcpr = 0

                        OV = truncatefunc[i](POPrft * OOrds[i])
                        Bdtao = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                        order = client.order_market_sell(symbol=Cry_strO[i], quantity=OV)

                        ordIdo = Bdtao[0]['orderId']

                        orders = 0
                        while orders != []:
                            orders = client.get_open_orders(symbol=Cry_strO[i])

                        Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                        dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                        sde = Bdta[0]['side']
                        ordId=ordIdo
                        while ([dttm.year, dttm.month, dttm.day, dttm.hour] !=
                               [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour]) \
                                or sde != 'SELL' or ordId==ordIdo:
                            time.sleep(0.5)
                            Bdta = client.get_all_orders(symbol=Cry_strO[i], limit=1)
                            dttm = datetime.fromtimestamp(Bdta[0]['time'] / 1000)
                            ordId = Bdta[0]['orderId']
                            sde = Bdta[0]['side']

                        vals[i] = float(Bdta[0]['executedQty'])
                        valsp[i] = float(Bdta[0]['cummulativeQuoteQty']) * 0.999
                        if SSign[i] != 0 and LSign[i] == 0:
                            Svals[i] = vals[i]
                            Svalsp[i] = valsp[i]
                        elif SSign[i] == 0 and LSign[i] != 0:
                            Lvals[i] = vals[i]
                            Lvalsp[i] = valsp[i]
                        elif SSign[i] != 0 and LSign[i] != 0:
                            Svals[i] = POPrft * Slstb[i]
                            Svalsp[i] = POPrft * Slstbp[i]
                            Lvals[i] = POPrft * Llstb[i]
                            Lvalsp[i] = POPrft * Llstbp[i]
                            Svals[i] = Svals[i] + (Scpr * (vals[i] - (Lvals[i] + Svals[i])))
                            Lvals[i] = Lvals[i] + (Lcpr * (vals[i] - (Lvals[i] + Svals[i])))
                            Svalsp[i] = Svalsp[i] + (Scpr * (valsp[i] - (Lvalsp[i] + Svalsp[i])))
                            Lvalsp[i] = Lvalsp[i] + (Lcpr * (valsp[i] - (Lvalsp[i] + Svalsp[i])))

                bupdt = lstb - vals
                Sbupdt = Slstb - Svals
                Lbupdt = Llstb - Lvals

                buyper = abs(vals / lstb)
                sbuyper = abs(Svals / Slstb)
                lbuyper = abs(Lvals / Llstb)
                buyper[(np.isnan(buyper)) | (np.isinf(buyper))] = 0
                sbuyper[(np.isnan(sbuyper)) | (np.isinf(sbuyper))] = 0
                lbuyper[(np.isnan(lbuyper)) | (np.isinf(lbuyper))] = 0

                Sbupdtp = Slstbp * (1-sbuyper)
                Lbupdtp = Llstbp * (1-lbuyper)
                bupdtp = Sbupdtp + Lbupdtp

                Sprofit = prolos - (Slstbp * sbuyper) + Svalsp
                Lprofit = prolol - (Llstbp * lbuyper) + Lvalsp
                profit = Sprofit + Lprofit

                pdelrec = " DELETE FROM profit_loss ORDER BY date DESC LIMIT 1"
                pdelrecs = " DELETE FROM profit_loss_short ORDER BY date DESC LIMIT 1"
                pdelrecl = " DELETE FROM profit_loss_long ORDER BY date DESC LIMIT 1"
                my_cursor.execute(pdelrec)
                my_cursor.execute(pdelrecs)
                my_cursor.execute(pdelrecl)
                Database.commit()
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

                # Withdrawal

                try:
                    result = client.withdraw(
                        asset='USDT',
                        address='',
                        network='BNB',
                        amount=OPrft)
                except BinanceAPIException as e:
                    msg = EmailMessage()
                    msg.set_content(f"Waithdraw Error.\n"
                                    f"\n"
                                    f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                                    f"BinanceAPIexception.\n"
                                    f"{e}\n"
                                    f"\n"
                                    f"\n"
                                    f"Traceback:\n"
                                    f"\n"
                                    f"{traceback.format_exc()}"
                                    f"\n")

                    msg['Subject'] = "Briareos.binance Withdraw Error"
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.send_message(msg)

                    Termy = (f"Withdraw Error. Check Email for more information.\n"
                             f"\n")
                    Term = Term + Termy
                    MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                    my_cursor.execute(MTrecord)
                    Database.commit()
                else:
                    Termy = ("Pay Out has been processed, withdrawal executed.\n"
                             "\n")
                    Term = Term + Termy
                    MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal" '
                    my_cursor.execute(MTrecord)

                    Database.commit()

            EMrecord = "UPDATE ExecutionCom SET payout = 0"
            my_cursor.execute(EMrecord)
            Database.commit()

        # Port Values (USDT)

        time.sleep(10) # wait for Binance Database (USDT)

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

        prices = []
        for crypto in Cry_strO:
            query = f"SELECT close " \
            f"FROM {crypto}h " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            prices += col[0]
        prices = np.asarray(prices)

        vap = client.get_asset_balance(asset='USDT')
        vas = float(vap['free'])

        Avals = np.hstack((lstb * prices, vas))
        SAvals= np.hstack((Slstb * prices, vas))
        LAvals = np.hstack((Llstb * prices, vas))
        record = " INSERT INTO Port_values VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Srecord = " INSERT INTO Port_values_short VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Lrecord = " INSERT INTO Port_values_long VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        nowr = datetime.now()
        values = [nowr] + np.ndarray.tolist(Avals)
        Svalues = [nowr] + np.ndarray.tolist(SAvals)
        Lvalues = [nowr] + np.ndarray.tolist(LAvals)
        my_cursor.execute(record, tuple(values))
        my_cursor.execute(Srecord, tuple(Svalues))
        my_cursor.execute(Lrecord, tuple(Lvalues))

        record = f"INSERT IGNORE INTO TotalFunds ( date, value) VALUES (%s, %s) "
        values = (datetime.now(), sum(Avals))
        my_cursor.execute(record, values)
        Database.commit()

        nowdat = datetime.now()
        Termy = (f"Execution of TradM_OEM_Module Has Completed Successfully.\n"
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
        msg.set_content(f"TradM_OEM_Module is experiencing Problems.\n"
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

        Term = Term.replace('"', "'")
        MTrecord = f'UPDATE Exception_Terminal SET Trad_OEM = "{Term}" WHERE PK = "Terminal"'
        my_cursor.execute(MTrecord)

        MTrecord2 = 'UPDATE Exception_Terminal SET Trad_OEM = "error" WHERE PK = "Status" '
        my_cursor.execute(MTrecord2)
        Database.commit()
