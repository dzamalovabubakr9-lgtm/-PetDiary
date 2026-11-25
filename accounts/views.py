from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    PasswordResetCompleteView,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from accounts.forms import ProfileEditForm, RegistrationForm
from accounts.models import Profile, User


class HomeView(TemplateView):
    template_name = 'pages/home.html'


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно. Войдите в систему.')
        return response


class LoginViewCustom(LoginView):
    template_name = 'accounts/login.html'


class LogoutViewCustom(LogoutView):
    template_name = 'accounts/logout.html'

    def get_success_url(self):
        return reverse('home')


@login_required
def profile_detail(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile_detail.html', {'profile': profile})


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_edit.html'
    form_class = ProfileEditForm

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse('profile_detail')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Профиль успешно обновлён.')
        return redirect('profile_detail')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Пароль успешно изменён.')
            return render(request, 'accounts/change_password.html', {'form': form, 'changed': True})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


class PasswordResetViewCustom(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('reset_password_done')


class PasswordResetDoneViewCustom(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('reset_password_complete')


class PasswordResetCompleteViewCustom(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
