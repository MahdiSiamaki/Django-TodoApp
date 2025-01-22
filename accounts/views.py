from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = "username","password"
    success_url = reverse_lazy('todo:todo_list')
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
    
    def get_next_page(self):
        next_page = super().get_next_page()
        return next_page or self.next_page

class UserSignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return response