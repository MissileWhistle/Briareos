# This module executes Matlab code responsible for the optimization of the trading strategies used by the algorithm
# It also optimizes parameters of the Predictions Module (refer to Pred_PMMmodule.py)

def tradingopt():

    import matlab.engine
    import numpy as np
    from datetime import date, datetime
    import mysql.connector as mysql
    import sys

    Database = mysql.connect(
        host="",
        user="root",
        passwd="")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    MTrecord = 'UPDATE Exception_Terminal SET TOptModule = "Running" WHERE PK = "Status" '
    my_cursor.execute(MTrecord)
    Database.commit()

    Term = ""

    try:

        eng = matlab.engine.start_matlab()

        eng.cd(r"C:\Users\Machine0\Desktop\Matlab Code", nargout=0)
        eng.ls(nargout=0)

        # Optimization Module (System 1)

        # Short-Term Trading Opt.
        nowdat = datetime.now()
        Term = (f"{nowdat}\n"
                f"\n"
                f"Trading Optimization Module Starting ...\n"
                f"\n"
                f"Short Term Trading Opt. Running ...\n"
                f"\n")

        MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        query = f"SELECT date " \
                f"FROM BTCUSDTh " \
                f"ORDER BY date DESC " \
                f"LIMIT 2000 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Cn = len(col)

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        metric = ['close', 'high', 'low', 'volume']
        Mvar = ['sPdc', 'sPdh', 'sPdl', 'sPdvol']
        sPdcnp = np.zeros((Cn, len(Cry_str)))
        sPdhnp = np.zeros((Cn, len(Cry_str)))
        sPdlnp = np.zeros((Cn, len(Cry_str)))
        sPdvolnp = np.zeros((Cn, len(Cry_str)))
        j = 0
        for metrc in metric:
            r = 0
            for crypto in Cry_str:
                query = f"SELECT {metrc} " \
                        f"FROM {crypto}h " \
                        f"ORDER BY date DESC " \
                        f"LIMIT 2000 "
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

        query = f"SELECT date "\
                f"FROM btc_svarcci " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        datedb = col[0][0]
        DBdate = datetime(datedb.year, datedb.month, datedb.day)
        VSOPTdt = (datetime.now() - DBdate).days

        query = f"SELECT Inception_Date " \
                f"FROM Miscellaneous " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        inceptdate = col[0][0]
        daycount = (date.today() - inceptdate).days
        d28 = np.mod(daycount+1, 28)
        d10 = np.mod(daycount, 10)
        d20 = np.mod(daycount, 20)

        if d10 == 0 or VSOPTdt > 10:

            Termy = ("Short Term Vars-Opt Running ...\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

            [SvarMACD, SvarOBV, SvarADL, SvarATR, SvarOSC, SvarCCI] = eng.ShortTermOptVars(sPdc, sPdh,
                                                                                           sPdl, sPdvol, nargout=6)

            Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']

            # Reconnect to DB, used because some code is very time expensive and connection to DB might have been lost
            Database = mysql.connect(
                host="",
                user="",
                passwd="")

            my_cursor = Database.cursor()

            my_cursor.execute("USE briareos")

            dta = ['SvarMACD', 'SvarOBV', 'SvarADL', 'SvarATR', 'SvarOSC', 'SvarCCI']
            dat = date.today()
            j = 0
            for crypto in Cry_str:
                for datav in dta:
                    if  datav == 'SvarOSC' or datav == 'SvarCCI':
                        record = f"INSERT IGNORE INTO {crypto}_{datav} VALUES ( %s, %s, %s, %s)"
                        data = [float(i) for i in list(vars()[f"{datav}"][j])]
                        valus = [dat] + data
                        values = tuple(valus)
                        my_cursor.execute(record, values)
                    else:
                        record = f"INSERT IGNORE INTO {crypto}_{datav} VALUES ( %s, %s, %s, %s, %s)"
                        data = [float(i) for i in list(vars()[f"{datav}"][j])]
                        valus = [dat] + data
                        values = tuple(valus)
                        my_cursor.execute(record, values)
                j += 1

            Database.commit()

            Termy = ("Short Term Var-Opt Executed.\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

        Termy = ("Short Term GO Strat. Opt. Running ...\n"
                 "\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        dta = ['SvarMACD', 'SvarOBV', 'SvarADL', 'SvarATR', 'SvarOSC', 'SvarCCI']
        SvarOSCnp = np.zeros((7, 2))
        SvarMACDnp = np.zeros((7, 3))
        SvarOBVnp = np.zeros((7, 3))
        SvarADLnp = np.zeros((7, 3))
        SvarATRnp = np.zeros((7, 3))
        SvarCCInp = np.zeros((7, 2))
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

        SStrt = eng.ShortTermOptGO(sPdc, sPdh, sPdl, sPdvol, SvarMACD, SvarOBV, SvarADL, SvarATR,
                                   SvarOSC, SvarCCI, nargout=1)

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        dat = date.today()
        j = 0
        for crypto in Cry_str:
            record = f"INSERT IGNORE INTO {crypto}_SStrt VALUES ( %s, %s, %s, %s, %s, %s, %s, %s," \
                     f" %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = [float(i) for i in list(SStrt[j])]
            valus = [dat] + data
            values = tuple(valus)
            my_cursor.execute(record, values)
            j += 1

        Termy = ("Short Term GO Strat. Opt. Executed.\n"
                 "\n"
                 "Short Term Trading Opt. Completed."
                 "\n"
                 "\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        # Long-Term Trading Opt.

        query = f"SELECT date "\
                f"FROM btc_lvarcci " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        datedb = col[0][0]
        DBdate = datetime(datedb.year, datedb.month, datedb.day)
        VLOPTdt = (datetime.now() - DBdate).days

        query = f"SELECT date "\
                f"FROM btc_lstrt " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        datedb = col[0][0]
        DBdate = datetime(datedb.year, datedb.month, datedb.day)
        GLOPTdt = (datetime.now() - DBdate).days

        if d10 == 0 or GLOPTdt > 10 or VLOPTdt > 20:

            Termy = ("Long Term Trading Opt. Starting ...\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

            Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
            metric = ['close', 'high', 'low', 'volume']
            Mvar = ['lPdc', 'lPdh', 'lPdl', 'lPdvol']
            lPdcnp = np.zeros((750, len(Cry_str)))
            lPdhnp = np.zeros((750, len(Cry_str)))
            lPdlnp = np.zeros((750, len(Cry_str)))
            lPdvolnp = np.zeros((750, len(Cry_str)))
            j = 0
            for metrc in metric:
                r = 0
                for crypto in Cry_str:
                    query = f"SELECT {metrc} " \
                            f"FROM {crypto}d " \
                            f"ORDER BY date DESC " \
                            f"LIMIT 750 "
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

            if d20 == 0 or VLOPTdt > 20:

                Termy = ("Long Term Vars-Opt Running ...\n"
                         "\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()

                [LvarMACD, LvarOBV, LvarADL, LvarATR, LvarOSC,
                 LvarCCI] = eng.LongTermOptVars(lPdc, lPdh, lPdl, lPdvol, nargout=6)

                Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']

                # Reconnect to DB, used because some code is very time expensive and connection to DB might have been lost
                Database = mysql.connect(
                    host="",
                    user="",
                    passwd="")

                my_cursor = Database.cursor()

                my_cursor.execute("USE briareos")

                dta = ['LvarMACD', 'LvarOBV', 'LvarADL', 'LvarATR', 'LvarOSC', 'LvarCCI']
                dat = date.strftime(date.today(), "%Y-%m-%d")
                j = 0
                for crypto in Cry_str:
                    for datav in dta:
                        if  datav == 'LvarOSC' or datav == 'LvarCCI':
                            record = f"INSERT IGNORE INTO {crypto}_{datav} VALUES ( %s, %s, %s, %s)"
                            data = [float(i) for i in list(vars()[f"{datav}"][j])]
                            valus = [dat] + data
                            values = tuple(valus)
                            my_cursor.execute(record, values)
                        else:
                            record = f"INSERT IGNORE INTO {crypto}_{datav} VALUES ( %s, %s, %s, %s, %s)"
                            data = [float(i) for i in list(vars()[f"{datav}"][j])]
                            valus = [dat] + data
                            values = tuple(valus)
                            my_cursor.execute(record, values)
                    j += 1

                Database.commit()

                Termy = ("Long Term Vars-Opt Executed.\n"
                         "\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()

            if d10 == 0 or GLOPTdt > 10:

                Termy = ("Long Term GO Strat. Opt. Running ...\n"
                         "\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()

                Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
                dta = ['LvarMACD', 'LvarOBV', 'LvarADL', 'LvarATR', 'LvarOSC', 'LvarCCI']
                LvarOSCnp = np.zeros((7, 2))
                LvarMACDnp = np.zeros((7, 3))
                LvarOBVnp = np.zeros((7, 3))
                LvarADLnp = np.zeros((7, 3))
                LvarATRnp = np.zeros((7, 3))
                LvarCCInp = np.zeros((7, 2))
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

                LStrt = eng.LongTermOptGO(lPdc, lPdh, lPdl, lPdvol,
                                          LvarMACD, LvarOBV, LvarADL, LvarATR, LvarOSC, LvarCCI, nargout=1)

                Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
                dat = date.strftime(date.today(), "%Y-%m-%d")
                j = 0
                for crypto in Cry_str:
                    record = f"INSERT IGNORE INTO {crypto}_LStrt VALUES ( %s, %s, %s, %s, %s, %s, %s, %s," \
                             f" %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    data = [float(i) for i in list(LStrt[j])]
                    valus = [dat] + data
                    values = tuple(valus)
                    my_cursor.execute(record, values)
                    j += 1

                Termy = ("Long Term GO Strat. Opt. Executed.\n"
                         "\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()

            Termy = ("Long Term Trading Opt. Completed."
                     "\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()


        # Predictions Opt.


        query = f"SELECT date "\
                f"FROM btcpopt " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        datedb = col[0][0]
        DBdate = datetime(datedb.year, datedb.month, datedb.day)
        POPTdt = (datetime.now() - DBdate).days

        if d28 == 0 or POPTdt > 28:

            Termy = ("Pred. Optimization Starting."
                     "\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

            query = f"SELECT price " \
                    f"FROM CryptoIndex " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 882 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [item for sublist in [list(i) for i in col] for item in sublist]
            list.reverse(Col)
            Md = eng.transpose(matlab.double(Col))
            mdfll = Col

            Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
            lPdcnp = np.zeros((len(mdfll), len(Cry_str)))
            r = 0
            for crypto in Cry_str:
                query = f"SELECT close " \
                        f"FROM {crypto}d " \
                        f"ORDER BY date DESC " \
                        f"LIMIT 882 "
                my_cursor.execute(query)
                col = my_cursor.fetchall()
                Col = [item for sublist in [list(i) for i in col] for item in sublist]
                list.reverse(Col)
                lPdcnp[:, r] = Col
                r += 1

            Pd = matlab.double(np.ndarray.tolist(lPdcnp))

            lPdcnpv = np.zeros((len(mdfll), len(Cry_str)))
            r = 0
            for crypto in Cry_str:
                query = f"SELECT volume " \
                        f"FROM {crypto}d " \
                        f"ORDER BY date DESC " \
                        f"LIMIT 882 "
                my_cursor.execute(query)
                col = my_cursor.fetchall()
                Col = [item for sublist in [list(i) for i in col] for item in sublist]
                list.reverse(Col)
                lPdcnpv[:, r] = Col
                r += 1

            Pdv = matlab.double(np.ndarray.tolist(lPdcnpv))

            query = f"SELECT BNB, IOTA, VET, ADA, LTC " \
                    f"FROM cryptos " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 882 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            Cryptos = np.asarray(Col)

            query = f"SELECT EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, " \
                    f"SPY, EWC, MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT," \
                    f" VDE, ERUS, XT, IAU, PICK, ICLN, ITA " \
                    f"FROM worldindices " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 882 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            Worldind = np.asarray(Col)

            query = f"SELECT TSLA, MSFT, GOOGL, AAPL, IBM, AMZN, FB, HYMTF, VWAGY " \
                    f"FROM stocks " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 882 "
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
                        f"LIMIT 882 "
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
                    f"LIMIT 882 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            GTdata = np.asarray(Col)

            mifll = np.ndarray.tolist(
                np.concatenate((CryptoND, GTdata, Worldind, Stocks, Cryptos, lPdcnp), axis=1))

            MDIFull = matlab.double([[*x, y] for x, y in zip(mifll, mdfll)])
            Mi = matlab.double(mifll)

            PPar = eng.PredOptRun(Mi, Md, Pd, Pdv, nargout=1)

            # Reconnect to DB, used because some code is very time expensive and connection to DB might have been lost
            Database = mysql.connect(
                host="",
                user="root",
                passwd="")

            my_cursor = Database.cursor()

            my_cursor.execute("USE briareos")

            Cry_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo']
            dat = date.strftime(date.today(), "%Y-%m-%d")
            j = 0
            for crypto in Cry_str:
                record = f"INSERT IGNORE INTO {crypto}popt VALUES ( %s, %s, %s, %s, %s, %s, %s, %s," \
                         f" %s, %s, %s, %s, %s, %s)"
                data = [float(i) for i in list(PPar[j])]
                valus = [dat] + data
                values = tuple(valus)
                my_cursor.execute(record, values)
                j += 1
            Database.commit()

            Termy = ("Pred. Optimization executed."
                     "\n"
                     "\n")
            Term = Term + Termy
            MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
            my_cursor.execute(MTrecord)
            Database.commit()

        Termy = (f"Execution of TOptimization_Modules Completed Successfully\n"
                 f"\n"
                 f"{datetime.now()}")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        MTrecord2 = 'UPDATE Exception_Terminal SET TOptModule = "idle" WHERE PK = "Status" '
        my_cursor.execute(MTrecord2)
        Database.commit()

    except Exception as e:
        import smtplib
        import ssl
        from email.message import EmailMessage
        import traceback

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
                  f"{traceback.format_exc()}"
                  f"\n")
        Term = Term + errstr

        msg = EmailMessage()
        msg.set_content(f"\n"
                        f"TOptimization_Modules is experiencing Problems.\n"
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

        Term=Term.replace('"',"'")
        MTrecord = fr'UPDATE Exception_Terminal SET TOptModule = "{Term}" WHERE PK = "Terminal"'
        my_cursor.execute(MTrecord)

        MTrecord2 = 'UPDATE Exception_Terminal SET TOptModule = "error" WHERE PK = "Status"'
        my_cursor.execute(MTrecord2)
        Database.commit()
