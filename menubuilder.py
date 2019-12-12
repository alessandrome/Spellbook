from telegram import InlineKeyboardButton


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    """
    Build button for keyboard responses.
    :param buttons:
    :param n_cols:
    :param header_buttons: Optional.
    :param footer_buttons: Optional.
    :return:
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def build_tuple_menu(tuple_list, n_cols, header_buttons=None, footer_buttons=None):
    button_list = [InlineKeyboardButton(s[0], callback_data=str(s[1])) for s in tuple_list]
    return build_menu(button_list, n_cols, header_buttons, footer_buttons)


def get_main_menu():
    pass
