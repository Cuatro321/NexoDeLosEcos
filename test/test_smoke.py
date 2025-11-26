import pytest

@pytest.mark.django_db
def test_django_carga(settings):
    """Comprueba que Django y settings se cargan correctamente."""
    assert "django.contrib.auth" in settings.INSTALLED_APPS

@pytest.mark.django_db
def test_home_responde(client):
    """
    Comprueba que la página principal responde sin error de servidor.
    Ajusta la URL si tu home no está en "/".
    """
    response = client.get("/", follow=True)
    assert response.status_code < 500
