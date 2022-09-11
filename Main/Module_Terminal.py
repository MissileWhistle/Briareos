# This module is responsible for the execution of the modules of the algo-trading system. It assigns the execution of
# these modules to machines\computer in the network, allowing them to run in parallel


def BriareosTerminal():

    import time
    import dispy
    import Matlab_Python_Modules.TOptimization_Modules as Topt
    import Matlab_Python_Modules.Pred_PMModule as PPMM
    import Matlab_Python_Modules.TradM_OEM as TM
    import Database.Trading_DataPd as TradDat
    import Database.DTRecoveryModule as DTrec
    import Database.Daily_DataMi as DayDat
    import PullOffModule as PLOf
    from datetime import datetime, date
    from email.message import EmailMessage
    import math as mt
    import numpy as np
    import mysql.connector
    import smtplib
    import ssl
    import sys
    import traceback

    Excp = 0

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = ""
    receiver_email = ""
    password = ''

    Database = mysql.connector.connect(
        host="",
        user="root",
        passwd="")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    Database.commit()

    MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "Running" WHERE PK = "Status" '
    my_cursor.execute(MTsrecord)
    nowdat = datetime.now()
    Term = (f"{nowdat}\n"
            f"\n"
            f"Briareos Terminal Module Starting ...\n"
            f"\n")

    MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    query = f"SELECT Inception_Date " \
            f"FROM Miscellaneous " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    inceptdate = col[0][0]
    daycount = (date.today() - inceptdate).days

    query = f"SELECT date "\
            f"FROM Cryptos " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    DiffGT = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)
    DT_daysGT = mt.floor(DiffGT/24)

    query = f"SELECT date "\
            f"FROM BTCUSDTh " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DiffTD = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    query = f"SELECT date "\
            f"FROM ShortTradingSig " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DiffSTSg = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    query = f"SELECT date "\
            f"FROM port_values_long " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DiffPVL = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    query = f"SELECT date "\
            f"FROM profit_loss " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    DBdate = col[0][0]
    DBdate = datetime(DBdate.year, DBdate.month, DBdate.day, DBdate.hour)
    DiffPL = mt.floor(24*(datetime.now() - DBdate).days + (datetime.now() - DBdate).seconds/3600)

    query = f"SELECT date "\
            f"FROM BTC_SStrt " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    OPTdt = (datetime.now() - DBdate).days

    query = f"SELECT date "\
            f"FROM PortfolioOptL " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    datedb = col[0][0]
    DBdate = datetime(datedb.year, datedb.month, datedb.day)
    POPTdt = (datetime.now() - DBdate).days

    query = f"SELECT TOptModule " \
            f"FROM exception_terminal " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    TOptS = col[0][0]

    query = f"SELECT Pred_PMM " \
            f"FROM exception_terminal " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    POptS = col[0][0]

    time.sleep(10)  # wait time for API's data

    # Database
    print("Database Queries Starting ...")

    Termy = (f"Database queries Starting ...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    try:
        if (DT_daysGT > 1 and datetime.now().hour > 8) or DiffTD > 2 or DiffSTSg > 1 or DiffPVL > 1 or DiffPL > 1:

            msg = EmailMessage()
            msg.set_content(f"Downtime Alert.\n"
                            f"\n"
                            f"Downtime Recovery Module executing.\n"
                            f"\n"
                            f"Downtime = {DiffSTSg-1}h.\n")

            msg['Subject'] = "Briareos Downtime"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)

            print(f"DTRecovery required, DT={DiffSTSg-1}h, Executing ...")
            DTpy = 1
            DTrec.DTRecovery()
            print("DTRecovery Executed")
        if datetime.now().hour == 8:
            print("Daily Data query running ...")
            DTpy = 2
            DayDat.DailyData()
            print("Daily Data query Executed.")

        # continuous
        DTpy = 3
        print("Trading Data query Running ...")
        TradDat.Trading_Data()
        print("Trading Data query Executed.")

        Termy = (f"Database queries Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

        print("Data acquisition completed")
    except Exception as e:
        print("Database (feed) in experiencing Problems")
        print("System had to Terminate early")
        Excp = 1

        msg = EmailMessage()
        msg.set_content(f"Database (feed) in experiencing Problems.\n"
                        f"System had to Terminate early.\n"
                        f"\n"
                        f"Exception (Module {DTpy}):\n"
                        f"\n"
                        f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                        f"{e}\n"
                        f"\n"
                        f"\n"
                        f"Traceback:\n"
                        f"\n"
                        f"{traceback.format_exc()}"
                        f"\n")

        msg['Subject'] = "Briareos System Error"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)

        MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "error" WHERE PK = "Status" '
        my_cursor.execute(MTsrecord)

        if DTpy == 1:
            MTsrecord = 'UPDATE Exception_Terminal SET DTRecovery = "error" WHERE PK = "Status" '
            my_cursor.execute(MTsrecord)
        elif DTpy == 2:
            MTsrecord = 'UPDATE Exception_Terminal SET DailyData = "error" WHERE PK = "Status" '
            my_cursor.execute(MTsrecord)
        elif DTpy == 3:
            MTsrecord = 'UPDATE Exception_Terminal SET TradingData = "error" WHERE PK = "Status" '
            my_cursor.execute(MTsrecord)

        Termy = (f"Database queries is experiencing Problems.\n"
                 f"System had to Terminate early.\n"
                 f"\n"
                 f"Exception (Module {DTpy}):\n"
                 f"\n"
                 f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                 f"{e}\n"
                 f"\n"
                 f"\n"
                 f"Traceback:\n"
                 f"\n"
                 f"{traceback.format_exc()}"
                 f"\n")
        Term = Term + Termy
        Term = Term.replace('"', "'")
        MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal"'
        my_cursor.execute(MTrecord)
        Database.commit()
        time.sleep(60)  # wait for minute to end to avoid Always-up reviving process in same instant
        quit()  # TODO: Warning! This will trigger scheduler termination. (although Always up will revive process)

    # Optimization Module (System 1)

    if ((np.mod(daycount, 5) == 0 or np.mod(daycount+1, 28) == 0) and datetime.now().hour == 8) \
            or (OPTdt > 5 and TOptS != "Running"):
        print("System 1 Starting ...")
        Termy = (f"Optimization Module Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()
        try:
            cluster1 = dispy.JobCluster(Topt.tradingopt, nodes=["192.168.1.3"])
            time.sleep(3)
            Tsk1 = cluster1.submit_node("192.168.1.3")
            time.sleep(1)
            Job1 = cluster1.node_jobs('192.168.1.3')
            print(f"Job1 = {Job1}")
            cluster1.close_node("192.168.1.3")
            if Job1 == -1:
                print("System 1 is experiencing problems")

                msg = EmailMessage()
                msg.set_content("System 1 is experiencing problems (Dispy).\n"
                                "\n"
                                "Workload was not assigned.\n")

                msg['Subject'] = "Briareos System Error"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)

                MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "error" WHERE PK = "Status" '
                my_cursor.execute(MTsrecord)
                Termy = (f"Optimization Module is experiencing Problems (Dispy).\n"
                         f"\n"
                         f"Workload was not assigned.\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f"UPDATE Exception_Terminal SET Bri_Terminal = '{Term}' WHERE PK = 'Terminal'"
                my_cursor.execute(MTrecord)
                Database.commit()
                Excp = 1
            else:
                print("Task 1 assigned, System 1 Running")
                Termy = (f"Task 1 assigned, System 1 Running.\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()
        except Exception as e:
            print("System 1 is experiencing problems")

            MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "error" WHERE PK = "Status" '
            my_cursor.execute(MTsrecord)
            Termy = (f"Optimization Module is experiencing Problems (Dispy).\n"
                     f"\n"
                     f"Exception:\n"
                     f"\n"
                     f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                     f"{e}\n"
                     f"\n"
                     f"\n"
                     f"Traceback:\n"
                     f"\n"
                     f"{traceback.format_exc()}"
                     f"\n")
            Term = Term + Termy
            Term = Term.replace('"', "'")
            MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal"'
            my_cursor.execute(MTrecord)
            Database.commit()

            msg = EmailMessage()
            msg.set_content(f"System 1 is experiencing problems.\n"
                            f"\n"
                            f"Exception:\n"
                            f"\n"
                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                            f"{e}\n"
                            f"\n"
                            f"\n"
                            f"Traceback:\n"
                            f"\n"
                            f"{traceback.format_exc()}"
                            f"\n")

            msg['Subject'] = "Briareos System Error"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)

            Excp = 1

    # Predictions and Portfolio Management Module (System 2)

    if (np.mod(daycount, 7) == 0 and datetime.now().hour == 8) or (POPTdt > 7 and POptS != "Running"):
        print("System 2 Starting ...")
        Termy = (f"Predictions and Portfolio Management Module Starting ...\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()
        try:
            cluster2 = dispy.JobCluster(PPMM.predictionport, nodes=["192.168.1.4"])
            time.sleep(2)
            Tsk2 = cluster2.submit_node("192.168.1.4")
            time.sleep(1)
            Job2 = cluster2.node_jobs('192.168.1.4')
            print(f"Job2 = {Job2}")
            cluster2.close_node("192.168.1.4")
            if Job2 == -1:
                print("System 2 is experiencing problems")

                msg = EmailMessage()
                msg.set_content("System 2 is experiencing problems (dispy).\n"
                                "\n"
                                "Workload was not assigned.\n")

                msg['Subject'] = "Briareos System Error"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)

                MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "error" WHERE PK = "Status" '
                my_cursor.execute(MTsrecord)
                Termy = (f"Predictions and PMM is experiencing Problems (Dispy).\n"
                         f"\n"
                         f"Workload was not assigned or terminated too early.\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()
                Excp = 1
            else:
                print("Task 2 assigned, System 2 Running")
                Termy = (f"Task 2 assigned, System 2 Running.\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()
        except Exception as e:
            print("System 2 is experiencing problems")

            msg = EmailMessage()
            msg.set_content(f"System 2 is experiencing problems.\n"
                            f"\n"
                            f"Exception:\n"
                            f"\n"
                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                            f"{e}\n"
                            f"\n"
                            f"\n"
                            f"Traceback:\n"
                            f"\n"
                            f"{traceback.format_exc()}"
                            f"\n")

            msg['Subject'] = "Briareos System Error"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)

            MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "error" WHERE PK = "Status" '
            my_cursor.execute(MTsrecord)
            Termy = (f"Predictions and PMM is experiencing Problems (Dispy).\n"
                     f"\n"
                     f"Exception:\n"
                     f"\n"
                     f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                     f"{e}\n"
                     f"\n"
                     f"\n"
                     f"Traceback:\n"
                     f"\n"
                     f"{traceback.format_exc()}"
                     f"\n")
            Term = Term + Termy
            Term = Term.replace('"', "'")
            MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal"'
            my_cursor.execute(MTrecord)
            Database.commit()
            Excp = 1

    # Trading and Order Execution Module (System 3)
    # continuous

    Termy = (f"Trading and OEM Module Starting ...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    if np.mod(daycount, 30) == 0 and datetime.now().hour == 0 and daycount > 1:
        EMrecord = "UPDATE ExecutionCom SET payout = 1"
        my_cursor.execute(EMrecord)
        Database.commit()

    if True: #Change for Binance scheduled updates
        print("System 3 Starting ...")
        try:
            if False: # pull of (sell all) for Binance scheduled updates
                cluster3 = dispy.JobCluster(PLOf.PullOffModule, nodes=["192.168.1.7"])
            else:
                cluster3 = dispy.JobCluster(TM.tradingmodule, nodes=["192.168.1.7"])
            time.sleep(2)
            Tsk3 = cluster3.submit_node("192.168.1.7")
            time.sleep(1)
            Job3 = cluster3.node_jobs("192.168.1.7")
            print(f"Job3 = {Job3}")
            cluster3.close_node("192.168.1.7")
            if Job3 == -1:
                print("System 3 is experiencing problems")

                msg = EmailMessage()
                msg.set_content("System 3 is experiencing problems (dispy).\n"
                                "Workload was not assigned.\n"
                                "\n")

                msg['Subject'] = "Briareos System Error"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)

                MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "error" WHERE PK = "Status" '
                my_cursor.execute(MTsrecord)
                Termy = (f"Trading and OEM is experiencing Problems (Dispy).\n"
                         f"\n"
                         f"Workload was not assigned or terminated too early.\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()
                Excp = 1
            else:
                print("Task 3 assigned, System 3 Running")
                Termy = (f"Task 3 assigned, System 3 Running.\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()

        except Exception as e:
            print("System 3 is experiencing problems")

            msg = EmailMessage()
            msg.set_content(f"System 3 is experiencing problems.\n"
                            f"\n"
                            f"Exception:\n"
                            f"\n"
                            f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                            f"{e}\n"
                            f"\n"
                            f"\n"
                            f"Traceback:\n"
                            f"\n"
                            f"{traceback.format_exc()}"
                            f"\n")

            msg['Subject'] = "Briareos System Error"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)

            MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "error" WHERE PK = "Status" '
            my_cursor.execute(MTsrecord)
            Termy = (f"Trading and OEM is experiencing Problems (Dispy).\n"
                     f"\n"
                     f"Exception:\n"
                     f"\n"
                     f"Error on line {sys.exc_info()[-1].tb_lineno}\n"
                     f"{e}\n"
                     f"\n"
                     f"\n"
                     f"Traceback:\n"
                     f"\n"
                     f"{traceback.format_exc()}"
                     f"\n")
            Term = Term + Termy
            Term = Term.replace('"', "'")
            MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal"'
            my_cursor.execute(MTrecord)
            Database.commit()
            Excp = 1

    if Excp == 0:
        MTsrecord = 'UPDATE Exception_Terminal SET Bri_Terminal = "idle" WHERE PK = "Status" '
        my_cursor.execute(MTsrecord)
        Termy = (f"Briareos Terminal Completed Execution Successfully\n"
                 f"\n"
                 f"{datetime.now()}\n"
                 f"\n")
        Term = Term + Termy
        Term = Term.replace('"', "'")
        MTrecord = f'UPDATE Exception_Terminal SET Bri_Terminal = "{Term}" WHERE PK = "Terminal"'
        my_cursor.execute(MTrecord)
        Database.commit()
