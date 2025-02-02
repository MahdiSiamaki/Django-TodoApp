from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages


class UserLoginView(LoginView):
    """
    Login view for users to authenticate.
    """

    template_name = "accounts/login.html"
    fields = "username", "password"
    success_url = reverse_lazy("todo:todo_list")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:todo_list")
        return super(UserLoginView, self).get(*args, **kwargs)


class UserLogoutView(LogoutView):
    """
    Logout view for users to logout.
    """

    next_page = reverse_lazy("accounts:login")

    def get_next_page(self):
        next_page = super().get_next_page()
        return next_page or self.next_page

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class UserSignupView(CreateView):
    """
    Signup view for users to register
    """

    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignupView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:todo_list")
        return super(UserSignupView, self).get(*args, **kwargs)


class PasswordResetView(PasswordResetView):
    """
    View for initiating password reset.
    """

    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetDoneView(PasswordResetDoneView):
    """
    View for indicating that password reset email has been sent.
    """

    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    """
    View for confirming new password.
    """

    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(PasswordResetCompleteView):
    """
    View for indicating that password reset has been completed.
    """

    template_name = "accounts/password_reset_complete.html"
