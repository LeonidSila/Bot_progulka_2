from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from create_bot import dp, bot
from aiogram.utils.keyboard import ReplyKeyboardBuilder


kb_vibor_work = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text ='Заполнить таблицу'), types.KeyboardButton(text ='Карточка товара'), types.KeyboardButton(text ='Отдыхать')]
    , [types.KeyboardButton(text ='Сколько скинули')]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Надо выбрать кнопки',
    selective=True

)

kb_vibor_work_1 = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text ='Устала/Выйти')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Надо выбрать кнопку если, устали',
    selective=True

)

kb_vibor_admin = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text ='Должники'), types.KeyboardButton(text ='Данные/перевел'), types.KeyboardButton(text ='Выйти'), types.KeyboardButton(text ='Данные/должен')]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Надо выбрать кнопки',
    selective=True

)