from Insta.insta import InstaBot


with InstaBot(browser="firefox") as bot:
    bot.get_url()
    bot.login()
    bot.do_something()
