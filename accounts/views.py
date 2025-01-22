from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = "username","password"
    success_url = reverse_lazy('todo:todo_list')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todo:todo_list')
        return super(UserLoginView, self).get(*args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
    
    def get_next_page(self):
        next_page = super().get_next_page()
        return next_page or self.next_page

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

class UserSignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignupView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todo:todo_list')
        return super(UserSignupView, self).get(*args, **kwargs)