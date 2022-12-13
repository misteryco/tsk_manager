from django.contrib.auth import views as auth_views, mixins as auth_mixins, get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import redirect
from TaskManager.accounts.forms import CreateUserForm, ChangeUserPasswordForm
from TaskManager.services.ses import SESService
from TaskManager.services.sqs import SQSService

UserModel = get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'


class CreateUserView(views.CreateView):
    template_name = 'accounts/profile-create.html'
    form_class = CreateUserForm

    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        user = form.save()
        # Sending email with AWS-SES service
        SESService().send_email(user.email)
        # SQS Services
        SQSService().send_message(user.email)
        login(self.request, user)
        return redirect(self.success_url)


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('home page')


class UserDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'accounts/profile-details.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_general_manager:
            raise PermissionDenied()
        context['is_general_manager'] = self.request.user.is_general_manager
        context['approved'] = self.request.user.role
        return context


class EditUserView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'accounts/profile-edit.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email', 'role', 'level', 'is_general_manager',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_general_manager:
            raise PermissionDenied()
        return context

    def get_success_url(self):
        return reverse_lazy(
            'profile-view user',
            kwargs={'pk': self.object.pk})


class ChangeUserPasswordView(auth_views.PasswordChangeView, UserPassesTestMixin):
    template_name = 'accounts/profile-edit.html'
    form_class = ChangeUserPasswordForm
    model = UserModel

    def get_success_url(self):
        return reverse_lazy(
            'profile-view user',
            kwargs={'pk': self.request.user.pk})


class DeleteUserView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'accounts/profile-delete.html'
    model = UserModel
    success_url = reverse_lazy('home page')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not self.request.user.is_general_manager:
            raise PermissionDenied()
        return context


class ManageSubordinatesView(views.ListView):
    model = UserModel
    template_name = 'accounts/manage_subordinates.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not self.request.user.is_general_manager:
            raise PermissionDenied()
        context['subordinates_to_add'] = self.model.objects. \
            exclude(level='junior'). \
            exclude(level='team_lead'). \
            exclude(level='senior')
        context['subordinates_to_manage'] = self.model.objects.all()
        return context
