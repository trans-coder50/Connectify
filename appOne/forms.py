from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class UserSearch(forms.ModelForm):
    class Meta:
        model = User
        fields = []

    def filter_results(self, search_q):
        if search_q:
            return User.objects.filter(username__contains=search_q)
        else:
            return User.objects.none()
