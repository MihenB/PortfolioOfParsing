headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
}

params = {
    'appType': '1',
    'couponsGeo': '12,7,3,6,5,18,21',
    'curr': 'rub',
    'dest': '-1216601,-337422,-1114902,-1198055',
    'emp': '0',
    'lang': 'ru',
    'locale': 'ru',
    'page': '2',
    'pricemarginCoeff': '1.0',
    'reg': '0',
    'regions': '68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48',
    'sort': 'popular',
    'spp': '0',
    'subject': '438;440;556;596;2786;2826;4928;6350',  # - id представленных категорий товаров,
    # можно вызывать по одному, это будет равносильно фильтрации на странице
    # 'supplier': '181237;225188;231062',  # Список поставщиков, выбор элемента из списка
    # аналогичен пред. пункту - наложение фильтра на товары
}

url = 'https://catalog.wb.ru/catalog/shealth/catalog'
