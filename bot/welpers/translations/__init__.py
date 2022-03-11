from bot import Config
from bot.welpers.translations import en
lang = None

if Config.LANGUAGE == "EN":
    lang = en.EN
