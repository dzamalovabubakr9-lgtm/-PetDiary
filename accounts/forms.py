from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile, User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'birthday', 'about', 'avatar')


    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = User.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.user_id)
        if qs.exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return email

    def save(self, commit=True):
        profile = super().save(commit)
        if self.cleaned_data.get('email'):
            User.objects.filter(pk=profile.user_id).update(email=self.cleaned_data['email'])
        return profile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['email'].initial = self.instance.user.email
