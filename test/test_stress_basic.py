import pytest

# 🔧 AJUSTA RUTAS A TU SITIO
URLS_STRESS = [
    "/",
    "/accounts/login/",
]

NUM_PETICIONES = 100  # súbelo si quieres más estrés

@pytest.mark.django_db
@pytest.mark.stress
@pytest.mark.parametrize("path", URLS_STRESS)
def test_stress_multiples_peticioness(client, path):
    """
    Simula varias peticiones seguidas a una misma ruta.
    No es una prueba de carga profesional, pero sirve como smoke test de estrés.
    """
    for _ in range(NUM_PETICIONES):
        response = client.get(path, follow=True)
        assert response.status_code < 500
