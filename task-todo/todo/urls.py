# todo/urls.py
from django.urls import path
from todo.views import todo_list, todo_info, todo_create, todo_update, todo_delete

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('create/', todo_create, name='todo_create'),
    path('<int:todo_id>/', todo_info, name='todo_info'),
    path('<int:todo_id>/update/', todo_update, name='todo_update'),
    path('<int:todo_id>/delete/', todo_delete, name='todo_delete'),
]
