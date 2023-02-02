from django.urls import path, register_converter
from . import views as views_horoscope, converters

my_converters = [
    (converters.FourDigitYearConverter, 'yyyy'),
    (converters.MyFloatConverter, 'my_float'),
    (converters.MyDateConverter, 'my_date')
]

for converter, name_converter in my_converters:
    register_converter(converter, name_converter)

urlpatterns = [
    path('', views_horoscope.index, name='horoscope-home'),
    path('<my_date:sign_zodiac>/', views_horoscope.get_my_date_converters),
    path('<yyyy:sign_zodiac>/', views_horoscope.get_yyyy_converters),
    path('<int:sign_zodiac>/', views_horoscope.get_info_about_sign_zodiac_by_num),
    path('<my_float:sign_zodiac>/', views_horoscope.get_my_float_converters),
    path('<str:sign_zodiac>/', views_horoscope.get_info_about_sign_zodiac, name='horoscope-name'),
    path('type', views_horoscope.index_type),
    path('type/<str:elem_type>', views_horoscope.get_info_about_elem_types, name='elems-name'),
    path('<int:month>/<int:day>/', views_horoscope.get_info_by_date)
]
