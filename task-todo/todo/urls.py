# todo/urls.py
from django.urls import path
from todo.views import todo_list, todo_info
from todo.cb_views import (
    TodoListView,
    TodoDetailView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
)

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('<int:todo_id>/', todo_info, name='todo_info'),

    # CBV
    path('cbv/', TodoListView.as_view(), name='cbv_todo_list'),
    path('cbv/<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_info'),
    path('cbv/create/', TodoCreateView.as_view(), name='cbv_todo_create'),
    path('cbv/<int:pk>/update/', TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('cbv/<int:pk>/delete/', TodoDeleteView.as_view(), name='cbv_todo_delete'),
]
