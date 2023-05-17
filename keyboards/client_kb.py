from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from handlers import admin
from config.data_base import *


def start_kb():
    button1 = InlineKeyboardButton(
        text='Посоветуй что-нибудь на...(завтрак, обед, ужин)', callback_data='button1')
    button2 = InlineKeyboardButton(
        text='Посоветуй что-нибудь из...(ингредиент)', callback_data='button2')
    button3 = InlineKeyboardButton(
        text='Посоветуй что-нибудь, похожее на...(название блюда)', callback_data='button3')
    button4 = InlineKeyboardButton(
        text='Выбрать категорию блюд', callback_data='button11')

    greet_kb = InlineKeyboardMarkup().add(button1).add(button2).add(button3).add(button4)

    return greet_kb


def check_time(user_id):
    text_ing = 'Указать ингредиент'
    text_dish = 'Указать блюдо, похожее на то, что я ищу'
    text_cat = 'Выбрать категорию блюд'

    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[1]) != None:
        text_ing = 'Изменить ингредиент'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[2]) != None:
        text_dish = 'Изменить похожее блюдо'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[3]) != None:
        text_cat = 'Изменить категорию блюд'
        
    button1 = InlineKeyboardButton(
        text=text_ing, callback_data="button4")
    button2 = InlineKeyboardButton(
        text=text_dish, callback_data="button5")
    button3 = InlineKeyboardButton(
        text='Получить рекомендацию', callback_data="button0")
    button4 = InlineKeyboardButton(
        text='Сбросить предпочтения', callback_data="button10")
    button5= InlineKeyboardButton(
        text=text_cat, callback_data='button11')
    
    inline_keyboard_markup = InlineKeyboardMarkup()\
        .add(button1).add(button2).add(button5).add(button3).add(button4)
    return inline_keyboard_markup


def check_ingredient(user_id):
    text_time = 'Указать назначение'
    text_dish = 'Указать блюдо, похожее на то, что я ищу'
    text_cat = 'Выбрать категорию блюд'

    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[0]) != None:
        text_time = 'Изменить назначение'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[2]) != None:
        text_dish = 'Изменить похожее блюдо'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[3]) != None:
        text_cat = 'Изменить категорию блюд'
        
    button1 = InlineKeyboardButton(
        text=text_time, callback_data="button6")
    button2 = InlineKeyboardButton(
        text=text_dish, callback_data="button7")
    button3 = InlineKeyboardButton(
        text='Получить рекомендацию', callback_data="button0")
    button4 = InlineKeyboardButton(
        text='Сбросить предпочтения', callback_data="button10")
    button5= InlineKeyboardButton(
        text=text_cat, callback_data='button11')
    
    inline_keyboard_markup = InlineKeyboardMarkup()\
        .add(button1).add(button2).add(button5).add(button3).add(button4)
    return inline_keyboard_markup


def check_dishes(user_id):
    text_time = 'Указать назначение'
    text_ing = 'Указать ингредиент'
    text_cat = 'Выбрать категорию блюд'

    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[0]) != None:
        text_time = 'Изменить назначение'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[1]) != None:
        text_ing = 'Изменить ингредиент'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[3]) != None:
        text_cat = 'Изменить категорию блюд'
        
    button1 = InlineKeyboardButton(
        text=text_time, callback_data="button8")
    button2 = InlineKeyboardButton(
        text=text_ing, callback_data="button9")
    button3 = InlineKeyboardButton(
        text='Получить рекомендацию', callback_data="button0")
    button4 = InlineKeyboardButton(
        text='Сбросить предпочтения', callback_data="button10")
    button5= InlineKeyboardButton(
        text=text_cat, callback_data='button11')
    
    inline_keyboard_markup = InlineKeyboardMarkup()\
        .add(button1).add(button2).add(button5).add(button3).add(button4)
    return inline_keyboard_markup

def category():
    button1 = KeyboardButton('Веганское меню')
    button2 = KeyboardButton('Доступно каждому: лучшие цены')
    button3 = KeyboardButton('Доступно только онлайн')
    button4 = KeyboardButton('Здоровое питание')
    button5 = KeyboardButton('Курица-грилль')
    button6 = KeyboardButton('Мало калорий')
    button7 = KeyboardButton('На дачу и пикник')
    button8 = KeyboardButton('Новинки')
    button9 = KeyboardButton('Роллы')
    button10 = KeyboardButton('Много белка')
    button11 = KeyboardButton('Салаты и закуски')
    button12 = KeyboardButton('Семейный формат')
    button13 = KeyboardButton('Супы')


    greet_kb = ReplyKeyboardMarkup(row_width=3,
        resize_keyboard=True, one_time_keyboard=True
    ).add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12, button13)
    return greet_kb

# После выбора категории блюд
def all_variation(user_id):
    text_time = 'Указать назначение'
    text_ing = 'Указать ингредиент'
    text_dish = 'Указать блюдо, похожее на то, что я ищу'
    
    
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[0]) != None:
        text_time = 'Изменить назначение'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[1]) != None:
        text_ing = 'Изменить ингредиент'
    if get_db_value(user_id=user_id, column=admin.PROMPT_LIST[2]) != None:
        text_dish = 'Изменить похожее блюдо'
    
    button0 = InlineKeyboardButton(
        text=text_time, callback_data="button8") 
    button1 = InlineKeyboardButton(
        text=text_ing, callback_data="button9")
    button2 = InlineKeyboardButton(
        text=text_dish, callback_data="button7")
    button3 = InlineKeyboardButton(
        text='Получить рекомендацию', callback_data="button0")
    button4 = InlineKeyboardButton(
        text='Сбросить предпочтения', callback_data="button10")
    button5= InlineKeyboardButton(
        text='Изменить категорию блюд', callback_data='button11')
    
    inline_keyboard_markup = InlineKeyboardMarkup()\
        .add(button0).add(button1).add(button2).add(button3).add(button4).add(button5)
    return inline_keyboard_markup
    
# завтрак обед ужин
def bld():
    button1 = InlineKeyboardButton(
        text='Завтрак', callback_data="breakfast") 
    button2 = InlineKeyboardButton(
        text='Обед', callback_data="lunch")
    button3 = InlineKeyboardButton(
        text='Ужин', callback_data="dinner")
    inline_keyboard_markup = InlineKeyboardMarkup()\
        .row(button1, button2,button3)
    return inline_keyboard_markup
    
