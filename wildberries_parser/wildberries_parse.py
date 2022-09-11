from parse_package.multipurpose_parser import ScrapSession
from wildberries_parser.config4 import url, headers, params


def get_data():
    session = ScrapSession()
    with open('wildberries_data.json', 'w', encoding='utf-8') as file:
        session.get(
            url=url,
            headers=headers,
            # secured=True,
            # proxies=True,
            params=params
        ).json_to_file(file=file)


def main():
    get_data()


if __name__ == '__main__':
    main()
