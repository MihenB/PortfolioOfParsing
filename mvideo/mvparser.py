import requests
import json

cookies = {
    '_ym_uid': '1632677838198888484',
    'MVID_CART_MULTI_DELETE': 'true',
    'PRESELECT_COURIER_DELIVERY_FOR_KBT': 'false',
    'searchType2': '1',
    'PICKUP_SEAMLESS_AB_TEST': '2',
    'MVID_CALC_BONUS_RUBLES_PROFIT': 'false',
    'MVID_ADDRESS_COMMENT_AB_TEST': '2',
    'PROMOLISTING_WITHOUT_STOCK_AB_TEST': '2',
    'MAIN_PAGE_VARIATION': '3',
    'MVID_ABC_TEST_WIDGET': '0',
    'MVID_AB_PROMO_DAILY': '1',
    'MVID_AB_TEST_COMPARE_ONBOARDING': 'true',
    'MVID_BLACK_FRIDAY_ENABLED': 'true',
    'MVID_IS_NEW_BR_WIDGET': 'true',
    'MVID_NEW_ACCESSORY': 'true',
    'MVID_NEW_MBONUS_BLOCK': 'true',
    'MVID_PRICE_FIRST': '2',
    'MVID_PRM20_CMS': 'true',
    'MVID_SERVICES': '111',
    'NEED_REQUIRE_APPLY_DISCOUNT': 'true',
    'MVID_NEW_LK_OTP_TIMER': 'true',
    'HINTS_FIO_COOKIE_NAME': '2',
    'MVID_FILTER_CODES': 'true',
    'MVID_GET_LOCATION_BY_DADATA': 'DaData',
    'MVID_WEBP_ENABLED': 'true',
    'wurfl_device_id': 'generic_web_browser',
    'MVID_TAXI_DELIVERY_INTERVALS_VIEW': 'old',
    'MVID_GIFT_KIT': 'true',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '__SourceTracker': 'google__organic',
    'admitad_deduplication_cookie': 'google__organic',
    'tmr_lvid': '916d8c8aef869312b6f0f1892fce7030',
    'tmr_lvidTS': '1632677837985',
    'gdeslon.ru.__arc_domain': 'gdeslon.ru',
    'gdeslon.ru.user_id': '33ffda2e-f7fd-442f-b79a-fb7f07914df4',
    'afUserId': '0f4e5bec-ded7-494c-9437-c138ed67eb8e-p',
    'adrcid': 'ArcfPaDjg7ojq4MfMH38_lg',
    '_ym_d': '1650131604',
    'deviceType': 'desktop',
    'flocktory-uuid': '5af84911-7774-414a-89dd-9e1253c962f6-6',
    'COMPARISON_INDICATOR': 'false',
    'MVID_NEW_DESKTOP_FILTERS': 'true',
    'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
    'MVID_AB_SERVICES_DESCRIPTION': 'var2',
    'MVID_CATALOG_STATE': '1',
    'MVID_FILTER_TOOLTIP': '1',
    'MVID_FLOCKTORY_ON': 'true',
    'MVID_LAYOUT_TYPE': '1',
    'MVID_SERVICES_MINI_BLOCK': 'var2',
    '__ttl__widget__ui': '1657131294765-11fc4ad9cb52',
    'MVID_MCLICK': 'true',
    'MVID_CRM_ID': '0047140908',
    'MVID_OLD_NEW': 'eyJjb21wYXJpc29uIjpmYWxzZSwiZmF2b3JpdGUiOmZhbHNlLCJjYXJ0Ijp0cnVlfQ==',
    'MVID_GTM_DELAY': 'true',
    'MVID_GUEST_ID': '21212060175',
    'MVID_LP_HANDOVER': '1',
    'MVID_LP_SOLD_VARIANTS': '3',
    'MVID_MINI_PDP': 'true',
    'advcake_track_id': '21290f4b-e825-c027-33a8-ccd3d84bcfd5',
    'advcake_session_id': '9eadef8d-a8e8-52c3-0afd-ea76ad13027d',
    'MVID_GEOLOCATION_NEEDED': 'false',
    'MVID_NEW_OLD': 'eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOmZhbHNlfQ==',
    'MVID_MINDBOX_DYNAMICALLY': 'true',
    'MVID_MOBILE_FILTERS': 'true',
    'MVID_NEW_LK': 'true',
    'MVID_NEW_LK_LOGIN': 'true',
    'flacktory': 'no',
    '_gid': 'GA1.2.1323991513.1660571198',
    '_ym_isad': '2',
    'SMSError': '',
    'authError': '',
    'MVID_TIMEZONE_OFFSET': '3',
    'MVID_CITY_ID': 'CityCZ_975',
    'MVID_REGION_SHOP': 'S002',
    'MVID_REGION_ID': '1',
    'MVID_CITY_CHANGED': 'false',
    'MVID_KLADR_ID': '7700000000000',
    'mindboxDeviceUUID': '4f723e23-7026-484d-b9a8-7babaa8e041f',
    'directCrm-session': '%7B%22deviceGuid%22%3A%224f723e23-7026-484d-b9a8-7babaa8e041f%22%7D',
    'BIGipServeratg-ps-prod_tcp80': '2936331274.20480.0000',
    'bIPs': '672961728',
    'MVID_GTM_BROWSER_THEME': '1',
    '__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VtVX0fLU16MX1ocz9GNkMVbWEdTVEfW1t1e3NXJDQkFXRAeWxfeycsGBcUR3EoR3Z3V20ZGkBmJmBOYSNFXj56Kx8RfHIkVQ8MYEVDX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkdzcy5CZiNnS18lQ1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYVy9wJBdIUn47FmtuR2dHV0wXX0I7OFhBEXVbPUV0dC07bh1nOVURCxIXRF5cVWl1ZxlMQFcvDS44Xi1vHmVMYCVHWU0KKBsRe2cVHkBPG1AINDZicFcnKxEmVD9HGUplTnsJXWMTOEQhCXY9PxsQOg==rFSYPw==',
    '__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VtVX0fLU16MX1ocz9GNkMVbWEdTVEfW1t1e3NXJDQkFXRAeWxfeycsGBcUR3EoR3Z3V20ZGkBmJmBOYSNFXj56Kx8RfHIkVQ8MYEVDX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkdzcy5CZiNnS18lQ1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYVy9wJBdIUn47FmtuR2dHV0wXX0I7OFhBEXVbPUV0dC07bh1nOVURCxIXRF5cVWl1ZxlMQFcvDS44Xi1vHmVMYCVHWU0KKBsRe2cVHkBPG1AINDZicFcnKxEmVD9HGUplTnsJXWMTOEQhCXY9PxsQOg==rFSYPw==',
    'cfidsgib-w-mvideo': '9Hhyi9lAGJOnrERTRjKhxJu9xPTNhw+/pEcZvHmSnUoDS4etorGFb9DE4q6FhCXonT+p/Zo5dwcT9f2V8/rR8W6s/Wge5LqxfCUK0kzND0rekSiHGA3p/uDjC/wAC5FIDy/F5NuT2puVNvbxxD5cSNOkr+nycSav+2aXfg==',
    'cfidsgib-w-mvideo': '9Hhyi9lAGJOnrERTRjKhxJu9xPTNhw+/pEcZvHmSnUoDS4etorGFb9DE4q6FhCXonT+p/Zo5dwcT9f2V8/rR8W6s/Wge5LqxfCUK0kzND0rekSiHGA3p/uDjC/wAC5FIDy/F5NuT2puVNvbxxD5cSNOkr+nycSav+2aXfg==',
    'gsscgib-w-mvideo': 'MuQP4pTBN9nn7PoyymMtjvCpWYvrE1COLh5Mk0wtCJC2me4/9zhF8f87ovciHwOkX8b09+mDTKfokl0UzF2s8GAwbEAUVml+G8sw2vJr+jBNlaS5t/7lwBDQiVRgiETFaybWaJ/d+k6IlPXfg8YQg9OL5TwD4PREyXSkuopK95egYvLJx8xNwtyu/y1FZmg6kT1yu1AsaFMkpE/KkTtYo0Un170V8nmcMcIhWRs4JKdJUbjA7hxiJRWC8MbNMQ==',
    'gsscgib-w-mvideo': 'MuQP4pTBN9nn7PoyymMtjvCpWYvrE1COLh5Mk0wtCJC2me4/9zhF8f87ovciHwOkX8b09+mDTKfokl0UzF2s8GAwbEAUVml+G8sw2vJr+jBNlaS5t/7lwBDQiVRgiETFaybWaJ/d+k6IlPXfg8YQg9OL5TwD4PREyXSkuopK95egYvLJx8xNwtyu/y1FZmg6kT1yu1AsaFMkpE/KkTtYo0Un170V8nmcMcIhWRs4JKdJUbjA7hxiJRWC8MbNMQ==',
    'fgsscgib-w-mvideo': 'Oi3l040c166ba90357ecb9fb8fd7252cb1de05bf',
    'fgsscgib-w-mvideo': 'Oi3l040c166ba90357ecb9fb8fd7252cb1de05bf',
    'cfidsgib-w-mvideo': 'tegezGSOeknMlivEdQv+VQWWlxoDTOgssttJCdsfFJpSMKSBtFaEMJXWwo3LkOwVV6q96lxkulMkbXwood6ViOW5WE26ONSYyg+WwCRZaZ3KGxT0tSAYv1WvUj/eZ/9odmO6CnLMySvDBVgIlozBx8OyTQOpyq5ZkatD8g==',
    'CACHE_INDICATOR': 'false',
    '__lhash_': '0f00f59ba3e2d90b4062dd28cd4053b6',
    'AF_SYNC': '1660574627327',
    '_ga': 'GA1.2.1902504243.1650131599',
    'tmr_detect': '0%7C1660574656979',
    'MVID_ENVCLOUD': 'prod2',
    'tmr_reqNum': '468',
    'JSESSIONID': 'bQH8v6dSjvsQ2QT159L5GX9h2QG2t4GL3MQnkPFfmhvLbkdS2gDq!519178429',
    '_ga_CFMZTSS5FM': 'GS1.1.1660574594.8.1.1660575028.0',
    '_ga_BNX5WPP3YK': 'GS1.1.1660574594.8.1.1660575028.60',
}
headers = {
    'authority': 'www.mvideo.ru',
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=8daea04ea1f3407d8824edf7cd4ff585,sentry-sample_rate=1',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ym_uid=1632677838198888484; MVID_CART_MULTI_DELETE=true; PRESELECT_COURIER_DELIVERY_FOR_KBT=false; searchType2=1; PICKUP_SEAMLESS_AB_TEST=2; MVID_CALC_BONUS_RUBLES_PROFIT=false; MVID_ADDRESS_COMMENT_AB_TEST=2; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; MAIN_PAGE_VARIATION=3; MVID_ABC_TEST_WIDGET=0; MVID_AB_PROMO_DAILY=1; MVID_AB_TEST_COMPARE_ONBOARDING=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_IS_NEW_BR_WIDGET=true; MVID_NEW_ACCESSORY=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PRICE_FIRST=2; MVID_PRM20_CMS=true; MVID_SERVICES=111; NEED_REQUIRE_APPLY_DISCOUNT=true; MVID_NEW_LK_OTP_TIMER=true; HINTS_FIO_COOKIE_NAME=2; MVID_FILTER_CODES=true; MVID_GET_LOCATION_BY_DADATA=DaData; MVID_WEBP_ENABLED=true; wurfl_device_id=generic_web_browser; MVID_TAXI_DELIVERY_INTERVALS_VIEW=old; MVID_GIFT_KIT=true; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; tmr_lvid=916d8c8aef869312b6f0f1892fce7030; tmr_lvidTS=1632677837985; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=33ffda2e-f7fd-442f-b79a-fb7f07914df4; afUserId=0f4e5bec-ded7-494c-9437-c138ed67eb8e-p; adrcid=ArcfPaDjg7ojq4MfMH38_lg; _ym_d=1650131604; deviceType=desktop; flocktory-uuid=5af84911-7774-414a-89dd-9e1253c962f6-6; COMPARISON_INDICATOR=false; MVID_NEW_DESKTOP_FILTERS=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_AB_SERVICES_DESCRIPTION=var2; MVID_CATALOG_STATE=1; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_LAYOUT_TYPE=1; MVID_SERVICES_MINI_BLOCK=var2; __ttl__widget__ui=1657131294765-11fc4ad9cb52; MVID_MCLICK=true; MVID_CRM_ID=0047140908; MVID_OLD_NEW=eyJjb21wYXJpc29uIjpmYWxzZSwiZmF2b3JpdGUiOmZhbHNlLCJjYXJ0Ijp0cnVlfQ==; MVID_GTM_DELAY=true; MVID_GUEST_ID=21212060175; MVID_LP_HANDOVER=1; MVID_LP_SOLD_VARIANTS=3; MVID_MINI_PDP=true; advcake_track_id=21290f4b-e825-c027-33a8-ccd3d84bcfd5; advcake_session_id=9eadef8d-a8e8-52c3-0afd-ea76ad13027d; MVID_GEOLOCATION_NEEDED=false; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOmZhbHNlfQ==; MVID_MINDBOX_DYNAMICALLY=true; MVID_MOBILE_FILTERS=true; MVID_NEW_LK=true; MVID_NEW_LK_LOGIN=true; flacktory=no; _gid=GA1.2.1323991513.1660571198; _ym_isad=2; SMSError=; authError=; MVID_TIMEZONE_OFFSET=3; MVID_CITY_ID=CityCZ_975; MVID_REGION_SHOP=S002; MVID_REGION_ID=1; MVID_CITY_CHANGED=false; MVID_KLADR_ID=7700000000000; mindboxDeviceUUID=4f723e23-7026-484d-b9a8-7babaa8e041f; directCrm-session=%7B%22deviceGuid%22%3A%224f723e23-7026-484d-b9a8-7babaa8e041f%22%7D; BIGipServeratg-ps-prod_tcp80=2936331274.20480.0000; bIPs=672961728; MVID_GTM_BROWSER_THEME=1; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VtVX0fLU16MX1ocz9GNkMVbWEdTVEfW1t1e3NXJDQkFXRAeWxfeycsGBcUR3EoR3Z3V20ZGkBmJmBOYSNFXj56Kx8RfHIkVQ8MYEVDX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkdzcy5CZiNnS18lQ1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYVy9wJBdIUn47FmtuR2dHV0wXX0I7OFhBEXVbPUV0dC07bh1nOVURCxIXRF5cVWl1ZxlMQFcvDS44Xi1vHmVMYCVHWU0KKBsRe2cVHkBPG1AINDZicFcnKxEmVD9HGUplTnsJXWMTOEQhCXY9PxsQOg==rFSYPw==; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VtVX0fLU16MX1ocz9GNkMVbWEdTVEfW1t1e3NXJDQkFXRAeWxfeycsGBcUR3EoR3Z3V20ZGkBmJmBOYSNFXj56Kx8RfHIkVQ8MYEVDX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkdzcy5CZiNnS18lQ1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYVy9wJBdIUn47FmtuR2dHV0wXX0I7OFhBEXVbPUV0dC07bh1nOVURCxIXRF5cVWl1ZxlMQFcvDS44Xi1vHmVMYCVHWU0KKBsRe2cVHkBPG1AINDZicFcnKxEmVD9HGUplTnsJXWMTOEQhCXY9PxsQOg==rFSYPw==; cfidsgib-w-mvideo=9Hhyi9lAGJOnrERTRjKhxJu9xPTNhw+/pEcZvHmSnUoDS4etorGFb9DE4q6FhCXonT+p/Zo5dwcT9f2V8/rR8W6s/Wge5LqxfCUK0kzND0rekSiHGA3p/uDjC/wAC5FIDy/F5NuT2puVNvbxxD5cSNOkr+nycSav+2aXfg==; cfidsgib-w-mvideo=9Hhyi9lAGJOnrERTRjKhxJu9xPTNhw+/pEcZvHmSnUoDS4etorGFb9DE4q6FhCXonT+p/Zo5dwcT9f2V8/rR8W6s/Wge5LqxfCUK0kzND0rekSiHGA3p/uDjC/wAC5FIDy/F5NuT2puVNvbxxD5cSNOkr+nycSav+2aXfg==; gsscgib-w-mvideo=MuQP4pTBN9nn7PoyymMtjvCpWYvrE1COLh5Mk0wtCJC2me4/9zhF8f87ovciHwOkX8b09+mDTKfokl0UzF2s8GAwbEAUVml+G8sw2vJr+jBNlaS5t/7lwBDQiVRgiETFaybWaJ/d+k6IlPXfg8YQg9OL5TwD4PREyXSkuopK95egYvLJx8xNwtyu/y1FZmg6kT1yu1AsaFMkpE/KkTtYo0Un170V8nmcMcIhWRs4JKdJUbjA7hxiJRWC8MbNMQ==; gsscgib-w-mvideo=MuQP4pTBN9nn7PoyymMtjvCpWYvrE1COLh5Mk0wtCJC2me4/9zhF8f87ovciHwOkX8b09+mDTKfokl0UzF2s8GAwbEAUVml+G8sw2vJr+jBNlaS5t/7lwBDQiVRgiETFaybWaJ/d+k6IlPXfg8YQg9OL5TwD4PREyXSkuopK95egYvLJx8xNwtyu/y1FZmg6kT1yu1AsaFMkpE/KkTtYo0Un170V8nmcMcIhWRs4JKdJUbjA7hxiJRWC8MbNMQ==; fgsscgib-w-mvideo=Oi3l040c166ba90357ecb9fb8fd7252cb1de05bf; fgsscgib-w-mvideo=Oi3l040c166ba90357ecb9fb8fd7252cb1de05bf; cfidsgib-w-mvideo=tegezGSOeknMlivEdQv+VQWWlxoDTOgssttJCdsfFJpSMKSBtFaEMJXWwo3LkOwVV6q96lxkulMkbXwood6ViOW5WE26ONSYyg+WwCRZaZ3KGxT0tSAYv1WvUj/eZ/9odmO6CnLMySvDBVgIlozBx8OyTQOpyq5ZkatD8g==; CACHE_INDICATOR=false; __lhash_=0f00f59ba3e2d90b4062dd28cd4053b6; AF_SYNC=1660574627327; _ga=GA1.2.1902504243.1650131599; tmr_detect=0%7C1660574656979; MVID_ENVCLOUD=prod2; tmr_reqNum=468; JSESSIONID=bQH8v6dSjvsQ2QT159L5GX9h2QG2t4GL3MQnkPFfmhvLbkdS2gDq!519178429; _ga_CFMZTSS5FM=GS1.1.1660574594.8.1.1660575028.0; _ga_BNX5WPP3YK=GS1.1.1660574594.8.1.1660575028.60',
    'pragma': 'no-cache',
    'referer': 'https://www.mvideo.ru/naushniki-54/naushniki-3967/f/tolko-v-nalichii=da?reff=menu_main_acc&page=2',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '8daea04ea1f3407d8824edf7cd4ff585-9972512cc845e616-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'x-set-application-id': 'c11c8dd0-74e9-46df-9c9d-b4be5dd04b97',
}


