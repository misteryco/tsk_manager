from django.contrib.auth import views as auth_views, mixins as auth_mixins, get_user_model, login
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import redirect, render
from TaskManager.accounts.forms import CreateUserForm, ChangeUserPasswordForm
from TaskManager.core.services.ses import SESService

UserModel = get_user_model()


def sign_up_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            SESService().send_email(user.email)
            login(request, user)
            return redirect('home page')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, template_name='accounts/login-page.html', context=context)


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'


# class CreateUserView(views.CreateView):
#     template_name = 'accounts/profile-create.html'
#     form_class = CreateUserForm
#
#     success_url = reverse_lazy('home page')
#
#     def post(self, request, *args, **kwargs):
#         form = CreateUserForm(self.request.POST)
#         if form.is_valid():
#             user = form.save()
#             SESService().send_email(user.email)
#             login(request, user)
#             return redirect('home page')
#         else:
#             form = CreateUserForm()
#         return super().post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     try:
    #         user = form.save()
    #     except Exception as ex:
    #         a = 5
    #     # Sending informational email for registration through AWS-SES service
    #     SESService().send_email(user.email)
    #     # !!! Not used for the moment !!!
    #     # SQS Services
    #     # SQSService().send_message(user.email)
    #     # !!! Not used for the moment !!!
    #     login(self.request, user)
    #     return redirect(self.success_url)


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('home page')


class UserDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'accounts/profile-details.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_pk = context.get('object').pk
        if not self.request.user.is_general_manager:
            if object_pk != self.request.user.pk:
                raise PermissionDenied()
        context['is_general_manager'] = self.request.user.is_general_manager
        context['approved'] = self.request.user.role
        return context


class EditUserView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'base/base-edit-view.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email', 'role', 'level', 'is_general_manager',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Profile'
        context['form__button_title'] = 'Save Changes'
        if not self.request.user.is_general_manager:
            raise PermissionDenied()
        return context

    def get_success_url(self):
        return reverse_lazy(
            'profile-view user',
            kwargs={'pk': self.object.pk})


class ChangeUserPasswordView(auth_views.PasswordChangeView, auth_mixins.UserPassesTestMixin):
    # template_name = 'accounts/profile-edit.html'
    template_name = 'base/base-edit-view.html'
    form_class = ChangeUserPasswordForm
    model = UserModel

    def get_success_url(self):
        return reverse_lazy(
            'profile-view user',
            kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Change Password'
        context['form__button_title'] = 'Save Changes'
        return context


class DeleteUserView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'accounts/profile-delete.html'
    model = UserModel
    success_url = reverse_lazy('home page')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
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
