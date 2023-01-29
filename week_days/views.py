from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.

body = '<h1>Day:</h1>' \
       '<li>Почистить зубы</li>' \
       '<li>Сделать расчет квантовых вычислений</li>'

days_dict = {
    'monday': body.replace('Day', 'Monday'),
    'tuesday': body.replace('Day', 'Tuesday'),
    'wednesday': body.replace('Day', 'Wednesday'),
    'thursday': body.replace('Day', 'Thursday'),
    'friday': body.replace('Day', 'Friday'),
    'saturday': body.replace('Day', 'Saturday'),
    'sunday': body.replace('Day', 'Sunday'),
}


def get_info_about_days(request, day: str) -> HttpResponse:
    if day in days_dict:
        return HttpResponse(days_dict[day])
    return HttpResponseNotFound(f'Unknown day - {day}')


def get_info_about_nums(request, day: int) -> HttpResponse:
    days = list(days_dict.keys())
    days_numbers = list(range(1, 8))
    if day in days_numbers:
        cur_day = days[day-1]
        redirect_url = reverse('todo_name', args=(cur_day, ))
        return HttpResponseRedirect(redirect_url)
    return HttpResponse(f'Wrong day number - {day}')
