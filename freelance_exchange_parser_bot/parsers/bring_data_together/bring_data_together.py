from freelance_exchange_parser_bot.parsers.habr.habr_parser_OOP import HabrParser
from freelance_exchange_parser_bot.parsers.kwork.kwork_parser_OOP import KWorkParser
from freelance_exchange_parser_bot.parsers.fl.fl_parser_OOP import FlParser


class AllData:
    def __init__(self):
        from datetime import datetime

        self.cur_time = datetime.now().strftime('%d_%m_%Y %H_%M_%S')

        self.kwork_parser = KWorkParser()
        self.habr_parser = HabrParser()
        self.fl_parser = FlParser()

    def update_time(self):
        from datetime import datetime
        self.cur_time = datetime.now().strftime('%d_%m_%Y %H_%M_%S')

    def parse_cards_to_message(self, update_only=False):
        result_list = []
        if update_only:
            self.habr_parser.parse_card_to_message(update_only)
            self.kwork_parser.parse_card_to_message(update_only)
            self.fl_parser.parse_card_to_message(update_only)
            return
        result_list.extend(self.habr_parser.parse_card_to_message(update_only))
        result_list.extend(self.kwork_parser.parse_card_to_message(update_only))
        result_list.extend(self.fl_parser.parse_card_to_message(update_only))
        return result_list

    async def parse_cards_to_file(self):
        await self.create_general_coroutine_with_files()
        return f'{self.cur_time}.csv'

    async def create_general_coroutine_with_files(self):
        from aiocsv import AsyncWriter
        import aiofiles

        self.update_time()
        async with aiofiles.open(f'{self.cur_time}.csv',
                                 'w',
                                 newline='',
                                 encoding='utf-8') as file:
            writer = AsyncWriter(file)

            await writer.writerow(
                [
                    'Название',
                    'Ссылка',
                    'Безопасная сделка',
                    'Цена',
                    'Дата и время размещения',
                    'Описание'
                ]
            )

            general_data = [*self.kwork_parser.get_file_data(),
                            *self.habr_parser.get_file_data(),
                            *self.fl_parser.get_file_data()]

            for item in general_data:
                await writer.writerow(
                    [
                        item['title'],
                        item['link'],
                        item['safe_deal'],
                        item['price'],
                        item['date_and_time'],
                        item['description']
                    ]
                )
            print(f'[INFO] File {self.cur_time}.csv successfully written!')


async def main():
    parsers = AllData()
    print(parsers.parse_cards_to_message(True))
    print(parsers.parse_cards_to_message())
    print(await parsers.parse_cards_to_file())


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
