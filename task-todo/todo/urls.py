# todo/urls.py
from django.urls import path
from todo.views import todo_list, todo_info

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('<int:todo_id>/', todo_info, name='todo_info'),
]
