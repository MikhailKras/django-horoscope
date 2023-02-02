from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from datetime import datetime
from dataclasses import dataclass

# Create your views here.

signs = {
    "aries": "Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).",
    "taurus": "Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).",
    "gemini": "Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).",
    "cancer": "Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля).",
    "leo": "Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).",
    "virgo": "Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября).",
    "libra": "Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября).",
    "scorpio": "Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября).",
    "sagittarius": "Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря).",
    "capricorn": "Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января).",
    "aquarius": "Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля).",
    "pisces": "Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта)."
}

types_elems = {'fire': ["aries", "leo", "sagittarius"],
               'earth': ["taurus", "virgo", "capricorn"],
               'air': ["gemini", "libra", "aquarius"],
               'water': ["cancer", "scorpio", "pisces"]}


class ZodiacDay:
    def __init__(self, date: str):
        self.date = date
        if self.date == '02/29':
            self.date = '02/28'
        self.zodiacs_dict = {('03/21', '04/20'): 'aries',
                             ('04/21', '05/21'): 'taurus',
                             ('05/22', '06/21'): 'gemini',
                             ('06/22', '07/22'): 'cancer',
                             ('07/23', '08/21'): 'leo',
                             ('08/22', '09/23'): 'virgo',
                             ('09/24', '10/23'): 'libra',
                             ('10/24', '11/22'): 'scorpio',
                             ('11/23', '12/22'): 'sagittarius',
                             ('12/23', '12/31'): 'capricorn',
                             ('01/01', '01/20'): 'capricorn',
                             ('01/21', '02/19'): 'aquarius',
                             ('02/20', '03/20'): 'pisces'}
        self.zodiacs_dict_numbers = {
            key: value for key, value in zip(map(lambda x: (self.convert(x[0]), self.convert(x[1])), self.zodiacs_dict.keys()),
                                             self.zodiacs_dict.values())
        }

    def convert(self, date: str = None) -> int:
        if not date:
            date = self.date
        date_strptime = datetime.strptime(date, '%m/%d')
        day_of_year = date_strptime.timetuple().tm_yday
        return day_of_year

    def date_to_zodiac(self) -> str:
        try:
            date_number = self.convert(self.date)
        except ValueError:
            return 'Unknown day'
        check_in_interval_func = lambda x, y, z: y <= x <= z
        for dates in self.zodiacs_dict_numbers:
            if check_in_interval_func(date_number, *dates):
                return self.zodiacs_dict_numbers[dates]


@dataclass
class Person:
    name: str
    age: int

    def __str__(self):
        return f'This is {self.name} and his age is {self.age}'


def get_info_about_sign_zodiac(request, sign_zodiac: str) -> HttpResponse:
    description = signs.get(sign_zodiac)
    data = {
        'description_zodiac': description,
        'sign': sign_zodiac,
        'my_list': [1, 2, 3],
        'my_tuple': (1, 2, 3, 4, 5, 6, 7),
        'my_dict': {'name': 'Jack', 'age': 40},
        'my_int': 111,
        'my_float': 111.5,
        'my_class': Person('Will', 50),
    }
    return render(request, 'horoscope/info_zodiac.html', context=data)


def get_info_about_sign_zodiac_by_num(request, sign_zodiac: int) -> HttpResponse:
    zodiacs = list(signs)
    if sign_zodiac > len(zodiacs):
        return HttpResponseNotFound(f'Неправильный номер знака зодиака - {sign_zodiac}')
    name_zodiac = zodiacs[sign_zodiac - 1]
    redirect_url = reverse('horoscope-name', args=(name_zodiac,))
    return redirect(redirect_url)


def index(request) -> HttpResponse:
    data = {
        'zodiac_names': list(signs.keys())
    }
    return render(request, 'horoscope/index.html', context=data)
    # zodiacs = list(signs)
    # elements = ''
    # for zodiac in zodiacs:
    #     redirect_url = reverse('horoscope-name', args=(zodiac,))
    #     elements += f'<li style="font-size:26px"> <a href={redirect_url} target="_blank"> {zodiac.title()} </a> </li> '
    # response = f"""
    # <h1 style="font-size:30px; color:blue"> Zodiacs </h1>
    # <ol>
    # {elements}
    # </ol>
    # """
    # return HttpResponse(response)


def index_type(request) -> HttpResponse:
    html_elements = ''
    for elem in types_elems:
        redirect_url = reverse('elems-name', args=(elem,))
        html_elements += f'<li style="font-size:26px"> <a href={redirect_url} target="_blank"> {elem.title()} </a> </li>'
    response = f"""
    <ul>
    {html_elements}
    </ul>
    """
    return HttpResponse(response)


def get_info_about_elem_types(request, elem_type: str) -> HttpResponse:
    zodiacs = types_elems[elem_type]
    html_elements = ''
    for zodiac in zodiacs:
        redirect_url = reverse('horoscope-name', args=(zodiac,))
        html_elements += f'<li style="font-size:26px"> <a href={redirect_url} target="_blank"> {zodiac.title()} </a> </li>'
    response = f"""
        <ul>
        {html_elements}
        </ul>
        """
    return HttpResponse(response)


def get_info_by_date(request, month, day):
    my_date = ZodiacDay(f'{month}/{day}')
    zodiac = my_date.date_to_zodiac()
    if zodiac in signs:
        body = signs[zodiac]
    else:
        body = zodiac
    return HttpResponse(f'<p style="font-size:34px"> {body} </p>')


def get_yyyy_converters(request, sign_zodiac):
    return HttpResponse(f'Вы передали число из 4х цифр - {sign_zodiac}')


def get_my_float_converters(request, sign_zodiac):
    return HttpResponse(f'Вы передали вещественное число - {sign_zodiac}')


def get_my_date_converters(request, sign_zodiac):
    return HttpResponse(f'Вы передали дату - {sign_zodiac}')
