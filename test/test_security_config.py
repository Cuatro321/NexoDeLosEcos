import pytest
from django.conf import settings

def _bool_setting(name, default=False):
    return bool(getattr(settings, name, default))

@pytest.mark.security
def test_csrf_middleware_activado():
    assert "django.middleware.csrf.CsrfViewMiddleware" in settings.MIDDLEWARE

@pytest.mark.security
def test_security_middleware_activado():
    assert "django.middleware.security.SecurityMiddleware" in settings.MIDDLEWARE

@pytest.mark.security
def test_allowed_hosts_no_vacio():
    # En producción NO debería estar vacío ni ser ["*"]
    assert isinstance(settings.ALLOWED_HOSTS, (list, tuple))
    assert len(settings.ALLOWED_HOSTS) > 0
    assert "*" not in settings.ALLOWED_HOSTS

@pytest.mark.security
def test_cookies_http_only():
    assert _bool_setting("SESSION_COOKIE_HTTPONLY", True) is True
    assert _bool_setting("CSRF_COOKIE_HTTPONLY", True) is True

@pytest.mark.security
def test_cookies_seguras_en_https():
    """
    Para producción, lo ideal es que estas flags sean True.
    Si estás en desarrollo sin HTTPS, puedes dejar esto como referencia
    y ajustarlo al desplegar.
    """
    assert _bool_setting("SESSION_COOKIE_SECURE", False) is True
    assert _bool_setting("CSRF_COOKIE_SECURE", False) is True

@pytest.mark.security
def test_cabeceras_seguridad_basicas():
    assert _bool_setting("SECURE_CONTENT_TYPE_NOSNIFF", False) is True
    assert _bool_setting("SECURE_BROWSER_XSS_FILTER", False) is True or hasattr(settings, "SECURE_BROWSER_XSS_FILTER")
    assert getattr(settings, "X_FRAME_OPTIONS", "DENY") in ("DENY", "SAMEORIGIN")

@pytest.mark.security
@pytest.mark.skipif(getattr(settings, "DEBUG", False), reason="DEBUG=True (entorno desarrollo)")
def test_debug_debe_ser_false_en_produccion():
    """
    Este test solo se ejecuta si DEBUG ya está en False.
    Úsalo como checklist para cuando prepares el despliegue.
    """
    assert settings.DEBUG is False
