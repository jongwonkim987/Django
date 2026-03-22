from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from todo.models import Todo

@login_required
def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).values_list('id', 'title')
    if request.user.is_superuser:
        todo_list = Todo.objects.all().values_list('id', 'title')
    result = []
    for todo in todo_list:
        result.append({'id': todo[0], 'title': todo[1]})

    return render(request, 'todo/todo_list.html', {'data': result})

@login_required
def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        if todo.user != request.user and not request.user.is_superuser:
            raise Http404("해당 To Do를 조회할 권한이 없습니다.")
        info = {
            'title': todo.title,
            'description': todo.description,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'is_completed': todo.is_completed,
        }
        return render(request, 'todo/todo_info.html', {'data': info})
    except Todo.DoesNotExist:
        raise Http404