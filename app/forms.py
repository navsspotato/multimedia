from django import forms
from .models import User


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'full_name',
            'email',
            'role'
        ]

    # HIDE ADMIN OPTION IF ALREADY 2 ADMINS
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        admin_count = User.objects.filter(
            role='admin'
        ).count()

        # REMOVE ADMIN FROM DROPDOWN
        if admin_count >= 2:

            self.fields['role'].choices = [
                choice for choice in self.fields['role'].choices
                if choice[0] != 'admin'
            ]

    # CHECK PASSWORDS MATCH
    def clean(self):

        cleaned_data = super().clean()

        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:

            raise forms.ValidationError(
                "Passwords do not match!"
            )

        return cleaned_data

    # BACKEND SECURITY
    def clean_role(self):

        role = self.cleaned_data.get('role')

        admin_count = User.objects.filter(
            role='admin'
        ).count()

        if role == 'admin' and admin_count >= 2:

            raise forms.ValidationError(
                "Maximum number of admins reached."
            )

        return role