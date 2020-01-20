from bs4 import BeautifulSoup
import requests as req
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def getDtfInfo(bot, update):
    resp = req.get("https://dtf.ru/")
    soup = BeautifulSoup(resp.text, 'lxml')

    resStr: str = ""

    mySpan = soup.findAll("span", {"class": "content-editorial-tick"})
    for span in mySpan:
        span.decompose()

    myDivs = soup.findAll("div", {"class": "feed__item"})
    for div in myDivs:
        divTitle = div.find("h2", {"class": "content-header__title"})
        titleText = divTitle.text.strip()
        # print(titleText)
        divHref = div.find("a", {"class": "content-feed__link"})
        # print(divHref['href'])
        resStr += titleText + "/n" + divHref['href'] + "/n"

    update.message.reply_text(resStr)


def getNPlusInfo(bot, update):
    resp = req.get("https://nplus1.ru/")
    soup = BeautifulSoup(resp.text, 'lxml')

    resStr = ""

    myArts = soup.findAll("article", {"class": "item"})
    for art in myArts:
        divTitle = art.find("h3")
        if divTitle is not None:
            titleText = divTitle.text.strip()
            # print(titleText)
            divHref = art.find("a")
            # print("https://nplus1.ru" + divHref['href'])
            resStr += titleText + "/n" + "https://nplus1.ru" + divHref['href'] + "/n"

    update.message.reply_text(resStr)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ["TG_KEY"], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("dtf", getDtfInfo))
    dp.add_handler(CommandHandler("nplus", getNPlusInfo))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()