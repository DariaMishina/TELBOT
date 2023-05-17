from aiogram import executor
from config.bot_config import dp
from handlers import other, client, admin, other_2

admin.register_handler(dp)
client.register_handler_client(dp)
# other.register_handler(dp)
other_2.register_handler_other(dp)


if __name__ == '__main__':
    print('Bot ready!')
    executor.start_polling(dp, skip_updates=True, on_startup=client.setup_bot_commands)