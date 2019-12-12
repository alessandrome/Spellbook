import sys
import yaml
import time
import logging
import botutils
import menubuilder
from telegram import utils, ChatAction, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, Filters
from spellbook import Spellbook

# Set logging level
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MENU, NAME, CHAR_CLASS, LEVEL, NAME_LEVEL = range(5)
BARBARIC, BARD, CLERIC, DRUID, MAGE, PALADIN, RANGER, WARLOCK, WIZARD = range(9)
LEVELS = range(10)


def overwrite_last_message_decorator(fn):
    def wrapper(self, *args, **kwargs):
        self._delete_last_message()
        return fn(self, *args, **kwargs)
    return wrapper


class SpellbookBot:
    def __init__(self, log_level=None):
        self.env_dict = botutils.get_environment()
        self._logger = botutils.set_logging(log_level)
        self._token = self.env_dict['SECRET_BOT_TOKEN']
        self.db_data = {
            'DB_USERNAME': self.env_dict['DB_USERNAME'],
            'DB_PASSWORD': self.env_dict['DB_PASSWORD'],
            'DB_URL': self.env_dict['DB_URL'] if 'DB_URL' in self.env_dict else None,
            'DB_PORT': self.env_dict['DB_PORT'] if 'DB_PORT' in self.env_dict else None,
            'DB_NAME': self.env_dict['DB_NAME'] if 'DB_NAME' in self.env_dict else None,
        }
        self.spellbook = Spellbook(self.db_data['DB_USERNAME'], self.db_data['DB_PASSWORD'], url=self.db_data['DB_URL'],
                                   db_name=self.db_data['DB_NAME'], db_port=self.db_data['DB_PORT'])
        self._updater = None
        self._dispatcher = None
        self._conversation_handler = None
        self._last_message = None
        self._conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.callback_start)],
            states={
                MENU: [
                    CallbackQueryHandler(self.callback_name_search, pattern='^{}$'.format(NAME)),
                    CallbackQueryHandler(self.callback_level_search, pattern='^{}$'.format(LEVEL)),
                    CallbackQueryHandler(self.callback_class_search, pattern='^{}$'.format(CHAR_CLASS)),
                    CallbackQueryHandler(self.callback_class_level_search, pattern='^{}$'.format(NAME_LEVEL))
                ],
                LEVEL: [
                    CallbackQueryHandler(self.callback_level_select, pattern='^\\d$'),
                ],
            },
            fallbacks=[CommandHandler('cancel', self.callback_cancel)]
    )

    def start(self):
        """Start the bot."""
        if self._updater is None:
            # Create the Updater and pass it your bot's token.
            # Make sure to set use_context=True to use the new context based callbacks
            # Post version 12 this will no longer be necessary
            self._updater = Updater(self._token, use_context=True)
            # Get the dispatcher to register handlers
            self._dispatcher = self._updater.dispatcher
            self._dispatcher.add_handler(self._conv_handler)
            self._dispatcher.add_error_handler(self._dispatcher_error_handler)
            self._updater.start_polling()
            self._logger.info('Bot Started')
        else:
            self._logger.warning("The BOT is already Up")
        return self._updater

    def stop(self):
        """Stop the bot."""
        if self._updater is not None:
            self._updater.stop()
            self._updater = None
            self._dispatcher = None
            self._logger.info('Bot Stopped')
        else:
            self._logger.warning('Bot is not Up yet')

    def _dispatcher_error_handler(self, update, context):
        self._logger.warning('Update "%s" caused error "%s"', update, context.error)

    def _delete_last_message(self):
        if self._last_message:
            self._last_message.delete()
            self._last_message = None
            self._logger.debug("Deleted last searching inline keyboard")

    # Callback responses
    @botutils.send_action(ChatAction.TYPING, True)
    def callback_start(self, update, context):
        self._logger.debug("Starting Spellbook bot")
        reply_keyboard = [('Nome', NAME), ('Livello', LEVEL), ('Classe', CHAR_CLASS), ('Classe e Livello', NAME_LEVEL)]
        update.message.reply_text(
            'Ricerca incantesimo per:',
            reply_markup=InlineKeyboardMarkup(menubuilder.build_tuple_menu(reply_keyboard, 2)))
        return MENU

    @botutils.send_action(ChatAction.TYPING, True)
    def callback_name_search(self, update, context):
        self._logger.debug("Search by name")
        query = update.callback_query
        query.edit_message_text('Ricerca incantesimo per:')

    @botutils.send_action(ChatAction.TYPING, True)
    def callback_class_search(self, update, context):
        self._logger.debug("Search by class")
        character_classes = (self.spellbook.get_classes())
        keyboard_classes = [(character_class.Nome, character_class.Nome) for character_class in character_classes]
        keyboard_columns = int(len(keyboard_classes)/2 + 0.5)

        query = update.callback_query
        bot = context.bot
        bot.send_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Seleziona la classe per cui cercare:',
            reply_markup=InlineKeyboardMarkup(menubuilder.build_tuple_menu(keyboard_classes, keyboard_columns)))

    @overwrite_last_message_decorator
    @botutils.send_action(ChatAction.TYPING, True)
    def callback_level_search(self, update, context):
        self._logger.debug("Search by level")
        keyboard_levels = [('Lv. 0', LEVELS[0]), ('Lv. 1', LEVELS[1]), ('Lv. 2', LEVELS[2]), ('Lv. 3', LEVELS[3]),
                           ('Lv. 4', LEVELS[4]),
                           ('Lv. 5', LEVELS[5]), ('Lv. 6', LEVELS[6]), ('Lv. 7', LEVELS[7]), ('Lv. 8', LEVELS[8]),
                           ('Lv. 9', LEVELS[9])]

        query = update.callback_query
        bot = context.bot
        self._last_message = bot.send_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Seleziona il livello per cui cercare:',
            reply_markup=InlineKeyboardMarkup(menubuilder.build_tuple_menu(keyboard_levels, 5)))
        return LEVEL

    @botutils.send_action(ChatAction.TYPING, True)
    def callback_class_level_search(self, update, context):
        self._logger.debug("Search by level name")
        query = update.callback_query
        query.edit_message_text('Ricerca incantesimo per classe e nome:')

    @botutils.send_action(ChatAction.TYPING, True)
    def callback_level_select(self, update, context):
        self._logger.debug("Level selected. Trying to retrieve data")
        query = update.callback_query
        spells = self.spellbook.get_spells_by_level(query.data)
        keyboard_spells = [('{} [Lvl. {}]'.format(spell.Nome, spell.Livello), spell.Nome) for spell in spells]
        bot = context.bot
        self._last_message = bot.send_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Ecco gli incantesimi della ricerca:",
            reply_markup=InlineKeyboardMarkup(menubuilder.build_tuple_menu(keyboard_spells, 1))
        )

    def callback_cancel(self, update, context):
        user = update.message.from_user
        self._logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Ciao! Spero di riverderti qui!',
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def main():
    try:
        spellbook_bot = SpellbookBot()
    except OSError as ex:
        sys.exit("Be sure that \"env.yaml\" file exists and you have read access to it!")
    updater = spellbook_bot.start()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()

    while True:
        user_input = input()
        if user_input == 'start':
            spellbook_bot.start()
        elif user_input == 'stop':
            spellbook_bot.stop()
        elif user_input == 'exit':
            spellbook_bot.stop()
            exit()
        else:
            print('Command not found')


if __name__ == '__main__':
    main()
