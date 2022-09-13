
Both project here rely on the Briareos Database and so are considered subproject. Again comments are scarce.


Project Oracle 

This is an automatically generated Analysis report of the Cryptocurrencies Market, generated every week and sent to subscribers by email. Programmed in Python. Fully autonomous report generation and email. An example of the report can be seen here (file HCdept_WeeklyMarketReport_210909.pdf).
The file Report.py produces the report using the package fpdf. The subscribers (emails and names) where taken from a list of friends that would get it for free and a list of subscribers from Stripe, a service that allows you to charge a montly fee to people for a product, using Stripe's API.


Project Tweety

This is a Twitter bot (using the Twitter API) that posts tweets with information about the currect status and trends of the Crypto Market and sever specific currencies, it also attempted to provide predictions. The account and several post can be seen on https://twitter.com/hc_dept. The types of post where scheduled and diverse.
The file TwitterBot.py has all the code


Both this projects (modules) ran on the same machine and shared a common scheduler. The file Oracle_Scheduler.py runs an infinite loop that every two seconds runs. It starts by checking if new subscribers existed, if so an e-mail with the lattest reposrt was sent to them, afterwards it checks if its time to post a new tweet or generate and send the weekly report to subscribers. The file sublist.txt stored the email of subcribers and serves to check if new subscrivers exist.


Again if problems where found during the execution of the modules it would send an email reporting those problems.
