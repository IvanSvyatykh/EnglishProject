import os

from aiogram import F, Bot
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from config import text
from model.Convertor import Convertor

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message) -> None:
    await msg.answer(text=text.START_PHRASE)


@router.message(F.photo)
async def load_photo_hander(msg: Message, bot: Bot) -> None:
    path = f'./downloads/{msg.from_user.id}.jpg'
    await msg.bot.download(file=msg.photo[-1].file_id, destination=path)
    convertor = Convertor(path)

    flag = convertor.to_csv()
    if (flag):
        await bot.send_document(msg.chat.id,
                                caption="Внимание бот смог разобрать фото не полностью! Колонки, где не хватает элементов содержат 0 в конце. Внимательно проверьте колонки на пропущенные запятые!",
                                document=FSInputFile(
                                    path=path.replace('.jpg', '.csv')))
    else:
        await bot.send_document(msg.chat.id,
                                caption="Внимательно проверьте колонки на пропущенные запятые!",
                                document=FSInputFile(
                                    path=path.replace('.jpg', '.csv')))
    convertor.remove_file()
