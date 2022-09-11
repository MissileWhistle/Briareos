# This module gathers hourly market data used by the algorithm by accessing Binance's API

def Trading_Data():
    from binance.client import Client
    import numpy as np
    from datetime import date, timedelta, datetime
    import mysql.connector as mysql

    Database = mysql.connect(
        host="192.168.1.5",
        user="root",
        passwd="Briareos")

    my_cursor = Database.cursor()

    my_cursor.execute("USE briareos")

    MTsrecord = 'UPDATE Exception_Terminal SET TradingData = "Running" WHERE PK = "Status" '
    my_cursor.execute(MTsrecord)
    Term = (f"{datetime.now()}\n"
            f"\n"
            f"Trading Data query Module Starting ...\n"
            f"\n")

    MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    Excp = 0

    # Crypto Price data (Binance API)

    client = Client("",
                    "")

    Cry_str = ['BTCUSDT', 'ETHUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'LINKUSDT', 'NEOUSDT']

    # Hourly data

    Termy = (f"Crypto price Hourly Data query starting ...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    Cry_PHdata = np.zeros((len(Cry_str), 5))
    j = 0
    for crypto in Cry_str:
        print(crypto)
        data = client.get_klines(symbol=crypto, interval=client.KLINE_INTERVAL_1HOUR)
        Cry_PHdata[j, :] = data[-2][1:6]
        j += 1

    metrc = ['open', 'high', 'low', 'close', 'volume']
    j = 0
    for crypto in Cry_str:
        record = f"INSERT IGNORE INTO {crypto}h ( date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"
        valus = (datetime.now() - timedelta(hours=1),)
        Cdata = Cry_PHdata[j, :]
        r = 0
        for data in Cdata:
            if data == 0 or data == 'NaN':
                query = f"SELECT {metrc[r]} " \
                        f"FROM {crypto}h " \
                        f"ORDER BY date DESC " \
                        f"LIMIT 1 "
                my_cursor.execute(query)
                valus += (my_cursor.fetchall()[0][0],)

                Termy = (f"Hourly {crypto} {data} problematic\n"
                         f"\n")
                Term = Term + Termy
                MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
                my_cursor.execute(MTrecord)
                Database.commit()
                Excp = 1
            else:
                valus += (float(data),)
            r += 1
        my_cursor.execute(record, valus)
        j += 1

    Database.commit()

    Termy = (f"Crypto price Hourly Data query completed Successfully.\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    # Daily data

    Termy = (f"Crypto price Daily Data query starting ...\n"
             f"\n")
    Term = Term + Termy
    MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
    my_cursor.execute(MTrecord)
    Database.commit()

    if datetime.now().hour == 0:
        Cry_PDdata = np.zeros((len(Cry_str), 5))
        j = 0
        for crypto in Cry_str:
            print(crypto)
            data = client.get_klines(symbol=crypto, interval=client.KLINE_INTERVAL_1DAY)
            Cry_PDdata[j, :] = data[-2][1:6]
            j += 1

        metrc = ['open', 'high', 'low', 'close', 'volume']
        j = 0
        for crypto in Cry_str:
            record = f"INSERT IGNORE INTO {crypto}d ( date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, " \
                     f"%s, %s) "
            valus = (date.today() - timedelta(days=1),)
            Cdata = Cry_PDdata[j, :]
            r = 0
            for data in Cdata:
                if data == 0 or data == 'NaN':
                    query = f"SELECT {metrc[r]} " \
                            f"FROM {crypto}d " \
                            f"ORDER BY date DESC " \
                            f"LIMIT 1 "
                    my_cursor.execute(query)
                    valus += (my_cursor.fetchall()[0][0],)

                    Termy = (f"Daily {crypto} {data} problematic\n"
                             f"\n")
                    Term = Term + Termy
                    MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
                    my_cursor.execute(MTrecord)
                    Database.commit()
                    Excp = 1
                else:
                    valus += (float(data),)
                r += 1
            my_cursor.execute(record, valus)
            j += 1

        Database.commit()

        Termy = (f"Crypto price Daily Data query Completed Successfully.\n"
                 f"\n")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)
        Database.commit()

    if Excp == 1:
        Termy = (f"Trading Data query Module completed.\n"
                 f"\n"
                 f"Some Data was unreliable."
                 f"\n"
                 f"{datetime.now()}")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)

        MTsrecord = 'UPDATE Exception_Terminal SET TradingData = "error" WHERE PK = "Status" '
        my_cursor.execute(MTsrecord)

        Database.commit()
    else:
        Termy = (f"Trading Data query Module completed Successfully.\n"
                 f"\n"
                 f"{datetime.now()}")
        Term = Term + Termy
        MTrecord = f'UPDATE Exception_Terminal SET TradingData = "{Term}" WHERE PK = "Terminal" '
        my_cursor.execute(MTrecord)

        MTsrecord = 'UPDATE Exception_Terminal SET TradingData = "idle" WHERE PK = "Status" '
        my_cursor.execute(MTsrecord)

        Database.commit()
