import enum
from aiogram import types
from aiogram.types import KeyboardButton


class Keyboards(enum.Enum):
    start_keyboard = (1, ['Начнем!'])
    header_keyboard = (2, ['Да'])
    keyboard = (3, ['Да', 'Нет'])

    def __init__(self, num, start_buttons):
        self.num = num
        self.start_buttons = [KeyboardButton(text=text, callback_data=text) for text in start_buttons]
        self.keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        self.keyboard.add(*self.start_buttons)

    def get_configured_keyboard(self) -> types.InlineKeyboardMarkup:
        return self.keyboard
