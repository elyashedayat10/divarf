from django import forms
from django.contrib.auth.forms import PasswordChangeForm, ReadOnlyPasswordHashField
from django.core.validators import ValidationError

from .models import User


class CreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone_number",)

    def clean(self):
        clean_data = super(CreationForm, self).clean()
        password, password_confirm = (
            clean_data["password"],
            clean_data["password_confirm"],
        )
        if (password & password_confirm) and (password != password_confirm):
            raise ValidationError("un match password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("phone_number",)


class AuthForm(forms.Form):
    phone_number = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={"placeholder": "", "class": "form-control text-left"}
        ),
    )

    password = forms.CharField(
        label="رمز عبوز",
        widget=forms.PasswordInput(
            attrs={"placeholder": "رمز عبور", "class": "form-control text-left"}
        ),
    )

    # class Meta:
    #     model = User
    #     fields = ("phone_number", "password")
    #     labels = {
    #         "phone_number": "نام کاربری",
    #         "password": "رمز عبور",
    #     }
    #     widgets = {
    #         "phone_number": forms.TextInput(
    #             attrs={"placeholder": "", "class": "form-control text-left"}
    #         ),
    #         "password": forms.PasswordInput(
    #             attrs={"placeholder": "رمز عبوز", "class": "form-control text-left"}
    #         ),
    #     }


class AdminPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].lable = ""
        self.fields["new_password1"].lable = ""
        self.fields["new_password1"].lable = ""

        for fieldname in ["new_password1", "new_password2", "old_password"]:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs["class"] = "form-control"


class AdminForm(AuthForm):
    password_confirm = forms.CharField(
        label="نایید رمز عبور",
        widget=forms.PasswordInput(
            attrs={"placeholder": "تایید  رمز عبوز", "class": "form-control text-left"}
        ),
    )

    def clean(self):
        clean_data = super(AdminForm, self).clean()
        password, password_confirm = (
            clean_data["password"],
            clean_data["password_confirm"],
        )
        if (password and password_confirm) and (password != password_confirm):
            raise ValidationError("dis match")
