import requests
import json
from config import headers


class ExceptionCurverter(Exception):
    pass


class CurrencyNameError(ExceptionCurverter):
    def __str__(self):
        return 'Проверьте правильность указания валют'


class InputError(ExceptionCurverter):
    def __str__(self):
        return 'Неверный ввод. Чтобы еще раз прочитать правила использования наберите "/help"'


class Converter:
    available_currency = {'AED': 'Дирхам ОАЭ', 'AFN': 'Афганский афгани', 'ALL': 'Албаниский лек',
                          'AMD': 'Армянский драм', 'ANG': 'Нидерландский антильский гульден',
                          'AOA': 'Ангольская кванза', 'ARS': 'Аргентинское песо', 'AUD': 'Австралийский доллар',
                          'AWG': 'Арубанский флорин', 'AZN': 'Азербайджанский манат',
                          'BAM': 'Конвертируемая марка Боснии и Герцеговины', 'BBD': 'Барбадосский доллар',
                          'BDT': 'Бангладешская така', 'BGN': 'Болгарский лев', 'BHD': 'Бахрейнский динар',
                          'BIF': 'Бурундийский франк', 'BMD': 'Бермудский доллар', 'BND': 'Брунейский доллар',
                          'BOB': 'Боливийский боливиано', 'BRL': 'Бразильский реал', 'BSD': 'Багамский доллар',
                          'BTC': 'Биткойн', 'BTN': 'Бутанский нгултрум', 'BWP': 'Ботсванская пула',
                          'BYN': 'Белорусский рубль', 'BZD': 'Белизский доллар', 'CAD': 'Канадский доллар',
                          'CDF': 'Конголезский франк', 'CHF': 'Швейцарский франк',
                          'CLF': 'Чилийская расчетная единица (UF)', 'CLP': 'Чилийское песо', 'CNY': 'Китайский юань',
                          'COP': 'Колумбийское песо', 'CRC': 'Костариканский колон',
                          'CUC': 'Кубинское конвертируемое песо', 'CUP': 'Кубинское песо', 'CVE': 'Эскудо Кабо-Верде',
                          'CZK': 'Чешская крона', 'DJF': 'Джибутийский франк', 'DKK': 'датская крона',
                          'DOP': 'Доминиканское песо', 'DZD': 'Алжирский динар', 'EGP': 'Египетский фунт',
                          'ERN': 'Эритрейская накфа', 'ETB': 'Эфиопский быр', 'EUR': 'Евро', 'FJD': 'Доллар Фиджи',
                          'FKP': 'Фунт Фолклендских островов', 'GBP': 'Британский фунт стерлингов',
                          'GEL': 'Грузинский лари', 'GGP': 'Гернсийский фунт', 'GHS': 'Ганский седи',
                          'GIP': 'Гибралтарский фунт', 'GMD': 'Гамбийский даласи', 'GNF': 'Гвинейский франк',
                          'GTQ': 'Гватемальский кетсаль', 'GYD': 'Гайанский доллар', 'HKD': 'Гонконгский доллар',
                          'HNL': 'Гондурасская Лемпира', 'HRK': 'Хорватская куна', 'HTG': 'Гаитянский гурд',
                          'HUF': 'Венгерский форинт', 'IDR': 'Индонезийская рупия', 'ILS': 'Израильский новый шекель',
                          'IMP': 'мэнский фунт', 'INR': 'индийская рупия', 'IQD': 'Иракский динар',
                          'IRR': 'Иранский риал', 'ISK': 'Исландская крона', 'JEP': 'Джерсийский фунт',
                          'JMD': 'Ямайский доллар', 'JOD': 'Иорданский динар', 'JPY': 'Японская йена',
                          'KES': 'Кенийский шиллинг', 'KGS': 'Киргизский сом', 'KHR': 'Камбоджийский риель',
                          'KMF': 'Коморский франк', 'KPW': 'Северокорейская вона', 'KRW': 'Южнокорейский вон',
                          'KWD': 'Кувейтский динар', 'KYD': 'Доллар Каймановых островов', 'KZT': 'Казахстанский тенге',
                          'LAK': 'Лаосский кип', 'LBP': 'Ливанский фунт', 'LKR': 'Шри-Ланка рупий',
                          'LRD': 'Либерийский доллар', 'LSL': 'Лоти Лесото', 'LTL': 'Литовский лит',
                          'LVL': 'Латвийский лат', 'LYD': 'Ливийский динар', 'MAD': 'Марокканский дирхам',
                          'MDL': 'Молдавский Лев', 'MGA': 'Малагасийский ариари', 'MKD': 'Македонский денар',
                          'MMK': 'Мьянманский кьят', 'MNT': 'Монгольский тугрик', 'MOP': 'Маканская патака',
                          'MRO': 'Мавританская угуйя', 'MUR': 'Маврикийская рупия', 'MVR': 'Мальдивская рупия',
                          'MWK': 'Малавийская квача', 'MXN': 'Мексиканское песо', 'MYR': 'Малайзийский ринггит',
                          'MZN': 'Мозамбикский метикал', 'NAD': 'Намибийский доллар', 'NGN': 'Нигерийская Найра',
                          'NIO': 'Никарагуанская Кордова', 'NOK': 'Норвежская крона', 'NPR': 'Непальская рупия',
                          'NZD': 'Новозеландский доллар', 'OMR': 'Оманский риал', 'PAB': 'Панамский бальбоа',
                          'PEN': 'Перуанский новый соль', 'PGK': 'Папуа-Новая Гвинея Кина', 'PHP': 'Филиппинское песо',
                          'PKR': 'Пакистанская рупия', 'PLN': 'Польский Злотый', 'PYG': 'Парагвайский гуарани',
                          'QAR': 'Катарский риал', 'RON': 'Румынский лей', 'RSD': 'Сербский динар',
                          'RUB': 'Российский рубль', 'RWF': 'Руандийский франк', 'SAR': 'Саудовский риал',
                          'SBD': 'Доллар Соломоновых островов', 'SCR': 'Сейшельская рупия', 'SDG': 'Суданский фунт',
                          'SEK': 'Шведская крона', 'SGD': 'Сингапурский доллар', 'SHP': 'Фунт Святой Елены',
                          'SLL': 'Сьерра-Леоне Леоне', 'SOS': 'Сомалийский шиллинг', 'SRD': 'Суринамский доллар',
                          'STD': 'Добра Сан-Томе и Принсипи', 'SYP': 'Сирийский фунт', 'SZL': 'Лилагени Эсватини',
                          'THB': 'Таиландский бат', 'TJS': 'Таджикисая сомони', 'TMT': 'Туркменистан Манат',
                          'TND': 'Тунисский динар', 'TOP': 'Тонганский паанга', 'TRY': 'Турецкая лира',
                          'TTD': 'Доллар Тринидада и Тобаго', 'TWD': 'Новый тайваньский доллар',
                          'TZS': 'Танзанийский шиллинг', 'UAH': 'Украинская Гривна', 'UGX': 'Угандийский шиллинг',
                          'USD': 'Американский доллар', 'UYU': 'Уругвайское песо', 'UZS': 'Узбекский сом',
                          'VEF': 'Венесуэльский Боливар Фуэрте', 'VES': 'Венесуэльский Боливар',
                          'VND': 'Вьетнамский донг', 'VUV': 'Вануату Вату', 'WST': 'Самоанская Тала',
                          'XAG': 'Серебро (тройская унция)', 'XAU': 'Золото (тройская унция)',
                          'XCD': 'Восточно-карибский доллар', 'XDR': 'Специальные права заимствования (МВФ)',
                          'XPF': 'Тихоокеанский Франк', 'YER': 'Йеменский риал', 'ZAR': 'Южноафриканский рэнд',
                          'ZMW': 'Замбийская квача', 'ZWL': 'Зимбабвийский доллар'}
    keys_of_available_currency = list(available_currency.keys())

    def __init__(self, currency_from: str, currency_to: str, amount: str):
        self.currency_to = currency_to
        self.currency_from = currency_from
        self.amount = amount

    # Подготовка запроса конвертации
    def convert(self) -> str:
        url = f"https://api.apilayer.com/fixer/convert?to={self.currency_to}&" \
              f"from={self.currency_from}&amount={self.amount}"
        param = 'result'
        return f'{self.amount} {self.currency_from.upper()} = ' \
               f'{self.response_to_request(url, param):.2f} {self.currency_to.upper()}'

    @staticmethod  # Вывод доступных валют
    def print_currency() -> str:
        available_currency_str = ''
        for key, value in Converter.available_currency.items():
            available_currency_str += '\n' + f'{key}: {value}'
        return available_currency_str

    @staticmethod  # Получение и обработка ответа на запрос
    def response_to_request(url: str, param: str) -> str:
        response = requests.get(url, headers=headers)
        result = json.loads(response.text)
        return result[param]


class InputHandling:  # Обработка полученного сообщения
    def __init__(self, message):
        self.message = message
        self.convert = None

    # Проверка на количество введенных аргументов
    def message_to_list(self) -> str:
        try:
            message_to_list = self.message.split()
            if len(message_to_list) == 3:
                return self.data_validation(*message_to_list)
            else:
                raise InputError()
        except ExceptionCurverter as e:
            return e

    # Проверка значений полученных аргументов
    def data_validation(self, currency_from: str, currency_to: str, amount: str) -> str:
        try:
            if currency_from.upper() not in Converter.keys_of_available_currency or \
                    currency_to.upper() not in Converter.keys_of_available_currency:
                raise CurrencyNameError()
            float(amount)
        except ExceptionCurverter as e:
            return e
        except ValueError:
            return 'Введено неверное количество конвертируемой валюты'
        self.convert = Converter(currency_from, currency_to, amount)
        return self.convert.convert()
