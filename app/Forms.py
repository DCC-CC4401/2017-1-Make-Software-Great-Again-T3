from django import forms

from app.models import AppUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = AppUser
        # email.widget.attrs.update({'class': 'validate', 'placeholder': 'email'})
