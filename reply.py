from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def contact_share_button():
    btn = KeyboardButton(text="Share contact ☎", request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True)


def main_menu_buttons():
    btn1 = KeyboardButton(text="New 📝")
    btn2 = KeyboardButton(text="My tasks 📋")
    btn3 = KeyboardButton(text="Info")
    design = [
        [btn1, btn2],
        [btn3]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)


def task_list_buttons():
    btn1 = KeyboardButton(text="Delete task")
    btn2 = KeyboardButton(text="🔙 Back")
    design = [
        [btn1],
        [btn2]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
