from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os
from aiogram.utils.markdown import hbold, hlink
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from freelance_exchange_parser_bot.config import token
from freelance_exchange_parser_bot.parsers.bring_data_together.bring_data_together_async import AllData
import asyncio

bot = Bot(token=token)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()
all_parsers = AllData()

start_buttons = [
    'Создать csv-документ с заказами за 24 часа',
    'Проверить наличие заказов за час'
]


def main():
    scheduler.start()
    executor.start_polling(dp)


@dp.message_handler(commands='start')
async def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.chat.id, f'Каждый час бот автоматически собирает информацию об '
                                            'актуальных заказах с трех  '
                                            'наиболее популярных онлайн-бирж и высылает их в виде карточек со всей '
                                            'информацией о заказе, а '
                                            'также ссылкой на источник.')

    await message.answer(
        'Загрузить csv-файл с абсолютно всеми данными с сайтов бирж можно через выпадающее меню'
    )
    await message.answer(
        f'{hbold("Пожалуйста, дождитесь сообщения о загрузке всех данных, прежде чем пользоваться ботом")}',
        parse_mode=types.ParseMode.HTML
    )

    try:
        await spam_message_with_cards(dp, message, True)
        await message.answer(
            'Первичная загрузка данных завершена, весь функционал доступен',
            reply_markup=keyboard
        )
    except Exception as ex:
        message.answer('Произошла ошибка на сервере. Повторите попытку позже.\n'
                       f'При повторном подключении нужно будет снова ввести команду {hbold("/start")}',
                       parse_mode=types.ParseMode.HTML)
        print(f'[ERROR] {ex}')
    finally:
        scheduler.add_job(spam_message_with_cards, 'interval', seconds=3590, args=(dp, message))


async def spam_message_with_cards(dp_, message, update_only=False):
    if update_only:
        await all_parsers.parse_cards_to_message(True)
        return
    cards = []
    items = await all_parsers.parse_cards_to_message()
    # await asyncio.sleep(2)
    for item in items:
        card = f'{hlink(item["title"], item["link"])}\n\n' \
               f'{hbold("Безопасная сделка: ")}{item["safe_deal"]}\n\n' \
               f'{hbold("Цена: ")}{item["price"]}\n\n' \
               f'{hbold("Дата и время: ")}\n{item["date_and_time"]}\n\n' \
               f'{hbold("Описание")}\n\n{item["description"]}'
        cards.append(card)
    print(f'[INFO] Всего карточек обработано: {len(cards)}')
    if not cards:
        await message.answer('Похоже, за последний час новых заказов не было')
    else:
        for card in cards:
            await asyncio.sleep(1)
            await dp_.bot.send_message(chat_id=message.chat.id, text=card, parse_mode=types.ParseMode.HTML)


async def send_waiting_message(message):
    await dp.bot.send_message(chat_id=message.chat.id, text='Ожидайте...')


async def send_file(message):
    file = await all_parsers.parse_cards_to_file()
    await bot.send_document(chat_id=message.chat.id, document=open(file, 'rb'))
    await os.remove(file)


@dp.message_handler(Text(equals=start_buttons[0]))
async def caught_message_to_send_day_file(message):
    await send_waiting_message(message)
    try:
        await send_file(message)
    except Exception as ex:
        print(f'[ERROR] {ex}')
        await message.answer('Произошла ошибка, повторите попытку позднее')


@dp.message_handler(Text(equals=start_buttons[1]))
async def caught_message_to_send_hour_cards(message):
    await send_waiting_message(message)
    try:
        await spam_message_with_cards(dp, message)
    except Exception as ex:
        print(f'[ERROR] {ex}')
        await message.answer('Произошла ошибка, повторите попытку позднее')


if __name__ == '__main__':
    main()
