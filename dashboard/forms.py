from django import forms
from .models import Address
from django.core.exceptions import ValidationError
from accounts.models import Profile


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'full_address', 'city', 'province', 'postal_code', 'receiver_name', 'phone_number',
                  'is_default']
        widgets = {
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError("عنوان آدرس باید حداقل 3 کاراکتر باشد.")
        if len(title) > 100:
            raise ValidationError("عنوان آدرس باید حداکثر 100 کاراکتر باشد.")
        return title

    def clean_full_address(self):
        full_address = self.cleaned_data.get('full_address')
        if len(full_address) < 10:
            raise ValidationError("آدرس باید حداقل 10 کاراکتر باشد.")
        if len(full_address) > 300:
            raise ValidationError("آدرس باید حداکثر 300 کاراکتر باشد.")
        return full_address

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if len(city) < 2:
            raise ValidationError("شهر باید حداقل 2 کاراکتر باشد.")
        if len(city) > 50:
            raise ValidationError("شهر باید حداکثر 50 کاراکتر باشد.")
        return city

    def clean_province(self):
        province = self.cleaned_data.get('province')
        if len(province) < 2:
            raise ValidationError("استان باید حداقل 2 کاراکتر باشد.")
        if len(province) > 50:
            raise ValidationError("استان باید حداکثر 50 کاراکتر باشد.")
        return province

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if len(postal_code) != 10:
            raise ValidationError("کد پستی باید 10 رقم باشد.")
        if not postal_code.isdigit():
            raise ValidationError("کد پستی باید فقط شامل اعداد باشد.")
        return postal_code

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.startswith('09'):
            raise ValidationError("شماره تلفن باید با 09 شروع شود.")
        if len(phone_number) != 11:
            raise ValidationError("شماره تلفن باید 11 رقم باشد.")
        return phone_number

    def clean_receiver_name(self):
        receiver_name = self.cleaned_data.get('receiver_name')
        if len(receiver_name.split()) < 2:
            raise ValidationError("لطفا نام و نام خانوادگی تحویل گیرنده را وارد کنید.")
        return receiver_name


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'about_me', 'phone', 'card_number', 'image']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 100:
            raise ValidationError("نام باید حداکثر 100 کاراکتر باشد.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 100:
            raise ValidationError("نام خانوادگی باید حداکثر 100 کاراکتر باشد.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("لطفاً یک ایمیل معتبر با دامنه @gmail.com وارد کنید.")
        if len(email) < 15:
            raise ValidationError("ایمیل باید حداقل 15 کاراکتر باشد.")
        if len(email) > 100:
            raise ValidationError("ایمیل باید حداکثر 100 کاراکتر باشد.")
        return email

    def clean_about_me(self):
        about_me = self.cleaned_data.get('about_me')
        if len(about_me) > 250:
            raise ValidationError("متن درباره من باید حداکثر 250 کاراکتر باشد.")
        return about_me

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('09'):
            raise ValidationError("شماره تلفن باید با 09 شروع شود.")
        if len(phone) != 11:
            raise ValidationError("شماره تلفن باید 11 رقم باشد.")
        return phone

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if len(card_number) != 16:
            raise ValidationError("شماره کارت باید 16 رقم باشد.")
        if not card_number.isdigit():
            raise ValidationError("شماره کارت باید فقط شامل اعداد باشد.")
        return card_number
