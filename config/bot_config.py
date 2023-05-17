from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
# Получение токенов из файла .env
config = dotenv_values('./config/.env')
API_TOKEN = config['TG_BOT_TOKEN']
PINECONE_API_ENV = config['PINECONE_API_ENV']
PINECONE_API_KEY = config['PINECONE_API_KEY']
# Для бота 
API_KEY_CHATGPT = config['API_KEY_CHATGPT']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)