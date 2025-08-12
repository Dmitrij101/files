from aiogram import Bot, Dispatcher
from aiogram.types import PreCheckoutQuery, Message
import requests

bot = Bot("YOUR_BOT_TOKEN")
dp = Dispatcher(bot)

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout(pre: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre.id, ok=True)

@dp.message_handler(content_types="successful_payment")
async def success_pay(msg: Message):
    await msg.answer("✅ Оплата прошла! Жми 'Крутить' в приложении.")

# Запуск polling
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)