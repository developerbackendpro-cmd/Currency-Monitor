import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode

API_TOKEN = "8023296312:AAFZvasvkaPKwvmfkPHXf5Q7AmoDaJLSvNg"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет !\nВведите код валюты: USD, EUR, RUB ...")

@dp.message_handler()
async def handle_message(message: types.Message):
    code = message.text.upper()
    try:
        response = requests.get("https://cbu.uz/ru/arkhiv-kursov-valyut/json/")
        data = response.json()
        found = None
        for item in data:
            if item['Ccy'] == code:
                found = item
                break
        if not found:
            await message.reply("Валюта не найдена.")
            return
        text = (f"{found['CcyNm_RU']} ({code})\nКурс: ( 1 - {code} ) => {found['Rate']} сум\nДата: {found['Date']}")
        await message.reply(text, parse_mode=ParseMode.MARKDOWN)
    except:
        await message.reply("Произошла ошибка при получении данных")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
