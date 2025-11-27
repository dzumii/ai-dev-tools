from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Todo


def todo_list(request):
    """Display all todos"""
    todos = Todo.objects.all()
    return render(request, 'todos/home.html', {'todos': todos})


def create_todo(request):
    """Create a new todo"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date') or None
        
        if title:
            Todo.objects.create(
                title=title,
                description=description,
                due_date=due_date
            )
            messages.success(request, 'Todo created successfully!')
        else:
            messages.error(request, 'Title is required!')
        
        return redirect('todo_list')
    
    return render(request, 'todos/create_todo.html')


def edit_todo(request, pk):
    """Edit a todo"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        todo.due_date = due_date if due_date else None
        
        if todo.title:
            todo.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Title is required!')
    
    return render(request, 'todos/edit_todo.html', {'todo': todo})


@require_http_methods(["POST"])
def delete_todo(request, pk):
    """Delete a todo"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    messages.success(request, 'Todo deleted successfully!')
    return redirect('todo_list')


@require_http_methods(["POST"])
def resolve_todo(request, pk):
    """Mark a todo as completed"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.resolve()
    messages.success(request, 'Todo marked as completed!')
    return redirect('todo_list')


@require_http_methods(["POST"])
def unresolve_todo(request, pk):
    """Mark a todo as incomplete"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.unresolve()
    messages.success(request, 'Todo marked as incomplete!')
    return redirect('todo_list')
