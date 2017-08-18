import logging
import os
import subprocess

import redis
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import apifetch

# adding a logger to monitor crashes and easier debugging

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='./telegbot.log',
                    format=LOG_FORMAT,
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger()


def get_token():
    token = os.getenv("FORUSHANDE_BOT")
    if token is None or not token:
        token = subprocess.call(["echo", "$FORUSHANDE_BOT"])

    if token:
        print(token)
        return token
    # raise Exception("Err: shell variable not fonud")


def start(bot, update):

    update.message.reply_text('خوش آمدید!')
    logger.info("start command used by {} ".format(update.message.from_user.first_name))
    logger.debug("new user << {} >>started the bot".format(update.message.from_user))

    reply_markup = parents_menu(bot, update)
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
    :param n_cols:  how many columns to show the butt,ons in
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
    logger.debug("a query was sent {}".format(query.data))
    if query.data[:4] == "caid:":
        bot.send_message(text="Selected option: %s" % query.data[5:],
                         chat_id=query.message.chat_id,
                         parse_mode='HTML')
        logger.debug("callback query handled by button")


def button_parent(bot, update):
    query = update.callback_query
    logger.debug("a query was sent {}".format(query.data))

    baseurl = "http://sunbyteit.com:8000/api/"
    suburl = "category/subs/all/{}".format(query.data[5:])
    child_categories = apifetch.fetch_json(baseurl, suburl)
    cat_names, cat_menu = gen_category(child_categories, "name", "id", "caid:")
    reply_markup = build_menu(cat_menu, n_cols=3)
    logger.debug("query handler built a menu")

    bot.send_message(text="Selected option: %s" % query.data[5:],
                     chat_id=query.message.chat_id,
                     reply_markup=reply_markup,
                     parse_mode='HTML')
    query.answer()
    logger.debug("callback query handled by button_parent")

def button_new(bot, update):
    query = update.callback_query

    bot.send_message(text="%s" % query.data,
                        chat_id=query.message.chat_id
                        )
    logger.debug("callback query handled by button_new")


def button_more(bot, update):
    query = update.callback_query
    if query[:4] == "more":
        bot.editMessageText(text="Selected option: %s" % query.data[5:],
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)
        logger.debug("callback query handled by button_more")


def parents_menu(bot, update):
    categories = apifetch.fetch_json("http://www.sunbyteit.com:8000/api/",
                                     "category/parents")
    # TODO: implement fetch from database instead of url
    logger.debug("update categories requested!")

    option_btn = 'name'
    callback = 'id'

    parent_names, button_list = gen_category(categories, option_btn, callback, "paid:")
    if len(parent_names) < 6:
        reply_markup = build_menu(button_list, n_cols=3)
    else:
        show_more = InlineKeyboardButton("بیشتر...", callback_data="more_categories")
        button_rest = button_list[6:]
        del button_list[6:]
        reply_markup = build_menu(button_list, n_cols=3, footer_buttons=[show_more])
    logger.debug("reply keyboard for category was returned")

    return reply_markup


def gen_category(categories, buttonfield, callbackfield, callbackheader):
    cat_names = []
    for item in categories:
        print(item)
        cat_names.append(item[buttonfield])
    logger.info("generated a list from the name of categories; {}".format(cat_names))

    button_list = [InlineKeyboardButton(s, callback_data=callbackheader + str(categories[cat_names.index(s)][callbackfield]))
                   for s in cat_names]
    return cat_names, button_list
