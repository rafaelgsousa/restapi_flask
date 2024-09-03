import pytest

from app import create_app
from config import MockConfig


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app(MockConfig)
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
                "name": "Rafael",
                "nickname": "Full-stack",
                "age": 34,
                "cpf": "253.845.920-60",
                "email": "elderrafaelgomes@gmail.com"
            }

    @pytest.fixture
    def invalid_user(self):
        return {
                "name": "Rafael",
                "nickname": "Full-stack",
                "age": 34,
                "cpf": "253.845.920-61",
                "email": "elderrafaelgomes@gmail.com"
            }

    def test_get_users(self, client):
        response = client.get('/devops')
        assert response.status_code == 200

    def test_create_user(self, client, valid_user):
        response = client.post('/devops', json=valid_user)
        assert response.status_code == 201
        assert valid_user["name"] in response.json["message"]

    def test_create_user_with_invalid_cpf(self, client, invalid_user):
        response = client.post('/devops', json=invalid_user)
        assert response.status_code == 400
        assert "CPF is invalid!" == response.json["message"]

    def test_get_user_by_cpf(self, client, valid_user):
        response = client.get(f'/devops/{valid_user['cpf']}')
        assert response.status_code == 200
        assert valid_user['cpf'] == response.json[0]['cpf']
