from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from todo.models import Todo


class TodoListView(ListView):
    model = Todo


class TodoDetailView(DetailView):
    pass

class TodoCreateView(CreateView):
    pass

class TodoUpdateView(UpdateView):
    pass

class TodoDeleteView(DeleteView):
    pass