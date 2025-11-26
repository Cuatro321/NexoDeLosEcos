# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••"})
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"class": "input", "placeholder": "Tu usuario"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "tucorreo@dominio.com"}),
        }

    def clean(self):
        data = super().clean()
        p1 = data.get("password1")
        p2 = data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "display_name",
            "gamer_tag",
            "bio",
            "country",
            "city",
            "favorite_domain",
            "avatar",
        )
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "input", "placeholder": "Nombre visible"}),
            "gamer_tag": forms.TextInput(attrs={"class": "input", "placeholder": "Tu gamer tag"}),
            "bio": forms.Textarea(attrs={"class": "textarea", "rows": 4, "placeholder": "Sobre ti..."}),
            "country": forms.TextInput(attrs={"class": "input", "placeholder": "País"}),
            "city": forms.TextInput(attrs={"class": "input", "placeholder": "Ciudad"}),
            "favorite_domain": forms.Select(attrs={"class": "select"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "file-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegura los choices desde el modelo (sin importar constantes externas)
        self.fields["favorite_domain"].choices = (
            Profile._meta.get_field("favorite_domain").choices or []
        )
