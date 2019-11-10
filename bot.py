import sys
import yaml
import time
import logging
import botutils
import menubuilder
from telegram import utils, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, Filters
from spellbook import Spellbook

# Set logging level
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MENU, NAME, LEVEL, NAME_LEVEL = range(4)
BARBARIC, BARD, CLERIC, DRUID, MAGE, PALADIN, RANGER, WARLOCK, WIZARD = range(9)
LEVELS = range(10)


def start(update, context):
    reply_keyboard = [('Nome', NAME), ('Livello', LEVEL), ('Classe e Livello', NAME_LEVEL)]

    update.message.reply_text(
        'Ricerca incantesimo per:',
        reply_markup=InlineKeyboardMarkup(menubuilder.build_tuple_menu(reply_keyboard, 2)))
    return MENU


def name_search(update, context):
    print(update)
    query = update.callback_query
    query.edit_message_text('Ricerca incantesimo per:')


def class_search(update, context):
    keyboard_classes = [('Barbaro', BARBARIC), ('Bardo', BARD), ('Chierico', CLERIC), ('Druiro', DRUID), ('Mago', MAGE),
               ('Paladino', PALADIN), ('Ranger', RANGER), ('Stregone', WIZARD), ('Warlock', WARLOCK)]

    query = update.callback_query
    bot = context.bot
    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Seleziona il livello per cui cercare:',
        reply_markup=InlineKeyboardMarkup(menubuilder.build_tuple_menu(keyboard_classes, 5)))


def level_search(update, context):
    keyboard_levels = [('Lv. 0', LEVELS[0]), ('Lv. 1', LEVELS[1]), ('Lv. 2', LEVELS[2]), ('Lv. 3', LEVELS[3]),
              ('Lv. 4', LEVELS[4]),
              ('Lv. 5', LEVELS[5]), ('Lv. 6', LEVELS[6]), ('Lv. 7', LEVELS[7]), ('Lv. 8', LEVELS[8]),
              ('Lv. 9', LEVELS[9])]

    query = update.callback_query
    bot = context.bot
    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Seleziona il livello per cui cercare:',
        reply_markup=InlineKeyboardMarkup(menubuilder.build_tuple_menu(keyboard_levels, 5)))


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
    try:
        env_dict = botutils.get_environment()
    except OSError as ex:
        sys.exit("Be sure that \"env.yaml\" file exists and you have read access to it!")

    env_errors = botutils.check_env_requirements(env_dict)
    if env_errors:
        sys.exit(env_errors)
    db_data = {
        'DB_USERNAME': env_dict['DB_USERNAME'],
        'DB_PASSWORD': env_dict['DB_PASSWORD'],
        'DB_URL': env_dict['DB_URL'] if 'DB_URL' in env_dict else None,
        'DB_PORT': env_dict['DB_PORT'] if 'DB_PORT' in env_dict else None,
        'DB_NAME': env_dict['DB_NAME'] if 'DB_NAME' in env_dict else None,
    }
    spellbook = Spellbook(db_data['DB_USERNAME'], db_data['DB_PASSWORD'], url=db_data['DB_URL'],
                          db_name=db_data['DB_NAME'], db_port=db_data['DB_PORT'])

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
