from typing import Optional
import json
from bs4 import BeautifulSoup
import cfscrape
import requests
from parse_package.user_agent import ExtendedUserAgent
import undetected_chromedriver
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


class JSONParseException(Exception):
    pass


class NoResponseFromPage4xxError(Exception):
    pass


class ScrapResponse:
    def __init__(self,
                 page_source: str):
        self.__page_source = page_source

    def __repr__(self):
        return f'[ScrapResponse]\n<begin_fragment>\n{self.__page_source[:100]} ...\n<end_fragment>\n'

    @property
    def html(self) -> str:
        return self.__page_source

    @property
    def json(self) -> Optional[dict]:
        try:
            try:
                return json.loads(self.__page_source)
            except json.decoder.JSONDecodeError:
                try:
                    return json.loads(self.soup.find('body').text)
                except json.decoder.JSONDecodeError:
                    raise JSONParseException("Tag <body> of the page doesn't contain json, nothing to parse")
                except AttributeError:
                    raise JSONParseException("Tag <body> is empty, nothing to parse")
        except JSONParseException as err:
            print(f'[ERROR] {str(err)}')

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.__page_source, 'lxml')

    def json_to_file(self, file) -> bool:
        """
            Производит запись json в файл.
            Возвращает True в случае успеха и False в случае ошибки.
        """
        try:
            json.dump(
                self.json,
                file,
                indent=4,
                ensure_ascii=False
            )
            return True
        except Exception as ex:
            print(str(ex))
            return False

    def html_to_file(self, file) -> bool:
        """
            Производит запись html в файл.
            Возвращает True в случае успеха и False в случае ошибки.
        """
        try:
            print(
                self.html,
                file=file
            )
            return True
        except Exception as ex:
            print(str(ex))
            return False


