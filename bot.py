import sys
import yaml
import time
import logging
import telegram
from telegram import utils, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, Filters
from spellbook import Spellbook


# Set logging level
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Read the environment file
def get_environment():
    """
    Get environment variables.
    :return: Dictionary with environment variables
    """
    env_dict = None
    try:
        with open('env.yaml', 'r') as f:
            env_dict = yaml.load(f, Loader=yaml.FullLoader)
    except OSError as ex:
        sys.exit("Be sure that \"env.yaml\" file exists and you have read access to it!")
    return env_dict


def check_env_requirements(env_dict):
    """
    Check if environment dictionary has all minimum required variables.
    :param env_dict:
    :return: Empty string if variables are ok. String with errors description otherwise
    """
    errors_description = ""
    if not env_dict or 'SECRET_BOT_TOKEN' not in env_dict:
        errors_description += "Be sure to have the \"SECRET_BOT_TOKEN\" value set in the \"env.yaml\"\n"
    if not env_dict or 'DB_USERNAME' not in env_dict:
        errors_description += "Be sure to have the \"DB_USERNAME\" value set in the \"env.yaml\" to correctly connect to the DB\n"
    if not env_dict or 'DB_PASSWORD' not in env_dict:
        errors_description += "Be sure to have the \"DB_PASSWORD\" value set in the \"env.yaml\" to correctly connect to the DB\n"
    return errors_description


MENU, NAME, LEVEL, NAME_LEVEL = range(4)
LEVELS = range(10)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def start(update, context):
    reply_keyboard = [('Nome', NAME), ('Livello', LEVEL), ('Classe e Livello', NAME_LEVEL)]
    button_list = [InlineKeyboardButton(s[0], callback_data=str(s[1])) for s in reply_keyboard]

    update.message.reply_text(
        'Ricerca incantesimo per:',
        reply_markup=InlineKeyboardMarkup(build_menu(button_list, 2)))
    return MENU


def name_search(update, context):
    print(update)
    query = update.callback_query
    query.edit_message_text('Ricerca incantesimo per:')


def level_search(update, context):
    levels = [('Lv. 0', LEVELS[0]), ('Lv. 1', LEVELS[1]), ('Lv. 2', LEVELS[2]), ('Lv. 3', LEVELS[3]), ('Lv. 4', LEVELS[4]),
              ('Lv. 5', LEVELS[5]), ('Lv. 6', LEVELS[6]), ('Lv. 7', LEVELS[7]), ('Lv. 8', LEVELS[8]), ('Lv. 9', LEVELS[9])]
    button_list = [InlineKeyboardButton(s[0], callback_data=str(s[1])) for s in levels]

    query = update.callback_query
    bot = context.bot
    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Seleziona il livello per cui cercare:',
        reply_markup=InlineKeyboardMarkup(build_menu(button_list, 5)))


def name_level_search(update, context):
    query = update.callback_query
    query.edit_message_text('Ricerca incantesimo per classe e nome:')


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Ciao! Spero di riverderti qui!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Get env variables and initialize Spellbook instance
    env_dict = get_environment()
    env_errors = check_env_requirements(env_dict)
    if env_errors:
        sys.exit(env_errors)
    db_data = {
        'DB_USERNAME': env_dict['DB_USERNAME'],
        'DB_PASSWORD': env_dict['DB_PASSWORD'],
        'DB_URL': env_dict['DB_URL'] if 'DB_URL' in env_dict else None,
        'DB_PORT': env_dict['DB_PORT'] if 'DB_PORT' in env_dict else None,
        'DB_NAME': env_dict['DB_NAME'] if 'DB_NAME' in env_dict else None,
    }
    spellbook = Spellbook(db_data['DB_USERNAME'], db_data['DB_PASSWORD'], url=db_data['DB_URL'], db_name=db_data['DB_NAME'], db_port=db_data['DB_PORT'])
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(env_dict['SECRET_BOT_TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [
                CallbackQueryHandler(name_search, pattern='^{}$'.format(NAME)),
                CallbackQueryHandler(level_search, pattern='^{}$'.format(LEVEL)),
                CallbackQueryHandler(name_level_search, pattern='^{}$'.format(NAME_LEVEL))
            ],
            LEVEL: [],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info('Bot Started!')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
