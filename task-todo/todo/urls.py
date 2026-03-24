# todo/urls.py
from django.urls import path
from todo.cb_views import (
    TodoListView,
    TodoDetailView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Todo CBV
    path('list/', TodoListView.as_view(), name='todo_list'),
    path('<int:pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('create/', TodoCreateView.as_view(), name='todo_create'),
    path('<int:pk>/update/', TodoUpdateView.as_view(), name='todo_update'),
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='todo_delete'),

    # Comment CBV
    path('comment/<int:todo_id>/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
