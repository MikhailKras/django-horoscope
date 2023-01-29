from django.urls import path
from . import views as views_week_days

urlpatterns = [
    path('<int:day>/', views_week_days.get_info_about_nums),
    path('<str:day>/', views_week_days.get_info_about_days, name='todo_name'),
]
