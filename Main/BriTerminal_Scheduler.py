# This module is responsible for the execution of the module that divides workload through the whole system, thus
# maintaining the execution of the system in periodic intervals (hourly)

# import modules
from Module_Terminal import BriareosTerminal
import time
from datetime import datetime
from email.message import EmailMessage
import smtplib
import ssl
import sys
import traceback

# set up e-mail variables to auto send email in case of error
port = 465
smtp_server = ""
sender_email = ""
receiver_email = ""
password = ''

# run infinite loop
while True:
    if datetime.now().minute == 00:
        print('Run Starting at:')
        print(f"{datetime.now()}\n")
        try:
            BriareosTerminal()
        except Exception as e:
            print("Scheduler is Experiencing Problems")
            msg = EmailMessage()
            msg.set_content(f"Scheduler is experiencing problems.\n"
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

            msg['Subject'] = "Briareos Scheduler Error"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)
        print('\nRun Executed.')
        print(f"{datetime.now()}\n")
    time.sleep(60)
