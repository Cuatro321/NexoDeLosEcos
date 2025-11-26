import pytest

# 🔧 AJUSTA RUTAS A TUS PÁGINAS REALES
URLS_USABILIDAD = [
    "/",
    "/accounts/login/",
]

@pytest.mark.django_db
@pytest.mark.usability
def test_html_tiene_lang(client):
    """
    Verifica que el <html> tenga atributo lang (ej. <html lang="es">).
    """
    response = client.get("/", follow=True)
    assert response.status_code < 500
    html = response.content.decode("utf-8").lower()

    assert "<html" in html
    assert 'lang="' in html

@pytest.mark.django_db
@pytest.mark.usability
@pytest.mark.parametrize("path", URLS_USABILIDAD)
def test_paginas_tienen_title_y_h1(client, path):
    """
    Verifica que las páginas importantes tengan <title> y al menos un <h1>.
    """
    response = client.get(path, follow=True)
    assert response.status_code < 500
    html = response.content.decode("utf-8").lower()

    assert "<title>" in html
    assert "<h1" in html

@pytest.mark.django_db
@pytest.mark.usability
@pytest.mark.parametrize("path", URLS_USABILIDAD)
def test_imagenes_tienen_alt_o_aria(client, path):
    """
    Si hay imágenes, comprueba que exista algún 'alt=' o 'aria-label'.
    (No es perfecto, pero ayuda a detectar problemas de accesibilidad.)
    """
    response = client.get(path, follow=True)
    assert response.status_code < 500
    html = response.content.decode("utf-8").lower()

    if "<img" in html:
        assert ('alt="' in html) or ("aria-label" in html)
