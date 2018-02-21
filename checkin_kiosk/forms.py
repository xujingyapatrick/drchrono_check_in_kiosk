from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from checkin_kiosk.utils.constants import Gender, Ethnicity, Race
from checkin_kiosk.utils.local_api import get_appointment_by_checkin_form


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "username"}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "password"}
    ),
        required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError("Username not correct")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            raise forms.ValidationError("Password not correct")
        else:
            return password


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Username"}
    ))
    client_id = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Client id in drchrono.com: account->API->MyApp"}
    ))
    client_secret = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Client secret in drchrono.com: account->API->MyApp"}
    ))

    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Your password"}
    ))
    password2 = forms.CharField(required=True, label='Confirm password', widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Confirm password"}
    ))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password does not match")
        return data


class CheckinForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "first name"}
    ))
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "last name"}
    ))
    SSN = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "SSN: xxx-xx-xxxx"}
    ))

    def clean(self):
        appointment = get_appointment_by_checkin_form(self.cleaned_data)
        if not appointment:
            raise forms.ValidationError(
                'No appointment for %s %s today, please make sure you have filled information correctly.' % (
                self.cleaned_data.get('first_name'), self.cleaned_data.get('last_name')))
        return self.cleaned_data


class InformationForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "first name"}
    ))
    middle_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "middle name"}
    ))
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "last name"}
    ))

    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(
        attrs={
            "type": "date",
            "placeholder": "birth day"}
    ))
    gender = forms.ChoiceField(required=False, choices=(
        ('', 'Select'),
        (Gender.MALE, 'Male'),
        (Gender.FEMALE, 'Female'),
        (Gender.OTHER, 'Other')
    ))

    address = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "address"}
    ))
    city = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "city"}
    ))

    cell_phone = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "phone number"}
    ))

    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "email"}
    ))
    ethnicity = forms.ChoiceField(required=False, choices=(
        ('', 'Select'),
        (Ethnicity.HISPANIC, 'Hispanic'),
        (Ethnicity.NOT_HISPANIC, 'Not Hispanic'),
        (Ethnicity.DECLINED, 'Decline to answer')
    ))
    race = forms.ChoiceField(required=False, choices=(
        ('', 'Select'),
        (Race.INDIAN, 'Indian'),
        (Race.ASIAN, 'Asian'),
        (Race.BLACK, 'Black'),
        (Race.WHITE, 'White'),
        (Race.HAWAIIAN, 'hawaiian'),
        (Race.BLANK, 'Leave blank'),
        (Race.DECLINED, 'Decline to answer')
    ))

    emergency_contact_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "emergency contact name"}
    ))

    emergency_contact_phone = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "emergency contact phone"}
    ))

    emergency_contact_relation = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            "placeholder": "emergency contact relation"}
    ))

    def __init__(self, *args, **kwargs):
        super(InformationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
