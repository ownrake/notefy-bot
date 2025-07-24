import asyncio
import logging
import tomllib

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

logging.basicConfig(level = logging.INFO)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

bot = Bot(config["settings"]["api_token"])
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(config["messages"]["start"],
                         parse_mode=ParseMode.MARKDOWN)


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(config["messages"]["help"])


@dp.message(Command("new"))
async def test(message: Message):
    text = message.text

    parts = text.split("—")[1:]

    data = {}
    for part in parts:
        key_value = part.strip().split(maxsplit=1)
        if len(key_value) == 2:
            key, value = key_value
            data[key] = value

    note = ""

    if "title" in data:
        note += f"<b>{data["title"]}</b>\n\n"

    if "text" in data:
        note += f"<blockquote>{data["text"]}</blockquote>"

    if "link" in data:
        pass

    # await message.answer(note, parse_mode=ParseMode.HTML)
    await bot.send_message(chat_id=config["settings"]["chanell_id"], text=note,
                           parse_mode=ParseMode.HTML)

@dp.message(Command("test"))
async def test(message: Message):
    await message.answer("<blockquote>bold_text cursive</blockquote>",
                         parse_mode=ParseMode.HTML)


@dp.message()
async def clog(message: Message):
    # await message.answer(config["messages"]["clog"])

    text = message.text
    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass