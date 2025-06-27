from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.core.validators import EmailValidator


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input_second input_all', 'placeholder': 'نام'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input_second input_all', 'placeholder': 'نام خانوادگی'})
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input_second input_all', 'placeholder': 'نام کاربری'})
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input_second input_all', 'placeholder': 'ایمیل'}),
        validators=[EmailValidator(message="لطفا یک ایمیل معتبر وارد کنید.")]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input_second input_all', 'placeholder': 'رمز عبور'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 100:
            raise ValidationError("نام کاربری نمی ‌تواند بیشتر از 100 کاراکتر باشد.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("نام کاربری وارد شده از قبل وجود دارد.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) > 100:
            raise ValidationError("ایمیل نمی ‌تواند بیشتر از 100 کاراکتر باشد.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("ایمیل وارد شده از قبل وجود دارد.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد.")
        if len(password) > 20:
            raise ValidationError("رمز عبور نباید بیشتر از 20 کاراکتر باشد.")
        return password


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input_second input_all', 'placeholder': 'نام کاربری'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input_second input_all', 'placeholder': 'رمز عبور'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("نام کاربری یا رمز عبور نادرست است.", code='invalid_info')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input_second input_all', 'placeholder': 'رمز عبور فعلی'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input_second input_all', 'placeholder': 'رمز عبور جدید'})
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input_second input_all', 'placeholder': 'تکرار رمز عبور جدید'})
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) < 8:
            raise ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد.")
        if len(new_password) > 20:
            raise ValidationError("رمز عبور نباید بیشتر از 20 کاراکتر باشد.")
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise ValidationError("رمز عبور جدید و تکرار آن مطابقت ندارند.")
        return cleaned_data
