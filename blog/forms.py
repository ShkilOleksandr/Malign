from django import forms
from django.contrib.auth import get_user_model
from .models import Creator

CustomUser = get_user_model()

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar']  # Include avatar and other user fields

class CreatorUpdateForm(forms.ModelForm):
    # Add fields from the CustomUser model
    username = forms.CharField(max_length=150, required=False, label='Login')
    avatar = forms.ImageField(required=False, label='Avatar')
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Password')

    class Meta:
        model = Creator
        fields = ['bio', 'website']  # Include Creator-specific fields

    def __init__(self, *args, **kwargs):
        # Extract the 'user' instance from the Creator model
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['avatar'].initial = user.avatar
            self.user = user  # Save the user instance for later use

    def save(self, commit=True):
        # Save Creator fields
        creator = super().save(commit=False)

        print(f"Saving Creator: {creator}")  # Debug Creator instance

        # Save CustomUser fields
        if hasattr(self, 'user'):
            if self.cleaned_data.get('username'):
                print(f"Updating username to: {self.cleaned_data['username']}")
                self.user.username = self.cleaned_data['username']
            if self.cleaned_data.get('avatar'):
                print(f"Updating avatar")
                self.user.avatar = self.cleaned_data['avatar']
            if self.cleaned_data.get('password'):
                print(f"Updating password")
                self.user.set_password(self.cleaned_data['password'])  # Use `set_password`

            if commit:
                self.user.save()  # Save the CustomUser instance
                print(f"CustomUser saved: {self.user}")

        if commit:
            creator.save()  # Save the Creator instance
            print(f"Creator saved: {creator}")

        return creator