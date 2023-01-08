import logging
from aiogram.utils import executor

from create_bot import dp  # bot
from handlers import client_part, admin_part
from db import work_with_db


async def on_startup(_):
    print('bot is online')
    # настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        filename='main.log',
        filemode='w',
        format=('%(asctime)s, %(levelname)s, %(name)s, %(message)s,' +
                '%(funcName)s, %(lineno)d')
    )
    # await bot.set_webhook('https://greytres.sytes.net')
    work_with_db.start_db()

admin_part.register_handlers_admin(dp)
client_part.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


# executor.start_webhook(
#     dp, webhook_path='/', skip_updates=True, on_startup=on_startup,
#     host='localhost', port=5001
# )
