from app.database import get_connection


def test_database_connection():
    connection = get_connection()

    assert connection.is_connected()

    connection.close()