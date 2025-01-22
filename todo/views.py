from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy

from todo.models import Todo


class TodoListView(ListView):
    model = Todo


class TodoDetailView(DetailView):
    model = Todo
    template_name = 'todo/todo_detail.html'
    context_object_name = 'todo'


class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'due_date', 'done']
    success_url = reverse_lazy('todo:todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'due_date', 'done']
    success_url = reverse_lazy('todo:todo_list')


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    success_url = reverse_lazy('todo:todo_list')