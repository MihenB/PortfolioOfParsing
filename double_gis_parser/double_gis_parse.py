from parse_package.multipurpose_parser import ScrapSession
from double_gis_parser.double_gis_config import url, cookies, headers, params


def get_data():
    session = ScrapSession()
    with open('double_gis.json', 'a', encoding='utf-8') as file:
        for page in range(1, 10):
            params.update(page=page)
            session.get(url=url,
                        cookies=cookies,
                        headers=headers,
                        params=params).json_to_file(file=file)


def main():
    get_data()


if __name__ == '__main__':
    main()
