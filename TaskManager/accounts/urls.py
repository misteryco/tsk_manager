from django.urls import path, include

from TaskManager.accounts.views import SignInView, CreateUserView, SignOutView, UserDetailsView, EditUserView, \
    DeleteUserView, ChangeUserPasswordView

urlpatterns = [
    path('login/', SignInView.as_view(), name='login user'),
    path('register/', CreateUserView.as_view(), name='register user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='profile-view user'),
        path('edit/', EditUserView.as_view(), name='profile-edit user'),
        path('edit-pwd/', ChangeUserPasswordView.as_view(), name='password-edit user'),
        path('delete/', DeleteUserView.as_view(), name='profile-delete user'),
    ])),
]
