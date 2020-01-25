from bs4 import BeautifulSoup
import requests as req
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def getDtfInfo(bot, update):
    try:
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
            resStr += titleText + "\n" + divHref['href'] + "\n"

        bot.send_message(chat_id=update.message.chat_id, text=resStr)
    except BaseException as baseError:
        logger.warning('dtfInfo "%s" caused error "%s"', bot, baseError)
        bot.send_message(chat_id=update.message.chat_id, text='Some error happen')


def getNPlusInfo(bot, update):
    try:
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
                resStr += titleText + "\n" + "https://nplus1.ru" + divHref['href'] + "\n"

        bot.send_message(chat_id=update.message.chat_id, text=resStr)
    except BaseException as baseError:
        logger.warning('nPlus "%s" caused error "%s"', bot, baseError)
        bot.send_message(chat_id=update.message.chat_id, text='Some error happen')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ["TG_KEY"])

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