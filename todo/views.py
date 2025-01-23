from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q

from todo.models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    """
    List all todos belonging to the current user
    """
    model = Todo
    template_name = 'todo/todo_list.html'
    ordering = ['-created_at']
    context_object_name = 'todos'
    paginate_by = 10

    def get_queryset(self):
        # Filter todos to show only those belonging to the current user
        queryset = Todo.objects.filter(user=self.request.user).order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset

    login_url = 'accounts:login'  # Redirect to login if user is not authenticated
    

class TodoDetailView(LoginRequiredMixin, DetailView):
    """
    Show details of a todo
    """
    model = Todo
    template_name = 'todo/todo_detail.html'
    context_object_name = 'todo'


class TodoCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new todo
    """
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'due_date', 'done']
    success_url = reverse_lazy('todo:todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a todo
    """
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'due_date', 'done']
    success_url = reverse_lazy('todo:todo_list')


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a todo
    """
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    success_url = reverse_lazy('todo:todo_list')
