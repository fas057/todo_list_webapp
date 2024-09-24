from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task = Task.objects.create(title=title)
            return JsonResponse({'status': 'success', 'task_id': task.id, 'title': task.title})
        return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


def task_list(request):
    status = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_order = request.GET.get('sort_order', 'asc')
    search = request.GET.get('search', '').lower()

    if status == 'completed':
        tasks = Task.objects.filter(completed=True)
    elif status == 'not_completed':
        tasks = Task.objects.filter(completed=False)
    else:
        tasks = Task.objects.all()

    if search:
        tasks = [task for task in tasks if search in task.title.lower()]

    if sort_by == 'created_at':
        tasks = sorted(tasks, key=lambda task: task.created_at, reverse=(sort_order == 'desc'))
    elif sort_by == 'completed':
        tasks = sorted(tasks, key=lambda task: (task.completed, task.created_at), reverse=(sort_order == 'desc'))

    return render(request, 'todo/task_list.html', {'tasks': tasks})

def search_tasks(request):
    search = request.GET.get('search', '').lower()
    tasks = Task.objects.all()
    tasks = [task for task in tasks if search in task.title.lower()]
    task_list = [{'id': task.id, 'title': task.title, 'completed': task.completed, 'created_at': task.created_at.strftime("%d.%m.%Y %H:%M")} for task in tasks]
    return JsonResponse({'tasks': task_list})

def task_update(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = request.POST.get('completed') == 'true'
        task.save()
        return JsonResponse({'status': 'success', 'completed': task.completed})
    return JsonResponse({'status': 'error'})


def task_delete(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def task_edit(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        new_title = request.POST.get('title')
        if new_title:
            task.title = new_title
            task.save()
            return JsonResponse({'status': 'success', 'title': task.title})
        return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})