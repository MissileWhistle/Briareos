# This module is responsible for creating a streamlit dashboard for monitoring of the
# algorithmic training system, it monitors the execution of each module of the system
# printing in a non-interactive like terminal messages that report the status of the module.
# It also shows execution times of each module and time elapsed since, and fundamental variables
# # to the whole system


# Import Modules

import mysql.connector
import pandas
from datetime import datetime, date
import numpy as np
import streamlit as st

# Connect to Database
Database = mysql.connector.connect(
    host="",
    user="",
    passwd="")

my_cursor = Database.cursor()

my_cursor.execute("USE briareos")

# Create Dashboard

# Exception Management Module
st.sidebar.title("Briareos Exception Management")


# Trading Data Terminal

if st.sidebar.checkbox('Trading Data'):
    st.title('Trading Data Terminal')

    TDTerminal = f"SELECT PK, TradingData " \
                 f"FROM exception_terminal "
    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    TD = pandas.DataFrame(col)
    st.header(f'Status: {str(col[0][1])}')
    st.subheader('Terminal: ')
    st.write(str(col[1][1]))

if st.sidebar.checkbox('Daily Data'):
    st.title('Daily Data Terminal')

    TDTerminal = f"SELECT PK, DailyData " \
                 f"FROM exception_terminal "
    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    TD = pandas.DataFrame(col)
    st.header(f'Status: {str(col[0][1])}')
    st.subheader('Terminal: ')
    st.write(str(col[1][1]))

if st.sidebar.checkbox('DTRecovery'):
    st.title('Downtime Recovery Terminal')

    TDTerminal = f"SELECT PK, DTRecovery " \
                 f"FROM exception_terminal "
    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    TD = pandas.DataFrame(col)
    st.header(f'Status: {str(col[0][1])}')
    st.subheader('Terminal: ')
    st.write(str(col[1][1]))

if st.sidebar.checkbox('TOptModule'):
    st.title('Trading Optimization Terminal')

    TDTerminal = f"SELECT PK, TOptModule " \
                 f"FROM exception_terminal "
    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    TD = pandas.DataFrame(col)
    st.header(f'Status: {str(col[0][1])}')
    st.subheader('Terminal: ')
    st.write(str(col[1][1]))

if st.sidebar.checkbox('Pred_PMM'):
    st.title('Prediction and PMM Terminal')

    TDTerminal = f"SELECT PK, Pred_PMM " \
                 f"FROM exception_terminal "
    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    TD = pandas.DataFrame(col)
    st.header(f'Status: {str(col[0][1])}')
    st.subheader('Terminal: ')
    st.write(str(col[1][1]))

if st.sidebar.checkbox('Trad_OEM'):
    st.title('Trading and OEM Terminal')

    TDTerminal = f"SELECT PK, Trad_OEM " \
                 f"FROM exception_terminal "
    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    TD = pandas.DataFrame(col)
    st.header(f'Status: {str(col[0][1])}')
    st.subheader('Terminal: ')
    st.write(str(col[1][1]))

if st.sidebar.checkbox('Bri_Terminal'):
    st.title('Briareos Terminal')

    TDTerminal = f"SELECT PK, Bri_Terminal " \
                 f"FROM exception_terminal "
    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    TD = pandas.DataFrame(col)
    st.header(f'Status: {str(col[0][1])}')
    st.subheader('Terminal: ')
    st.write(str(col[1][1]))

if st.sidebar.checkbox('M. Counter'):
    st.title('Modules Counters')

    TDTerminal = f"SELECT * " \
                 f"FROM exception_terminal " \
                 f"LIMIT 1 "

    my_cursor.execute(TDTerminal)
    col = my_cursor.fetchall()
    status = col[0][1:]

    query = f"SELECT Inception_date " \
            f"FROM Miscellaneous " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    incept = col[0][0]
    daycount = (date.today() - incept).days

    query = f"SELECT date " \
            f"FROM btc_svarosc " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    dbdate = col[0][0]
    SVARdt = datetime(dbdate.year, dbdate.month, dbdate.day)

    query = f"SELECT date " \
            f"FROM btc_lvarosc " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    dbdate = col[0][0]
    LVARdt = datetime(dbdate.year, dbdate.month, dbdate.day)

    query = f"SELECT date " \
            f"FROM btc_sstrt " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    dbdate = col[0][0]
    SGOdt = datetime(dbdate.year, dbdate.month, dbdate.day)

    query = f"SELECT date " \
            f"FROM btc_lstrt " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    dbdate = col[0][0]
    LGOdt = datetime(dbdate.year, dbdate.month, dbdate.day)

    query = f"SELECT date " \
            f"FROM btcpopt " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    dbdate = col[0][0]
    PrOpdt = datetime(dbdate.year, dbdate.month, dbdate.day)

    query = f"SELECT date " \
            f"FROM payout " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    dbdate = col[0][0]
    POdt = datetime(dbdate.year, dbdate.month, dbdate.day)

    query = f"SELECT date " \
            f"FROM portfolioopts " \
            f"ORDER BY date DESC " \
            f"LIMIT 1 "
    my_cursor.execute(query)
    col = my_cursor.fetchall()
    dbdate = col[0][0]
    PPdt = datetime(dbdate.year, dbdate.month, dbdate.day)

    mctdta = {'Status': [f"{status[3]}", f"{status[3]}", f"{status[3]}", f"{status[3]}", f"{status[3]}",
                         f"{status[4]}", f"N/A"],
              'Run mod': [10, 5, 20, 10, 28, 7, 30],
              'daycount mod': [np.mod(daycount,10), np.mod(daycount, 5), np.mod(daycount, 20),
                               np.mod(daycount, 10), np.mod(daycount+1, 28), np.mod(daycount, 7), np.mod(daycount, 30)],
              'Last Run': [SVARdt, SGOdt, LVARdt, LGOdt, PrOpdt, PPdt, POdt],
              'delta t': [(datetime.today()-SVARdt).days, (datetime.today()-SGOdt).days,
                          (datetime.today()-LVARdt).days, (datetime.today()-LGOdt).days, (datetime.today()-PrOpdt).days,
                          (datetime.today()-PPdt).days, (datetime.today()-POdt).days]}
    Pdmetdta = pandas.DataFrame(mctdta, index=["Short Var.", "Short GO", "Long Var.", "Long GO", "PredOpt",
                                               "Pred_PMM", "Pay-out"])
    st.table(Pdmetdta)

    TDmisc = f"SELECT * " \
             f"FROM miscellaneous " \
             f"LIMIT 1 "
    my_cursor.execute(TDmisc)
    col = my_cursor.fetchall()
    misce = col[0]

    st.write('### Miscellaneous')

    metdta = {'t': misce[0], 'MinPort': misce[1], 'SavRate': misce[2], 'Incept. date': misce[3], 'daycount': daycount}
    Pdmetdta = pandas.DataFrame(metdta, index=[''])
    st.table(Pdmetdta)
