from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
# from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from PIL import Image
from django.forms import fields
from .models import CustomUser, Investisseur


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_superuser', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserCreationForm2(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """Cette class permet de modifier les informations de l'utilisateur"""
    class Meta:
        model = CustomUser
        fields = ('email',)


class ChangeUserType(forms.ModelForm):
    """Cette calss permet de modifier leet de deactiver le compte"""
    class Meta:
        model = CustomUser
        fields = ('is_active',)


class PasswordChangeFormEdit(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Votre ancien mot de passe'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Votre nouveau mot de passe'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'confirmer votre mot de passe '})


class InvestisseurForm(forms.ModelForm):

    class Meta:
        model = Investisseur
        fields = ("prenom", "nom", "telephone", "adresse", "cni", "user",)


class UpdateInvestisseurForm(forms.ModelForm):

    class Meta:
        model = Investisseur
        fields = ("prenom", "nom", "adresse", "telephone", "user",)
