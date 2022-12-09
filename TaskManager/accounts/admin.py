from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from TaskManager.accounts.forms import CreateUserForm, EditUserForm

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'last_login', 'is_general_manager')
    list_filter = ('is_staff', 'is_superuser', 'is_general_manager',)
    ordering = ('email',)
    form = EditUserForm
    add_form = CreateUserForm

    fieldsets = (
        (None,
         {'fields': (
             'username',
             'password',
         )
         }
         ),
        ('Personal info',
         {'fields': (
             'first_name',
             'last_name',
             'email',
             'role',
             'level',
             'is_general_manager',
         )
         }
         ),
        ('Permissions',
         {'fields': (
             'is_active',
             'is_staff',
             'is_superuser',
             'groups',
             'user_permissions',
         ),
         },
         ),
        ('Important dates',
         {'fields': (
             'last_login',
             'date_joined',
         )
         }
         ),
    )
    readonly_fields = ('date_joined', "last_login")