def write_to_json(data):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open('result_data.json', 'w', encoding='UTF-8') as file:
        file.write(json_data)


def get_session():
    return requests.Session()


def get_total():
    params = {
        'categoryId': '3967',
        'offset': '24',
        'limit': '24',
        'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
        'doTranslit': 'true',
    }
    session = get_session()
    response = session.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                           headers=headers)
    a = dict(response.json())
    total = a['body']['total']
    return int(total)


def get_product_ids():
    result_list = []
    offset = 0
    total = get_total()
    while offset <= total:
        params = {
            'categoryId': '3967',
            'offset': offset,
            'limit': '24',
            'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
            'doTranslit': 'true',
        }
        session = get_session()
        response = session.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                               headers=headers)
        all_info = dict(response.json())
        ids = dict(all_info['body'])
        list_of_ids = ids['products']
        for i in list_of_ids:
            result_list.append(i)
        offset += 24
    return result_list


def get_products_data(list_ids):
    result = []
    session = get_session()
    index = 0
    total = get_total()
    while index <= total:
        try:
            json_data = {
                'productIds': list_ids[0+index:23+index],
                'mediaTypes': [
                    'images',
                ],
                'category': True,
                'status': True,
                'brand': True,
                'propertyTypes': [
                    'KEY',
                ],
                'propertiesConfig': {
                    'propertiesPortionSize': 5,
                },
                'multioffer': False,
            }
            response = session.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers,
                                    json=json_data)
            body = dict(response.json())['body']
            for i in body['products']:
                result.append(i)
            index += 24
        except requests.exceptions.JSONDecodeError:
            continue
    return result


def main():
    print(get_total())
    list_ids = get_product_ids()
    data = get_products_data(list_ids)
    print(len(data))
    write_to_json(data)


if __name__ == '__main__':
    main()
