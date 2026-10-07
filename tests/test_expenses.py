from app.main import app


def test_home_page(monkeypatch):
    app.config["TESTING"] = True

    monkeypatch.setattr(
        "app.main.get_all_expenses",
        lambda: []
    )

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200