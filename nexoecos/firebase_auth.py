import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()

FIREBASE_REST_URL = "https://identitytoolkit.googleapis.com/v1"


class FirebaseError(Exception):
    """Error genérico para problemas al hablar con Firebase."""
    pass


def _firebase_request(endpoint: str, payload: dict) -> dict:
    api_key = getattr(settings, "FIREBASE_API_KEY", None)
    if not api_key:
        raise FirebaseError("FIREBASE_API_KEY no está configurada en settings.py")
    url = f"{FIREBASE_REST_URL}/{endpoint}?key={api_key}"
    resp = requests.post(url, json=payload, timeout=10)
    data = resp.json()
    if resp.status_code != 200:
        msg = data.get("error", {}).get("message", "Error en Firebase")
        raise FirebaseError(msg)
    return data


def firebase_sign_up(email: str, password: str) -> dict:
    """Crea un usuario email/password en Firebase Authentication."""
    return _firebase_request(
        "accounts:signUp",
        {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        },
    )


def firebase_sign_in(email: str, password: str) -> dict:
    """Inicia sesión email/password en Firebase Authentication."""
    return _firebase_request(
        "accounts:signInWithPassword",
        {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        },
    )


def get_or_create_local_user_from_firebase(email: str, username: str | None = None):
    """Sincroniza un usuario de Firebase con la tabla User de Django usando el email."""
    # 1) ¿Ya hay un usuario con ese correo en Django?
    user = User.objects.filter(email__iexact=email).first()
    if user:
        return user

    # 2) Crear uno nuevo si no existe
    base_username = (username or email.split("@")[0] or "user").replace(" ", "")[:30]
    new_username = base_username or "user"
    suffix = 1
    while User.objects.filter(username=new_username).exists():
        new_username = f"{base_username}_{suffix}"
        suffix += 1

    user = User.objects.create_user(
        username=new_username,
        email=email,
    )
    # No sabemos la contraseña local (la maneja Firebase), así que la marcamos como inutilizable
    user.set_unusable_password()
    user.save()
    return user


class FirebaseBackend(BaseBackend):
    """Backend de autenticación que valida contra Firebase usando email/password."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # El campo del form de login de Django se llama username,
        # pero puede contener correo o username.
        login_value = username or kwargs.get("email")
        if not login_value or not password:
            return None

        # Si el usuario escribe su correo, lo usamos tal cual.
        # Si escribe su username, intentamos resolver a un email.
        if "@" in login_value:
            email = login_value
            display_username = None
        else:
            existing = User.objects.filter(username=login_value).first()
            if existing and existing.email:
                email = existing.email
                display_username = existing.username
            else:
                # Último intento: tratar el valor como si fuera un correo
                email = login_value
                display_username = login_value

        try:
            firebase_sign_in(email=email, password=password)
        except FirebaseError:
            return None

        user = get_or_create_local_user_from_firebase(
            email=email,
            username=display_username,
        )
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
