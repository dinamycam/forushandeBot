import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telegbot

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='./bot.log',
                             format=LOG_FORMAT,
                             filemode='w',
                             level=logging.INFO)

logger = logging.getLogger()

token = telegbot.get_token()
updates = Updater(token)

logger.info("adding dispatchers")


updates.dispatcher.add_handler(CommandHandler('start', telegbot.start))
updates.dispatcher.add_handler(CallbackQueryHandler(telegbot.button))
updates.dispatcher.add_handler(CallbackQueryHandler(telegbot.button_more))
updates.dispatcher.add_handler(CommandHandler('help', telegbot.help))
# updates.dispatcher.add_handler(CommandHandler('end', telegbot.help))

logger.info("all commands configured")



updates.start_polling()
updates.idle()



