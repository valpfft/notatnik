
*Test version of application - https://telegram.me/notatnik_Bot*

TODO:
------
~~- correct arguments for sql requests~~

~~- test console version~~

~~- start to work with python telegram bot api (pip install python-telegram-bot)~~

~~- Google chart~~

- Microsoft oxford project (https://www.microsoft.com/cognitive-services/en-us/face-api). When we send a photo to bot, they will return age and gender


~~- use flask for database management~~

- Replace get_Updates method with webhook, but they require ssl. Now try to use self-signed certificate (generate them with: 'openssl req -new -x509 -nodes -newkey rsa:2048 -keyout webhook_cert.key -out webhook_cert.crt -days 365')
*Now it not a problem, couse every heroku domain had ssl. Thats work properly.*

- try to host them somewhere. google_appengine is unsuitable, couse they work only with python27. Now i try ~Heroku~.

A few bugs:
-----
- Sometimes, when app run on heroku with gunicorn, they send message twice. I think it something with thred's. Should learn more about it.

~~-After migration from sqlite to Postgre get_google_chart didn't work. *AttributeError: 'NoneType' object has no attribute 'fetchall'*~~

