from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from config.bot_config import dp
from keyboards import client_kb
from config.data_base import *
import re


PROMPT = f'Посоветуй нескольно блюд'
PROMPT_LIST = ['time','ingredient','dishes','category'] # время, ингредиент, блюдо, категория

def regular_check_ingredient(msg, user_id):
    # matches_meat = re.findall(r"\b[Мм]яс\w*\b",string)
    if re.findall(r"\b[Мм]яс\w*\b",msg) != [] and len(msg.split()) == 1:
        temp = 'мяса(курица, говядина, свинина, индейка, баранина)'
        db_update_ingredient(user_id=user_id, ingredient=f' из {temp}')
        print('Замечено мясо')
    # matches_fish = re.findall(r"\b[Рр]ыб\w*\b",string)
    elif re.findall(r"\b[Рр]ыб\w*\b",msg) != [] and len(msg.split()) == 1:
        temp = 'рыбы(лосось, сёмга, тунец, угорь)'
        db_update_ingredient(user_id=user_id, ingredient=f' из {temp}')
        print('Замечена рыба')
    else: 
        db_update_ingredient(user_id=user_id, ingredient=f' из {msg}')
        print('Замечен ингридиент')
        
def regular_check_dishes(msg, user_id):
    if re.findall(r"\b[Кк]аш\w*\b", msg) != [] and len(msg.split()) == 1:
        temp = 'каша(гречка, рис, плов, булгур)'
        db_update_dishes(user_id=user_id, dishes=f' похожее на {temp}')
    elif re.findall(r"\b[Вв][еи]рми\w*\b",msg) != [] and len(msg.split()) == 1:
        temp = 'вермишель(паста, макароны, вермишель)'
        db_update_dishes(user_id=user_id, dishes=f' похожее на {temp}')  
    elif re.findall(r"\b[Щщ]и\w*\b",msg) != [] and len(msg.split()) == 1:
        temp = 'щи(суп, борщ)'
        db_update_dishes(user_id=user_id, dishes=f' похожее на {temp}')  
    else:
        db_update_dishes(user_id=user_id, dishes=f' похожее на {msg}')
        
        
def prompt_create(status=None, user_id=None):
    if status is None:
        NEW_PROMPT = ''
        for el in get_db_all_value(user_id=user_id):
            if el != None:
                NEW_PROMPT += el
        return NEW_PROMPT + ', выведи название и ссылку нумерованным списком. В выводе должны быть только названия рекомендованных блюд без лишенго текста'
    else:
        NEW_PROMPT = 'Посоветуй что-нибудь'
        for el in get_db_all_value(user_id=user_id)[1:]:
            if el != None:
                NEW_PROMPT += el
        return NEW_PROMPT
        

class FSMAdmin(StatesGroup):
    # time = State()
    ingredient = State()
    dishes = State()
    category = State()

# time
# async def start_time(message: types.Message):
#     await FSMAdmin.time.set()

# async def set_time(message: types.Message, state:FSMContext):
#     inline_keyboard_markup = client_kb.check_time()
#     await state.update_data(time=message.text)
#     PROMPT_LIST[0] = f' на {message.text}'
#     data = await state.get_data()
#     await message.answer(f'Отлично! Время задано\n'
#                          f"Время: <i>{data['time']}</i>\n"
#                          f"<b>Ваш текущий запрос:</b> <i>{prompt_create('user')}</i>", 
#                          reply_markup=inline_keyboard_markup, parse_mode='HTML')
#     await state.finish()
    
# ingredient
async def start_ingredient(message: types.Message):
    await FSMAdmin.ingredient.set()
    

async def set_ingredient(message: types.Message, state:FSMContext):
    inline_keyboard_markup = client_kb.check_ingredient(message.from_user.id)        
    await state.update_data(ingredient=message.text)
    regular_check_ingredient(message.text, message.from_user.id)
    # PROMPT_LIST[1] = f' из {message.text}'
    data = await state.get_data()
    await message.answer(f'Отлично! Ингредиент задан\n'
                         f"Игредиент: <i>{data['ingredient']}</i>\n"
                         f"<b>Ваш текущий запрос:</b> <i>{prompt_create('user', user_id=message.from_user.id)}</i>", 
                         reply_markup=inline_keyboard_markup, parse_mode='HTML')
    await state.finish()
    
# dishes
async def start_dishes(message: types.Message):
    await FSMAdmin.dishes.set()
    

async def set_dishes(message: types.Message, state:FSMContext):
    inline_keyboard_markup = client_kb.check_dishes(message.from_user.id)
    await state.update_data(dishes=message.text)
    regular_check_dishes(message.text, message.from_user.id)
    data = await state.get_data()
    await message.answer(f'Отлично! Блюдо задано\n'
                         f"Блюдо: <i>{data['dishes']}</i>\n"
                         f"<b>Ваш текущий запрос:</b> <i>{prompt_create('user',user_id=message.from_user.id)}</i>", 
                         reply_markup=inline_keyboard_markup, parse_mode='HTML')
    await state.finish()
    print(prompt_create(user_id=message.from_user.id))

#category
async def start_category(message: types.Message):
    await FSMAdmin.category.set()
    

async def set_category(message: types.Message, state:FSMContext):
    inline_keyboard_markup = client_kb.all_variation(message.from_user.id)
    await state.update_data(category=message.text)
    
    db_update_category(user_id=message.from_user.id, category=f' из категории {message.text}')
    
    data = await state.get_data()
    await message.answer(f'Отлично! Категория задана\n'
                         f"Блюдо: <i>{data['category']}</i>", 
                         reply_markup= types.ReplyKeyboardRemove(), parse_mode='HTML')
    await message.answer(f"<b>Ваш текущий запрос:</b> <i>{prompt_create('user', user_id=message.from_user.id)}</i>", 
                         reply_markup=inline_keyboard_markup, parse_mode='HTML')

    await state.finish()
    print(prompt_create(user_id=message.from_user.id))



def register_handler(dp: Dispatcher):
    # dp.register_message_handler(start_time, lambda msg: msg.text == 'Задать время', state=None)
    # dp.register_message_handler(set_time, state=FSMAdmin.time)
    dp.register_message_handler(start_ingredient, lambda msg: msg.text == 'Задать ингредиент', state=None)
    dp.register_message_handler(set_ingredient, state=FSMAdmin.ingredient)
    dp.register_message_handler(start_dishes, lambda msg: msg.text == 'Задать время', state=None)
    dp.register_message_handler(set_dishes, state=FSMAdmin.dishes)
    dp.register_message_handler(start_category, lambda msg: msg.text == 'Задать категорию', state=None)
    dp.register_message_handler(set_category, state=FSMAdmin.category)