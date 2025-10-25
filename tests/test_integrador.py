import pytest
from src.integrador.main import app  # Si usas Flask

@pytest.fixture
def cliente():
    app.testing = True
    return app.test_client()

def test_pagina_principal(cliente):
    """Verifica que la app integradora (Flask) responde con 200."""
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
