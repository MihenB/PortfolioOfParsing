import OzonParser.OzonParser
import DromParser.DromParser
import json


def write_to_json(data):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open('result_data.json', 'w') as file:
        file.write(json_data)


def main():
    data_ozon = OzonParser.OzonParser.get_info_cards('1520800Q0F')
    data_drom = DromParser.DromParser.get_info_cards('1660063G20')
    data = data_drom + data_ozon
    write_to_json(data)


if __name__ == '__main__':
    main()