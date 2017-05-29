from django import forms

from app.models import AppUser, Product, Category


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    repassword = forms.CharField(widget=forms.PasswordInput, required=False)
    type_choices = (('C', 'Comprador'), ('VF', 'Vendedor Fijo'), ('VA', 'Vendedor Ambulante'))
    user_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'multiple'}),
                                  choices=type_choices, required=False)
    name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'dropify'}))
    payment = forms.MultipleChoiceField(choices=[],
                                        widget=forms.SelectMultiple(attrs={'class': 'multiple'}), required=False)
    t_init = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    t_finish = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = AppUser
        # email.widget.attrs.update({'class': 'validate', 'placeholder': 'email'})


class AddProductForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), required=False)
    name = forms.CharField(max_length=255, required=True)
    price = forms.IntegerField(min_value=0, required=True)
    stock = forms.IntegerField(min_value=0, required=True)
    des = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'dropify'}))

    class Meta:
        model = Product


class EditVendorForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'dropify'}))
    choices = []
    payment = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'multiple'}),
                                        choices=choices, required=False)
    t_init = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    t_finish = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

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
