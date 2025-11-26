import pytest

# 🔧 AJUSTA ESTAS RUTAS A TU SITIO REAL
URLS_BÁSICAS = [
    "/",                   # home
    "/accounts/login/",    # login
    "/news/",              # noticias (si no la tienes, bórrala)
    "/community/",         # comunidad (si no la tienes, bórrala)
]

@pytest.mark.django_db
@pytest.mark.performance
@pytest.mark.parametrize("path", URLS_BÁSICAS)
def test_rendimiento_endpoints_basicos(benchmark, client, path):
    """
    Mide el tiempo de respuesta de tus páginas clave.
    Usa pytest-benchmark para ver tiempos medios, máx, mín, etc.
    """

    def fetch():
        response = client.get(path, follow=True)
        # Para rendimiento solo exigimos que no haya error 5xx
        assert response.status_code < 500

    benchmark(fetch)
