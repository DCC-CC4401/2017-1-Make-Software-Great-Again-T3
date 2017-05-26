from django import forms

from app.models import AppUser, Vendor, Product


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = AppUser
        # email.widget.attrs.update({'class': 'validate', 'placeholder': 'email'})


class EditVendorForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'dropify'}))

    class Meta:
        model = AppUser


class EditProductForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    price = forms.IntegerField(min_value=0, required=False)
    stock = forms.IntegerField(min_value=0, required=False)
    des = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'dropify'}))

    class Meta:
        model = Product
