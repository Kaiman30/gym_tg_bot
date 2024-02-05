import asyncio
from DB import database as db

from aiogram import Router, Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode


# выборка токена бота
with open('token.txt', 'r') as file:
    TOKEN = file.read()
    
bot = Bot(token=TOKEN.strip(), parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message) -> None:
    """Команда /start"""
    #await db.cmd_db_start(message.from_user.id, message.from_user.full_name)
    await message.answer(f'Привет! \n<b>Я</b> - бот помощник для тренировок\n'
                         f'Чтобы получше узнать мой функционал, пиши "/help"')


@dp.message(Command("help"))
async def help(message: Message) -> None:
    """Команда /help"""
    await message.answer(f'Список команд:\n\n'
                         f'<b>/w Упражнение Вес (целое число или число с точкой)</b> - Добавить упражнение\n'
                         f'<b>/l - Список добавленных упражнений</b>\n'
                         f'<b>/cw Упражнение - Текущий вес на выбранное упражнение</b>')


@dp.message(Command("w"))
async def weight(message: Message, command: CommandObject):
    """Команда /w (weight)"""
    data = command.args.capitalize()
    if data:
        data = data.split()
        exercise = data[:-1] # [1, 2, 3]
        exercise = ' '.join(exercise)
        weight = data[-1]

        await db.add_weight(message.from_user.id, message.from_user.full_name, exercise, weight)
        await message.answer(f'Упражнение: <b>{exercise}</b>\n'
                             f'Вес: <b>{weight}</b>')
    else:
        await message.answer('❌ Упражнение и вес не указаны')


@dp.message(Command("l"))
async def list_(message: Message):
    """Команда /l (Список записанных упражнений)"""
    ex_list = await db.list_exes(message.from_user.id)
    if ex_list:
        output = '🔢<b>Список записанных упражнений:</b>\n\n' + '\n'.join(ex_list)
        await message.answer(output)
    else:
        await message.answer('❌ Список записанных упражнений пуст')


@dp.message(Command("cw"))
async def current_weight(message: Message, command: CommandObject):
    """Команда /cw (Текущие веса)"""
    exes = command.args.capitalize()
    current_weight = await db.current_weight(message.from_user.id, exes)
    if current_weight:
        await message.answer(f'Текущие вес на упражнение "{exes}": <b>{current_weight[0]}</b>')
    else:
        await message.answer('❌ Упражнение не найдено')


async def main() -> None:
    """Запуск бота"""
    await db.db_start()
    
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
