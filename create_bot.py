import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage=storage)