class ScrapSession:
    ua = ExtendedUserAgent()
    default_headers = {
        'User-Agent': f'{ua.random_fresh_ua}',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
    }

    @staticmethod
    def install_undetected_chrome_selenium_driver(headless: bool,
                                                  proxies: bool,
                                                  chrome_driver_manager=ChromeDriverManager()) -> WebDriver:
        """
            Возвращает модифицированную версию классического selenium Chrome драйвера
            для обхода большинства видов блокировок и проверок на ботов.
        """
        options = webdriver.ChromeOptions()
        options.headless = headless
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # proxies with login and password

        # if proxies:
        #     import os
        #     plugin_file = 'proxy_auth_plugin.zip'
        #     if not os.path.exists(plugin_file):
        #         import zipfile
        #         from config import manifest_json, background_js
        #         with zipfile.ZipFile(plugin_file, 'w') as zp:
        #             zp.writestr("manifest.json", manifest_json)
        #             zp.writestr("background.js", background_js)
        #     options.add_extension(plugin_file)

        # proxies with auth by ip
        if proxies:
            from parse_package.proxy import ip, port
            options.add_argument(f'--proxy-server={ip}:{port}')
        return undetected_chromedriver.Chrome(
            service=Service(chrome_driver_manager.install()),
            options=options
        )

    @staticmethod
    def install_selenium_chrome_driver_configured(headless: bool,
                                                  proxies: bool,
                                                  chrome_driver_manager=ChromeDriverManager()) -> WebDriver:
        """
            Метод, устанавливающий конфигурацию для "чистого" selenium драйвера, которые позволяют
            обходить некоторые методы обнаружения ботов.
            Возвращает готовый драйвер.
        """
        ua = ExtendedUserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={ua.random_fresh_ua}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # proxies with login and password

        # if proxies:
        #     import os
        #     plugin_file = 'proxy_auth_plugin.zip'
        #     if not os.path.exists(plugin_file):
        #         import zipfile
        #         from config import manifest_json, background_js
        #         with zipfile.ZipFile(plugin_file, 'w') as zp:
        #             zp.writestr("manifest.json", manifest_json)
        #             zp.writestr("background.js", background_js)
        #     options.add_extension(plugin_file)

        # proxies with auth by ip
        if proxies:
            from parse_package.proxy import ip, port
            # print(f'--proxy-server={_proxies[f"{protocol}"]}')
            options.add_argument(f'--proxy-server={ip}:{port}')
        options.headless = headless
        # Нужно добавить функционал:
        #   - поддержка вывода списка запросов через selenium_wire
        #   - поддержка многопоточности
        return webdriver.Chrome(
            service=Service(chrome_driver_manager.install()),
            options=options
        )

    class DriverWrapper:
        """
            Класс, реализующий менеджер контекста для удобной работы с драйверами браузера.
        """

        def __init__(self, driver: WebDriver):
            self.driver = driver

        def __enter__(self):
            return self.driver

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.driver.close()
            self.driver.quit()
            if exc_type is WebDriverException:
                raise NoResponseFromPage4xxError(exc_val)
            elif exc_type:
                raise exc_type(exc_val)

    def __init__(self):
        self.pure_session = requests.Session()
        self.pure_session.headers = self.default_headers
        self.secured_session = cfscrape.create_scraper(sess=requests.Session())

        self.configured_pure_driver_wrapper = None
        self.secured_driver_wrapper = None

    def init_driver(self,
                    browser_headless_mode: bool = True,
                    secured: bool = False,
                    proxies: bool = False) -> None:
        """
            Инициализирует драйвера по запросу. Процесс длительный и тяжеловесный, потому вынесен в отдельный метод.

            Есть смысл вызывать из main кода напрямую только если необходимо изменить параметр headless браузера
            (по умолчанию True, то есть браузер запускается в фоновом режиме для экономии ресурсов)
            или добавить proxies (по умолчанию отключен).

            В новой версии пакета все соответствующие параметры перенесены в метод render,
            init_driver теперь вызывается неявно.
        """
        if secured:
            self.secured_driver_wrapper = self.DriverWrapper(
                self.install_undetected_chrome_selenium_driver(headless=browser_headless_mode,
                                                               proxies=proxies)
            )
        else:
            self.configured_pure_driver_wrapper = self.DriverWrapper(
                self.install_selenium_chrome_driver_configured(headless=browser_headless_mode,
                                                               proxies=proxies)
            )

    def driver_initiated(self,
                         secured: bool) -> bool:
        """
            Проверяет, были ли инициализированы драйвера.
        """
        return secured and self.secured_driver_wrapper or not secured and self.configured_pure_driver_wrapper

    def refresh_session(self,
                        secured: bool = False) -> None:
        """
            Метод создает новый экземпляр защищенной или незащищенной сессии в зависимости от значения аргумента,
            сбрасывая при этом всю информацию о заголовках и cookies.
        """
        if secured:
            self.secured_session = cfscrape.create_scraper(sess=requests.Session())
        else:
            self.pure_session = requests.Session()

    def get_pure_session(self) -> requests.Session:
        """
            Возвращает "чистую" сессию, из которой можно получить ее текущие параметры (заголовки, cookies etc...)
        """
        return self.pure_session

    def get_secured_session(self) -> cfscrape.CloudflareScraper:
        """
            Возвращает "обернутую" сессию с защитой от CloudFlare,
            из которой можно получить ее текущие параметры (заголовки, cookies etc...)
        """
        return self.secured_session

    def get(self,
            url: str,
            secured: bool = False,
            proxies: bool = False,
            **kwargs) -> Optional[ScrapResponse]:
        """
            Метод представляет собой расширенную реализацию одноименного метода из библиотеки requests.
            Добавлена возможность делать запрос через модифицированную сессию с возможностью обхода ограничений
            для ботов.
        """
        if proxies:
            from parse_package.proxy import protocol, ip, port
            _proxies = {
                f'{protocol}': f'{ip}:{port}'
            }
        else:
            _proxies = None
        try:
            return ScrapResponse(self.secured_session.get(url=url, proxies=_proxies, **kwargs).text) if secured \
                else ScrapResponse(self.pure_session.get(url=url, proxies=_proxies, **kwargs).text)
        except requests.exceptions.ConnectionError as err:
            print(f'[ERROR] Connection error, possible caused by page return 4xx code. Error:\n{str(err)}')
        return None

    def post(self,
             url: str,
             secured: bool = False,
             proxies: bool = False,
             **kwargs) -> Optional[ScrapResponse]:
        """
            Метод представляет собой расширенную реализацию одноименного метода из библиотеки requests.
            Добавлена возможность делать запрос через модифицированную сессию с возможностью обхода ограничений
            для ботов.
        """
        if proxies:
            from parse_package.proxy import protocol, ip, port
            _proxies = {
                f'{protocol}': f'{ip}:{port}'
            }
        else:
            _proxies = None
        try:
            return ScrapResponse(self.secured_session.post(url=url, proxies=_proxies, **kwargs).text) if secured \
                else ScrapResponse(self.pure_session.post(url=url, proxies=_proxies, **kwargs).text)
        except requests.exceptions.ConnectionError as err:
            print(f'[ERROR] Connection error, possible caused by page return 4xx code. Error:\n{str(err)}')
        return None

    def render(self,
               url: str,
               func=None,
               args: tuple = tuple(),
               secured: bool = False,
               implicitly_wait: float = 10.0,
               proxies: bool = False,
               browser_headless_mode: bool = True) -> Optional[ScrapResponse]:
        """
        Метод позволяет исполнить весь JS код, который содержится на странице, и получить результат
        в виде объекта ScrapResponse.
            Логика работы метода:\n
        Проверка инициализации драйвера и его установка при необходимости ->\n
        Получение методом driver.get() нужной страницы -> \n
        Ожидание ее загрузки заданное время (implicitly_wait) -> \n
        Выполнение переданной в качестве аргумента функции func -> \n
        Закрытие браузера и отправка результатов.

            Пример создания функции для прокрутки страницы:\n

        def f(driver, your_arg) -> None:
            actions = ActionChains(driver)\n
            element = driver.find_element('xpath', "/html/body/div[1]/")\n
            actions.click(on_element=element).send_keys(Keys.END)\n
            actions.perform()\n

        В данном примере сначала создается объект ActionChains - своеобразное "временное хранилище" для будущей
        цепочки действий в браузере.

        Затем выполняется клик по некоторому элементу страницы, найденному в данном случае
        по его xpath, который можно скопировать в браузере из кода страницы (инструменты разработчика).
        Клик необходим в случае, когда полос прокрутки на странице несколько, и для выбора одной нужно кликнуть мышью в
        элемент, принадлежащий ей.

        Далее происходит нажатие клавиши End, которая прокручивает страницу до конца, а
        метод perform запускает исполнение цепочки действий.

            Пример вызова метода render с параметрами заданной функции:

        render(
            url=url,\n
            func=f,\n
            args=(your_arg,) ИЛИ args=tuple(your_arg)\n
        )\n

        :param browser_headless_mode: Параметр перенесен из метода init_driver, позволяет произвести рендеринг страницы
         в фоне, без открытия окна браузера (True - значение по умолчанию)
        :param proxies: boolean параметр, отвечающий за подключение proxies (см. файлы config.py и _proxies.py)
        :param url: url страницы для запроса.
        :param func: Функция, реализующая все необходимые действия,
         которые необходимо произвести на полученной странице.
         Ничего не возвращает. В качестве обязательного первого аргумента выступает driver класса
         selenium.webdriver.chrome.webdriver, а далее следуют необязательные аргументы, которые должны быть заданы
         следующим после объекта самой функции параметром метода render (см. описание след. параметра и пример)
        :param args: Необязательные аргументы, которые будут переданы в func во время ее исполнения.
        :param secured: Отвечает за то, из какого браузера, защищенного или незащищенного от обнаружения бота,
         будет сделан запрос. Следует отметить, что защищенный запрос зачастую требует больше времени, чем незащищенный.
        :param implicitly_wait: Время, которое браузер будет ожидать после get-запроса на страницу,
         перед исполнением func(driver, *args). Ожидание продлится менее заданного времени, если будет найден
         искомый элемент на странице (метод driver.find_element()).
        :return: ScrapResponse
        """

        if not self.driver_initiated(secured):
            self.init_driver(secured=secured,
                             proxies=proxies,
                             browser_headless_mode=browser_headless_mode)

        def driver_actions(_driver: WebDriver) -> str:
            """
                Отвечает за выполнение всех действий на странице. Возвращает ее исходный (html) код.
            """
            _driver.get(url=url)
            _driver.implicitly_wait(implicitly_wait)
            func(_driver, *args) if func else None
            return _driver.page_source

        try:
            if secured:
                with self.secured_driver_wrapper as driver:
                    page_source = driver_actions(driver)
            else:
                with self.configured_pure_driver_wrapper as driver:
                    page_source = driver_actions(driver)
            return ScrapResponse(page_source)
        except NoResponseFromPage4xxError as err:
            print("[ERROR] Page sent code 4xx which means that there is an error on server backend "
                  f"or you don't have access to the page. Error:\n{str(err)}")
        except Exception as err:
            print(f'[ERROR] Something went wrong. Error:\n{str(err)}')
        return None


def main():
    import time
    from config import url, headers, cookies

    # Рекомендую в будущем именно импортировать параметры,
    # потому как они занимают колоссальное количество места и
    # портят читабельность кода

    session = ScrapSession()

    # session.init_driver(browser_headless_mode=False, secured=True)
    # Больше не нужно вызывать этот метод, весь его функционал перенесен в метод render

    def func(driver: WebDriver):
        driver.implicitly_wait(5)
        time.sleep(1)

    try:
        print(
            session.get(
                url=url,
                # cookies=cookies,
                # headers=headers,
                # secured=True,
                # proxies=True,
                # json=json_data
            ).html
            # session.render(url=url,
            #                secured=True,
            #                implicitly_wait=0,
            #                func=func,
            #                proxies=True,
            #                browser_headless_mode=False).soup.find(id='d_clip_button').text.strip()
            # Может выкинуть AttributeError,
            # так как тип возвращаемого значения метода render - Optional[ScrapResponse],
            # что означает, что при определенных обстоятельствах (при возникновении исключения WebDriverException)
            # возвращается значение типа None
        )
    except AttributeError as err:
        print(f'[ERROR] {str(err)}')


if __name__ == '__main__':
    main()
