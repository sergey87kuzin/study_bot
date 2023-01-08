import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

from dotenv import load_dotenv

load_dotenv()
# storage = RedisStorage2(host='0.0.0.0', port=6379, db=1)
storage = MemoryStorage()

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage=storage)
