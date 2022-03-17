# Guardian_TGbot

This is simple bot for Telegram which calculates insurance premium rates for voluntary liability insurance for vehicle owners. Bot written with the https://github.com/eternnoir/pyTelegramBotAPI

To run the bot put all the files in the same directory and execute main.py. Bear in mind that you must have python and pyTelegramBotAPI installed in the system.

DCV.json contents all the tariffs, sums insured and premiums amount for selected insurance type. 
SQLighter.py uses users.db as a finite state mashine to store the states of the users.

__TODO__
* need to be rewritten with async version of pyTelegramBotAPI
* requirments.txt has to be added 
