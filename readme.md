
*Test version of application - https://telegram.me/notatnik_Bot*

TODO:
------
~~- correct arguments for sql requests~~

~~- test console version~~

~~- start to work with python telegram bot api (pip install python-telegram-bot)~~

~~- Google chart~~

- Microsoft oxford project (https://www.microsoft.com/cognitive-services/en-us/face-api). When we send a photo to bot, they will return age and gender


- use flask for database management

- Replace get_Updates method with webhook, but they require ssl. Now try to use self-signed certificate (generate them with: 'openssl req -new -x509 -nodes -newkey rsa:2048 -keyout webhook_cert.key -out webhook_cert.crt -days 365')

- try to host them somewhere. google_appengine is unsuitable, couse they work only with python27. Now i try Heroku.
