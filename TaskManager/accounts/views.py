from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render

from TaskManager.accounts.forms import CreateUserForm, ChangeUserPasswordForm

UserModel = get_user_model()


class HomePage(views.ListView):
    model = UserModel
    template_name = 'list_users.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'


class CreateUserView(views.CreateView):
    template_name = 'accounts/profile-create.html'
    form_class = CreateUserForm

    success_url = reverse_lazy('home page')


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('home page')


class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile-details.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        # self.request.user is logged now user
        context['is_general_manager'] = self.request.user.is_general_manager

        return context


class EditUserView(views.UpdateView):
    template_name = 'accounts/profile-edit.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email', 'role', 'level', 'is_general_manager',)

    def get_success_url(self):
        return reverse_lazy(
            'profile-view user',
            kwargs={'pk': self.object.pk})


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/profile-edit.html'
    form_class = ChangeUserPasswordForm
    model = UserModel

    def get_success_url(self):
        return reverse_lazy(
            'profile-view user',
            kwargs={'pk': self.request.user.pk})


class DeleteUserView(views.DeleteView):
    template_name = 'accounts/profile-delete.html'
    model = UserModel
    success_url = reverse_lazy('home page')
