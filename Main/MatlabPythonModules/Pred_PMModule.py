# This Modules executes Matlab code responsible for predicting future market trends and optimize the portfolios
# considering those predictions


def predictionport():

    import mysql.connector
    import sys

    Database = mysql.connector.connect(
        host="",
        user="root",
        passwd="")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    MTrecord = 'UPDATE Exception_Terminal SET Pred_PMM = "Running" WHERE PK = "Status" '
    my_cursor.execute(MTrecord)
    Database.commit()

    Term = ""

    try:
        import matlab.engine
        import numpy as np
        import datetime
        import pickle
        from datetime import datetime, date, timedelta

        # Predictions and Portfolio Management Module (System 2)

        eng = matlab.engine.start_matlab()

        eng.cd(r'C:\Users\Machine2\Desktop\Matlab Code', nargout=0)
        eng.ls(nargout=0)

        # Predictions Module

        nowdat = datetime.now()
        Term = (f"{nowdat}\n"
                f"\n"
                f"Prediction Module Starting ...\n"
                f"\n")

        MTrecord = f'UPDATE Exception_Terminal SET Pred_PMM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        query = f"SELECT t " \
                f"FROM Miscellaneous " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        t = int(col[0][0])
        pt = matlab.double([int(col[0][0])])

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

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
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

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        lPdcnpv = np.zeros((250, len(Cry_str)))
        r = 0
        for crypto in Cry_str:
            query = f"SELECT volume " \
                    f"FROM {crypto}d " \
                    f"ORDER BY date DESC " \
                    f"LIMIT 250 "
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
                f"LIMIT 700 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        Col = [list(item) for item in col]
        list.reverse(Col)
        Cryptos = np.asarray(Col)

        query = f"SELECT EWA, EWT, INDA, EWZ, EEM, EWQ, EWM, EWU, EWG, " \
                f"SPY, EWC, MCHI, VEA, EIDO, EWS, VGK, EWJ, IYW, VGT, " \
                f"VDE, ERUS, XT, IAU, PICK, ICLN, ITA " \
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

        Cry_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo']
        Par = np.zeros((7, 12))
        j = 0
        for crypto in Cry_str:
            query = f"SELECT a, b, c, d, e, f, g, h, i, j, k, l "\
                    f"FROM {crypto}popt "\
                    f"ORDER BY date DESC "\
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            Par[j, :] = np.asarray(Col)
            j += 1
        PPar=matlab.double(np.ndarray.tolist(Par))

        mifll = np.ndarray.tolist(np.concatenate((CryptoND, GTdata, Worldind, Stocks, Cryptos, lPdcnp), axis=1))

        MDIFull = matlab.double([[*x, y] for x, y in zip(mifll, mdfll)])
        Mi = matlab.double(mifll[-(7 * t):])

        [CFTA, MdR, MdRvar, MdRExp, MEMpredi, PdR1, PdR2, PdR3, PdR4, PdR5, PdR6, PdR7, PDvar,
         PDExp, PPMpredi, Predicts, n] = eng.PreditionsModule(pt, MDIFull, Mi, Md, Pd, Pdv, PPar, nargout=17)

        with open(r"C:\Users\Machine2\Desktop\PickleFiles\predvars.pickle", "wb") as f:
            pickle.dump([CFTA, MdR, MdRvar, MdRExp, MEMpredi, PdR1, PdR2, PdR3, PdR4, PdR5, PdR6, PdR7, PDvar,
                         PDExp, PPMpredi, Predicts, n], f)

        dat = (date.today() + timedelta(days=6))
        data = [MEMpredi] + [list(i) for i in PPMpredi][0]
        val = [float(i) for i in data]
        record = f"INSERT IGNORE INTO Predictions VALUES ({'%s, ' * (len(val))}%s)"
        valu = [dat] + val
        value = tuple(valu)
        my_cursor.execute(record, value)
        Database.commit()

        # Portfolio Management Module

        TermPPM = "Prediction Module Executed"
        TermPMM1= "Portfolio Management Module Starting ..."
        Term = (f"{nowdat}\n"
                f"\n"
                f"Prediction Module Starting ...\n"
                f"\n"
                f"{TermPPM}\n"
                f"\n"
                f"\n"
                f"{TermPMM1}\n"
                f"\n")

        MTrecord = f'UPDATE Exception_Terminal SET Pred_PMM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']
        lPdcnp = np.zeros((2*t, len(Cry_str)))
        r = 0
        for crypto in Cry_str:
            query = f"SELECT close " \
                    f"FROM {crypto}d " \
                    f"ORDER BY date DESC " \
                    f"LIMIT {2 * t} "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [item for sublist in [list(i) for i in col] for item in sublist]
            list.reverse(Col)
            lPdcnp[:, r] = Col
            r += 1

        Pd = matlab.double(np.ndarray.tolist(lPdcnp))

        sPdcnp = np.zeros((24 * t, len(Cry_str)))
        r = 0
        for crypto in Cry_str:
            query = f"SELECT close " \
                    f"FROM {crypto}h " \
                    f"ORDER BY date DESC " \
                    f"LIMIT {24 * t} "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [item for sublist in [list(i) for i in col] for item in sublist]
            list.reverse(Col)
            sPdcnp[:, r] = Col
            r += 1

        sPd = matlab.double(np.ndarray.tolist(sPdcnp))

        Cry_sig = ["BTC", "ETH", "XLM", "XMR", "XRP", "LINK", "NEO"]

        query = f"SELECT BTC " \
                f"FROM ShortTradingSigR " \
                f"ORDER BY date DESC " \
                f"LIMIT {24 * t} "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        if len(col) < 24 * t:
            SGSg = np.zeros((len(col), len(Cry_sig)))
        else:
            SGSg = np.zeros((24 * t, len(Cry_sig)))

        r = 0
        for crypt in Cry_sig:
            query = f"SELECT {crypt} " \
                    f"FROM ShortTradingSigR " \
                    f"ORDER BY date DESC " \
                    f"LIMIT {24 * t} "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            SGSg[:, r] = np.asarray(Col).flatten()
            r += 1

        SGSg = np.delete(SGSg, -1, 0)
        SGS = matlab.double(np.ndarray.tolist(SGSg))

        query = f"SELECT BTC " \
                f"FROM LongTradingSigR " \
                f"ORDER BY date DESC " \
                f"LIMIT {24 * t} "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        if len(col) < 24 * t:
            LGSg = np.zeros((len(col), len(Cry_sig)))
        else:
            LGSg = np.zeros((24 * t, len(Cry_sig)))

        r = 0
        for crypt in Cry_sig:
            query = f"SELECT {crypt} " \
                    f"FROM LongTradingSigR " \
                    f"ORDER BY date DESC " \
                    f"LIMIT {24 * t} "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            list.reverse(Col)
            LGSg[:, r] = np.asarray(Col).flatten()
            r += 1

        LGSg = np.delete(LGSg, -1, 0)
        LGS = matlab.double(np.ndarray.tolist(LGSg))

        with open(r"C:\Users\Machine2\Desktop\PickleFiles\predvars.pickle", "rb") as f:
            CFTA, MdR, MdRvar, MdRExp, MEMpredi, PdR1, PdR2, PdR3, PdR4, PdR5, PdR6, PdR7, PDvar, \
            PDExp, PPMpredi, Predicts, n = pickle.load(f)

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        STPp = np.zeros((7, 1))
        j = 0
        for crypto in Cry_str:
            query = f"SELECT alpha "\
                    f"FROM {crypto}_SStrt "\
                    f"ORDER BY date DESC "\
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            STPp[j] = np.asarray(Col)
            j += 1

        STP = matlab.double(np.ndarray.tolist(STPp))

        LTPp = np.zeros((7, 1))
        j = 0
        for crypto in Cry_str:
            query = f"SELECT alpha "\
                    f"FROM {crypto}_LStrt "\
                    f"ORDER BY date DESC "\
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            LTPp[j] = np.asarray(Col)
            j += 1

        LTP = matlab.double(np.ndarray.tolist(LTPp))

        Cry_str = ['btc', 'eth', 'xlm', 'xmr', 'xrp', 'link', 'neo']
        Para = np.zeros(7)
        j = 0
        for crypto in Cry_str:
            query = f"SELECT accur "\
                    f"FROM {crypto}popt "\
                    f"ORDER BY date DESC "\
                    f"LIMIT 1 "
            my_cursor.execute(query)
            col = my_cursor.fetchall()
            Col = [list(item) for item in col]
            Para[j] = np.asarray(Col)
            j += 1
        Par=matlab.double(np.ndarray.tolist(Para))

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        Sdta = ['SvarMACD', 'SvarOBV', 'SvarADL', 'SvarATR', 'SvarOSC', 'SvarCCI', 'SStrt']
        SvarOSCnp = np.zeros((7, 2))
        SvarMACDnp = np.zeros((7, 3))
        SvarOBVnp = np.zeros((7, 3))
        SvarADLnp = np.zeros((7, 3))
        SvarATRnp = np.zeros((7, 3))
        SvarCCInp = np.zeros((7, 2))
        SStrtnp = np.zeros((7, 22))
        for data in Sdta:
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

        Cry_str = ['BTC', 'ETH', 'XLM', 'XMR', 'XRP', 'LINK', 'NEO']
        Ldta = ['LvarMACD', 'LvarOBV', 'LvarADL', 'LvarATR', 'LvarOSC', 'LvarCCI', 'LStrt']
        LvarOSCnp = np.zeros((7, 2))
        LvarMACDnp = np.zeros((7, 3))
        LvarOBVnp = np.zeros((7, 3))
        LvarADLnp = np.zeros((7, 3))
        LvarATRnp = np.zeros((7, 3))
        LvarCCInp = np.zeros((7, 2))
        LStrtnp = np.zeros((7, 22))
        for data in Ldta:
            j = 0
            for crypto in Cry_str:
                if  data == 'LvarOSC' or data == 'LvarCCI':
                    query = f"SELECT a, b " \
                            f"FROM {crypto}_{data} " \
                            f"ORDER BY date DESC " \
                            f"LIMIT 1 "
                    my_cursor.execute(query)
                    col = my_cursor.fetchall()
                    Col = [list(item) for item in col]
                    vars()[f"{data}np"][j, :] = np.asarray(Col)
                elif data == 'LStrt':
                    query = f"SELECT a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v " \
                            f"FROM {crypto}_{data} " \
                            f"ORDER BY date DESC " \
                            f"LIMIT 1 "
                    my_cursor.execute(query)
                    col = my_cursor.fetchall()
                    Col = [list(item) for item in col]
                    LStrtnp[j, :] = np.asarray(Col)
                else:
                    query = f"SELECT a, b, c " \
                            f"FROM {crypto}_{data} " \
                            f"ORDER BY date DESC " \
                            f"LIMIT 1 "
                    my_cursor.execute(query)
                    col = my_cursor.fetchall()
                    Col = [list(item) for item in col]
                    vars()[f"{data}np"][j, :] = np.asarray(Col)
                j += 1


        sima = np.zeros(len(Cry_str))
        lima = np.zeros(len(Cry_str))
        for i in range(len(Cry_str)):
            Sof = SStrtnp[i,-len(Sdta):]
            Lof = LStrtnp[i,-len(Ldta):]
            # Short
            SMc = Sof[0] * np.mean(SvarMACDnp[i, :])
            SOb = Sof[1] * np.mean(SvarOBVnp[i, :])
            SAd = Sof[2] * np.mean(SvarADLnp[i, :])
            SAt = Sof[3] * np.mean(SvarATRnp[i, :])
            SOs = Sof[4] * np.mean(SvarOSCnp[i, :])
            SCi = Sof[5] * np.mean(SvarCCInp[i, :])
            sima[i]=(SMc + SOb + SAd + SAt + SOs + SCi)/np.sum(Sof)
            # Long
            LMc = Lof[0] * np.mean(LvarMACDnp[i, :])
            LOb = Lof[1] * np.mean(LvarOBVnp[i, :])
            LAd = Lof[2] * np.mean(LvarADLnp[i, :])
            LAt = Lof[3] * np.mean(LvarATRnp[i, :])
            LOs = Lof[4] * np.mean(LvarOSCnp[i, :])
            LCi = Lof[5] * np.mean(LvarCCInp[i, :])
            lima[i] = (LMc + LOb + LAd + LAt + LOs + LCi) / np.sum(Lof)

        Simag = matlab.double(np.ndarray.tolist(sima))
        Limag = matlab.double(np.ndarray.tolist(lima))

        query = f"SELECT value " \
                f"FROM totalfunds " \
                f"ORDER BY date DESC " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        TotalFunds = matlab.double([col[0][0]])

        query = f"SELECT Inception_Date " \
                f"FROM Miscellaneous " \
                f"LIMIT 1 "
        my_cursor.execute(query)
        col = my_cursor.fetchall()
        inceptdate = col[0][0]
        daycount = matlab.double([(date.today() - inceptdate).days])

        [SPort, LPort, LAPort, SAPort, LPortSD, SPortSD] = eng.PortfolioOpt(pt, daycount, SGS, LGS, Pd, sPd,
                                                                            TotalFunds, Predicts, Par, STP, LTP,
                                                                            Simag, Limag, nargout=6)

        recordS = "INSERT IGNORE INTO PortfolioOptS VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        recordL = "INSERT IGNORE INTO PortfolioOptL VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        dat = date.today()
        dataS = [SPortSD] + [SPort] + [list(i) for i in SAPort][0]
        dataL = [LPortSD] + [LPort] + [list(i) for i in LAPort][0]
        valS = [float(i) for i in dataS]
        valL = [float(i) for i in dataL]
        valuS = [dat] + valS
        valuL = [dat] + valL
        valueS = tuple(valuS)
        valueL = tuple(valuL)
        my_cursor.execute(recordS, valueS)
        my_cursor.execute(recordL, valueL)
        Database.commit()

        EMrecord = "UPDATE ExecutionCom SET adjust = 1"
        my_cursor.execute(EMrecord)
        Database.commit()

        TermPMM2= "Portfolio Management Module Executed"
        Term = (f"{nowdat}\n"
                f"\n"
                f"Prediction Module Starting ...\n"
                f"\n"
                f"{TermPPM}\n"
                f"\n"
                f"\n"
                f"{TermPMM1}\n"
                f"\n"
                f"{TermPMM2}\n"
                f"\n"
                f"\n"
                f"Execution of Pre_PMModule Completed Successfully\n"
                f"\n"
                f"{datetime.now()}")

        MTrecord1 = f'UPDATE Exception_Terminal SET Pred_PMM = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord1)

        MTrecord2 = 'UPDATE Exception_Terminal SET Pred_PMM = "idle" WHERE PK = "Status" '
        my_cursor.execute(MTrecord2)
        Database.commit()
    except Exception as e:
        import smtplib
        import ssl
        from email.message import EmailMessage
        from datetime import datetime
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
        msg.set_content(f"Pre_PMModule is experiencing Problems.\n"
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
        MTrecord = f'UPDATE Exception_Terminal SET Pred_PMM = "{Term}" WHERE PK = "Terminal"'
        my_cursor.execute(MTrecord)

        MTrecord2 = 'UPDATE Exception_Terminal SET Pred_PMM = "error" WHERE PK = "Status" '
        my_cursor.execute(MTrecord2)
        Database.commit()
