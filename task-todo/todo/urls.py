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
    # CBV
    path('cbv/', TodoListView.as_view(), name='cbv_todo_list'),
    path('cbv/<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_info'),
    path('cbv/create/', TodoCreateView.as_view(), name='cbv_todo_create'),
    path('cbv/<int:pk>/update/', TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('cbv/<int:pk>/delete/', TodoDeleteView.as_view(), name='cbv_todo_delete'),

    # Comment CBV
    path('cbv/<int:todo_id>/comment/create/', CommentCreateView.as_view(), name='cbv_comment_create'),
    path('cbv/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='cbv_comment_update'),
    path('cbv/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='cbv_comment_delete'),
]
