from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import FormView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views

from .forms import SignupForm, ProfileUpdateForm
from .models import Profile


class SignupView(FormView):

    template_name = 'users/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:registerok')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'users/logged_out.html'


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('users:profile')

    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form': form
    }

    return render(request, 'users/user_profile.html', context)

