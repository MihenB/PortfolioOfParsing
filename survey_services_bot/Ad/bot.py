from aiogram import Bot, Dispatcher, executor, types
from config import token
from kb import Keyboards
from db_control import DBControl
from state import CurrentCondition


class AvitoBot:
    # Vars for any session
    bot = Bot(token=token)
    dp = Dispatcher(bot)
    greetings = 'Привет! Я бот для проведения опросов. ' \
                'Я буду предлагать список услуг, разделенный по группам. В каждой группе имеется набор подгрупп - ' \
                'узких компетенций.\n' \
                'Твоя задача состоит в том, чтобы выбрать, ' \
                'входит ли услуга в список твоих умений и навыков, или нет.\n' \
                'Выбор осуществляется нажатием клавиши "Да" или "Нет" соответственно. ' \
                'После каждого выбора будет отправлено сообщение с информацией о нажатой кнопке.\n' \
                'Все ответы будут сохранены в базу данных анонимно.'
    # Vars which MUST be in local session
    current_condition = CurrentCondition()
    db_control = DBControl()

    @staticmethod
    @dp.message_handler(commands='start')
    async def start(message: types.Message):
        # Introducing to bot features
        await message.answer(AvitoBot.greetings)
        await message.answer('Начнем?', reply_markup=Keyboards.start_keyboard.get_configured_keyboard())

    @staticmethod
    @dp.callback_query_handler(lambda x: x.data == 'Начнем!')
    async def start_button(callback_query: types.CallbackQuery):
        # Make connection
        AvitoBot.db_control.create_connection()

        # Clean past records (FULLY)
        AvitoBot.db_control.clean_up_table(table_name='AvitoServices.service_groups')
        AvitoBot.db_control.clean_up_table(table_name='AvitoServices.services')

        # Generate data about the first record in the table
        AvitoBot.current_condition.next_stream_elem()
        current_value, is_header = AvitoBot.current_condition.get_cur_val_and_head_mark()

        # Send generated message (with a keyboard) depends on type of the current_value
        if is_header:
            await AvitoBot.bot.send_message(
                callback_query.from_user.id,
                f'Переходим к группе "{AvitoBot.current_condition.get_cur_header()}"',
                reply_markup=Keyboards.header_keyboard.get_configured_keyboard()
            )
        else:
            await AvitoBot.bot.send_message(
                callback_query.from_user.id,
                current_value,
                reply_markup=Keyboards.keyboard.get_configured_keyboard()
            )

    @staticmethod
    @dp.callback_query_handler(lambda x: x.data == 'Да')
    async def yes_button(callback_query: types.CallbackQuery):
        # User pressed Yes button which means current statement is going to DB
        AvitoBot.db_control.send_data_to_db(
            AvitoBot.current_condition.get_cur_val(),
            AvitoBot.current_condition.get_cur_header()
        )
        # Notification. Maybe it will be removed in the future (?)
        await AvitoBot.bot.send_message(callback_query.from_user.id, 'Нажата кнопка "Да", ответ записан')
        # Generate and print the next statement as a message
        await AvitoBot.create_new_message(callback_query)

    @staticmethod
    @dp.callback_query_handler(lambda x: x.data == 'Нет')
    async def no_button(callback_query: types.CallbackQuery):
        # User pressed No button which means current statement is just skipping
        # Notification. Maybe it will be removed in the future (?)
        await AvitoBot.bot.send_message(callback_query.from_user.id, 'Нажата кнопка "Нет", запись пропущена')
        # Generate and print the next statement as a message
        await AvitoBot.create_new_message(callback_query)

    @staticmethod
    async def create_new_message(callback_query: types.CallbackQuery):
        AvitoBot.current_condition.next_stream_elem()
        current_value, is_header = AvitoBot.current_condition.get_cur_val_and_head_mark()
        if current_value:
            if is_header:
                await AvitoBot.bot.send_message(callback_query.from_user.id,
                                                f'Переходим к группе "{AvitoBot.current_condition.get_cur_header()}"',
                                                reply_markup=Keyboards.header_keyboard.get_configured_keyboard())
            else:
                await AvitoBot.bot.send_message(callback_query.from_user.id,
                                                current_value,
                                                reply_markup=Keyboards.keyboard.get_configured_keyboard())
        else:
            await AvitoBot.bot.send_message(
                callback_query.from_user.id,
                'Опрос окончен, результаты записаны. Спасибо за участие!\n'
                'Чтобы пройти опрос повторно, нужно снова ввести команду /start.\n'
                'ВНИМАНИЕ! ПРИ ПОВТОРНОМ ЗАПУСКЕ ОПРОСА ВСЕ ДАННЫЕ БУДУТ ОЧИЩЕНЫ И ПЕРЕЗАПИСАНЫ!'
            )
            AvitoBot.db_control.commit_and_close_connection()

    @classmethod
    def start_polling(cls):
        executor.start_polling(cls.dp)


def main():
    AvitoBot.start_polling()


if __name__ == '__main__':
    main()
