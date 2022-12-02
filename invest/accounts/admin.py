from django.contrib import admin
from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import *
# # Register your models here.


class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('__str__', 'email',  'date_inscription',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email',)
    ordering = ('date_inscription',)
    readonly_fields = ('id', 'date_inscription', 'last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Informations Personnels ', {'fields': ('profile_image',)}),
        ('Permissions', {'fields': ('is_active',
         'is_admin', 'is_staff', 'is_superuser')}),
    )
    # ordering =
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', ),
        }),
    )


admin.site.register(CustomUser, AccountAdmin)
admin.site.register(Investisseur)


# # admin.site.register(Mairie)
# # admin.site.register(Profil)
# # admin.site.register(Activite)

# # unregister the Group model from admin.
# admin.site.unregister(Group)
