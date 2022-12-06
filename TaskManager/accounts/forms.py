from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class CreateUserForm(auth_forms.UserCreationForm):
    # placeholder 'username' is override in 'accounts/templatetags/placeholders' and applied with filter in template.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_object in self.fields.items():
            if '1' in field_name:
                field_object.widget.attrs['placeholder'] = 'password'
            elif '2' in field_name:
                field_object.widget.attrs['placeholder'] = 'repeat password'
            else:
                field_object.widget.attrs['placeholder'] = field_name

    class Meta:
        model = UserModel
        fields = ('username', 'email')
        field_classes = {'username': auth_forms.UsernameField}


class ChangeUserPasswordForm(auth_forms.PasswordChangeForm):
    pass


class EditUserForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        field_classes = {'username': auth_forms.UsernameField}
