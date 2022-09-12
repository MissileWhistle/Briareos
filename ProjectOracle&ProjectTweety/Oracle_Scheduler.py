import time
import numpy as np
from datetime import datetime, date
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl
import sys
import traceback
import glob
import os
import stripe as st

port = 465
smtp_server = "smtp.gmail.com"
sender_email = ""
receiver_email = ""
passwordT = ''

st.api_key = ""

pastmails = []
with open('sublist.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        email = line[:-1]
        # add item to the list
        pastmails.append(email)

while True:
    Ndate = datetime.now()
    if np.mod(Ndate.second, 2) == 0:

        # check for new subscrivers on Stripe
        Custms = st.Customer.list(limit=10000000)
        submails = []
        names = []
        for i in range(len(Custms)):
            submails += [Custms["data"][i]["email"]]
            names += [Custms["data"][i]["name"]]
        i = 0
        # send email to new members
        for mail in submails:
            if mail not in pastmails:
                try:
                    folder = r'C:\Users\HC.deptR&D\Desktop\Reports'
                    files_path = os.path.join(folder, '*')
                    files = sorted(
                        glob.iglob(files_path), key=os.path.getctime, reverse=True)
                    Tdate = files[0][-14:-4]

                    body = f"Hello {names[i]}!\n" \
                           f"\n" \
                           f"Welcome to the team. Here at HC.dept we aim to provide a simple and straightforward " \
                           f"analysis of the Crypto Market, including BTC, ETH, XMR and XRP. Our report is delivered " \
                           f"to you weekly, every Saturday at 8AM UTC. This is intended for everyone looking to gain insight " \
                           f"into the Crypto Market and prepare for the weeks ahead.\n" \
                           f"\n" \
                           f"Here's your latest weekly report. Enjoy and be objective.\n" \
                           f"You can expect a new report by Saturday, 8AM UTC.\n" \
                           f"\n" \
                           f"Best regards;\n" \
                           f"HC.dept\n"

                    sender = "hc.dept.report@gmail.com"
                    password = 'EcW90HjzEtwl'

                    receiver = mail

                    # Setup the MIME
                    message = MIMEMultipart()
                    message['From'] = sender
                    message['To'] = mail
                    message['Subject'] = f"HC.dept Weekly Report {Tdate}"

                    message.attach(MIMEText(body, 'plain'))

                    pdfloc = fr'C:\Users\HC.deptR&D\Desktop\Reports\HCdept_Weekly_Report_{Tdate}.pdf'

                    binary_pdf = open(pdfloc, 'rb')

                    payload = MIMEBase('application', 'octate-stream', Name=f"HCdept_Weekly_Report_{Tdate}.pdf")
                    payload.set_payload((binary_pdf).read())
                    encoders.encode_base64(payload)
                    payload.add_header('Content-Decomposition', 'attachment', filename=f"HCdept_Weekly_Report_{Tdate}.pdf")
                    message.attach(payload)

                    session = smtplib.SMTP('smtp.gmail.com', 587)
                    session.starttls()
                    session.login(sender, password)

                    text = message.as_string()
                    session.sendmail(sender, mail, text)
                    session.quit()
                    print('New Subscriber! Email Sent')
                except Exception as e:
                    # Email me if problems found
                    print("Scheduler is Experiencing Problems")
                    msg = EmailMessage()
                    msg.set_content(f"Oracle Scheduler is experiencing problems (Subscriber Mail).\n"
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

                    msg['Subject'] = "Oracle Scheduler Error"
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, passwordT)
                        server.send_message(msg)
            i += 1
        pastmails = submails
        with open('sublist.txt', 'w') as filehandle:
            for listitem in submails:
                filehandle.write('%s\n' % listitem)
        time.sleep(1)

    # depending on date and time post a new tweet on Twitter or generate and send a report to subscribers
    if Ndate.minute == 00 and (Ndate.hour == 9 or Ndate.hour == 17):
        from TwitterBot import TwitterBot
        print('Twitter Run Starting at:')
        print(f"{datetime.now()}\n")
        try:
            TwitterBot(Ndate)
            print('\nTweet Posted Successfully.')
            print(f"{datetime.now()}\n")
            time.sleep(60)
        except Exception as e:
            print("Scheduler is Experiencing Problems")
            msg = EmailMessage()
            msg.set_content(f"Oracle Scheduler is experiencing problems (Twitter).\n"
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

            msg['Subject'] = "Oracle Scheduler Error"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, passwordT)
                server.send_message(msg)
            time.sleep(60)

    if Ndate.minute == 6 and Ndate.hour == 9 and date.today().weekday() == 5:
        from Report import Report
        print('Report Run Starting at:')
        print(f"{datetime.now()}\n")
        try:
            Report()
            print('\nReports Sent Successfully.')
            print(f"{datetime.now()}\n")
            time.sleep(60)
        except Exception as e:
            print("Scheduler is Experiencing Problems")
            msg = EmailMessage()
            msg.set_content(f"Oracle Scheduler is experiencing problems (Report).\n"
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

            msg['Subject'] = "Oracle Scheduler Error"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, passwordT)
                server.send_message(msg)
            time.sleep(60)

