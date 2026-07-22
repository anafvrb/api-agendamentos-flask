from app import app


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Agenda Médica" in response.get_data(as_text=True)


def test_invalid_login():
    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "email": "usuario@invalido.com",
            "password": "senha-errada"
        }
    )

    assert response.status_code == 200
    assert "Usuário ou senha inválidos" in response.get_data(as_text=True)


def test_appointments_api():
    client = app.test_client()

    response = client.get("/api/appointments")

    assert response.status_code == 200
    assert response.is_json

    dados = response.get_json()

    assert isinstance(dados, list)