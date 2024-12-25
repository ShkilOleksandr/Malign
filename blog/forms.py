from django import forms
from django.contrib.auth import get_user_model
from .models import Creator

CustomUser = get_user_model()

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'avatar']

class CreatorForm(forms.ModelForm):
    # Include fields from CustomUser
    username = forms.CharField(max_length=150, required=False, label="Username")
    email = forms.EmailField(required=False, label="Email")
    avatar = forms.ImageField(required=False, label="Avatar")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Password")

    class Meta:
        model = Creator
        fields = ['bio', 'website']  # Fields specific to Creator

    def __init__(self, *args, **kwargs):
        # Get the 'user' instance from kwargs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Populate CustomUser fields if user is provided
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['avatar'].initial = self.user.avatar

    def save(self, commit=True):
        # Save Creator fields
        creator = super().save(commit=False)

        # Save CustomUser fields
        if self.user:
            if self.cleaned_data.get('username'):
                self.user.username = self.cleaned_data['username']
            if self.cleaned_data.get('email'):
                self.user.email = self.cleaned_data['email']
            if self.cleaned_data.get('avatar'):
                self.user.avatar = self.cleaned_data['avatar']
            if self.cleaned_data.get('password'):
                self.user.set_password(self.cleaned_data['password'])  # Hash the password

            if commit:
                self.user.save()

        if commit:
            creator.save()

        return creator