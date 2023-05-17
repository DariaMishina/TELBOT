from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config.bot_config import bot
from config.data_base import *
from keyboards import client_kb
from handlers import admin
from handlers.other_2 import chat_gpt, chat_gpt_category


def clear(user_id):
    db_update_time(user_id=user_id, time=None)
    db_update_ingredient(user_id=user_id, ingredient=None)
    db_update_dishes(user_id=user_id,dishes=None)
    db_update_category(user_id=user_id, category=None)
    
# Общие команды для меню
async def setup_bot_commands(dp: Dispatcher):
    bot_commands = [
        types.BotCommand(command="/start", description="Запустить бота")
    ]
    await bot.set_my_commands(bot_commands)
    
# Обработка команды /start
async def start_handler(message: types.Message):
    # admin.PROMPT_LIST = ['','','','']
    us_id = message.from_user.id
    
    clear(user_id=us_id)
    
    if not user_exists(user_id=us_id):
        db_table_val(user_id=us_id)
    db_update_prompt(user_id=us_id, prompt=admin.PROMPT)
    
    print(get_db_all_value(us_id))
    
    greet_kb = client_kb.start_kb()
    await message.answer(f'👋<b>Привет!</b>\n'
                         f'Я помогу вам быстро и удобно подобрать готовые блюда на основе ваших пожеланий.\n'
                         f'Выберите один из заготовленных запросов или напишите свой собственный запрос.', parse_mode='HTML',reply_markup=greet_kb)


async def process_callback(callback_query: types.CallbackQuery):
    # Обрабатыаем нажатие на кнопку
    if callback_query.data in ["button1", "button6", "button8"]:
        await bot.send_message(callback_query.message.chat.id, text='Выберите время приема пищи',reply_markup=client_kb.bld())
        # await admin.start_time('Задать время')
        print('Обработано нажатие на кнопку')
        
    elif callback_query.data in["button2", "button4", "button9"]:
        await bot.send_message(callback_query.message.chat.id, text='Введите ингридиент. Например: мясо, рыба или творог')
        await admin.start_ingredient('Задать ингредиент')
        print('Обработано нажатие на кнопку')
        
    elif callback_query.data in ["button3", "button5", "button7"]:
        await bot.send_message(callback_query.message.chat.id, text='Введите блюдо. Например: каша, вермишель или щи')
        await admin.start_dishes('Задать время')
        print('Обработано нажатие на кнопку')
    
    # Получить рекомендацию
    elif callback_query.data == "button0":
        print(admin.prompt_create(user_id=callback_query.message.chat.id))
        
        if get_db_value(callback_query.message.chat.id, column='category') == None:
            await bot.send_message(callback_query.message.chat.id, text=chat_gpt(admin.prompt_create(user_id=callback_query.message.chat.id)))
        else:
            temp_category = ' '.join(get_db_value(callback_query.message.chat.id, column='category').split()[2:])
            db_update_category(callback_query.message.chat.id, None)
            print('Запрос, который подается в бота: ',admin.prompt_create(user_id=callback_query.message.chat.id))
            await bot.send_message(callback_query.message.chat.id, text=chat_gpt_category(admin.prompt_create(user_id=callback_query.message.chat.id), temp_category))
            print('Запуск бота с категорией', temp_category)
            
        await bot.send_message(callback_query.message.chat.id, text=f'Хотите что-нибудь ещё?', reply_markup=client_kb.start_kb())
        clear(user_id=callback_query.message.chat.id)
        print('Пользователь получил рекомендацию')
        
    # Сбросить рекомендации
    elif callback_query.data == "button10":
        clear(user_id=callback_query.message.chat.id)
        await bot.send_message(callback_query.message.chat.id, text='Список ваших предпочтений сброшен. Хотите выбрать что-нибудь другое?'\
            ,reply_markup=client_kb.start_kb())
        print('Обработано нажатие на кнопку')
        
    # Выбрать категорию
    elif callback_query.data == "button11":
        await bot.send_message(callback_query.message.chat.id, text='Выберите категорию'\
            ,reply_markup=client_kb.category())
        await admin.start_category('Задать категорию')
        print('Обработано нажатие на кнопку')
    
    # Выбор времени завтрак\обед\ужин
    elif callback_query.data == "breakfast":
        db_update_time(user_id=callback_query.message.chat.id, time=' на завтрак')
        await bot.send_message(callback_query.message.chat.id, text=f'Отлично! Время задано\n'
                         f"Время: <i>Завтрак</i>\n"
                         f"<b>Ваш текущий запрос:</b> <i>{admin.prompt_create('user', user_id=callback_query.message.chat.id)}</i>"\
            ,reply_markup=client_kb.check_time(callback_query.message.chat.id), parse_mode='HTML')
       
        print('Обработано нажатие на кнопку')

    elif callback_query.data == "lunch":
        db_update_time(user_id=callback_query.message.chat.id, time=' на обед')
        await bot.send_message(callback_query.message.chat.id, text=f'Отлично! Время задано\n'
                         f"Время: <i>Обед</i>\n"
                         f"<b>Ваш текущий запрос:</b> <i>{admin.prompt_create('user',user_id=callback_query.message.chat.id)}</i>"\
            ,reply_markup=client_kb.check_time(callback_query.message.chat.id), parse_mode='HTML')
       
        print('Обработано нажатие на кнопку')

    elif callback_query.data == "dinner":
        db_update_time(user_id=callback_query.message.chat.id, time=' на ужин')
        await bot.send_message(callback_query.message.chat.id, text=f'Отлично! Время задано\n'
                         f"Время: <i>Ужин</i>\n"
                         f"<b>Ваш текущий запрос:</b> <i>{admin.prompt_create('user',user_id=callback_query.message.chat.id)}</i>"\
            ,reply_markup=client_kb.check_time(callback_query.message.chat.id), parse_mode='HTML')
        
        print('Обработано нажатие на кнопку')   
    

 

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_callback_query_handler(process_callback)
