import os, subprocess
import logging
import apifetch
from telegram import bot
from telegram import update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import redis


# adding a logger to monitor crashes and easier debugging

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='./telegbot.log',
                    format=LOG_FORMAT,
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger()

# redis database
rds = redis.StrictRedis(host="localhost", port=6379, db=1)
stat = rds.get("status")
logger.info("in database, status is: {}".format(stat))


def get_token():
    token = os.getenv("FORUSHANDE_BOT")
    if token == None or token == '':
        token = subprocess.call(["echo", "$FORUSHANDE_BOT"])

    if token:
        # print(token)
        return token
    # raise Exception("Err: shell variable not fonud")




def start(bot, update):

    update.message.reply_text('خوش آمدید!')
    logger.info("start command used by {} ".format(update.message.from_user.first_name))
    logger.debug("new user << {} >>started the bot".format(update.message.from_user))

    reply_markup = gen_category(bot, update)
    logger.debug("a keyboard was generated from categories")
    # keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
    #             InlineKeyboardButton("Option 2", callback_data='2')],
    #
    #             [InlineKeyboardButton("Option 3", callback_data='3')]]
    #
    # reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a category:', reply_markup=reply_markup)
    # bot.send_message(update.message.chat_id, "you can search in these categories: ", reply_markup=reply_markup)
    logger.info("message with keyboard was sent")


def help(bot, update):

    update.message.reply_text(
        'Help\n'
        'dear ` {} `,\n'
        'here are the commands for this bot:\n'
        '/start - starts the bot\n'
        '/help - shows this message\n'
        '/hell - go to hell\n'.format(update.message.from_user.first_name))
    logger.debug("help message is set")
    logger.info("help command used by {}".format(update.message.from_user.first_name))


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    """
    :param buttons: a list of buttons
    :param n_cols:  how many columns to show the buttons in
    :param header_buttons:  list of buttons appended to the beginning
    :param footer_buttons:  list of buttons added to the end
    :return: the menu
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    print(buttons)
    logger.debug("buttons created")
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    logger.debug("header and footer buttons added")
    print(InlineKeyboardButton(menu))
    return InlineKeyboardMarkup(menu)


def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    logger.debug("callback query handled by button_edit")


def button_new(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    logger.debug("callback query handled by button_new")


def button_more(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    logger.debug("callback query handled by button_new")


def gen_category(bot, update):
    """
    Args:
        bot, update

    Returns:
        reply_markup
    """
    # categories = apifetch.fetch_json("http://www.sunbyteit.com:8000/api/", "categories")
    logger.debug("update categories requested!")
    categories = [{"name": "phones", "id":"100"},
                  {"name": "TV", "id":"5"},
                  {"name": "اسپینر", "id":"0"},
                  {"name": "tablets", "id":"1000"},
                  {"name": "phablets", "id":"200"},
                  {"name": "best", "id": "5000"}]

    option_btn = 'name'
    callback = 'id'

    cat_names = []
    for item in categories:
        print(item)
        cat_names.append(item[option_btn])
    logger.debug("generated a list from the name of categories; {}".format(cat_names))
    cat_names = ['xiaomi', 't4', 't3', 'سونی' , 'redmi', 'note'] #, 'موبایل']

    button_list = [InlineKeyboardButton(s, callback_data=str(categories[cat_names.index(s)][callback])) for s in cat_names]
    reply_markup = build_menu(button_list, n_cols=1)
    logger.debug("reply keyboard for category was returned")

    return reply_markup

