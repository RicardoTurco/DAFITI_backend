import json


base_url = "http://localhost:5000/api/v1/pessoas"


class TestPessoaList:

    def test_can_get_all_pessoas(self, client):
        response = client.get(f"{base_url}")
        assert response.status_code == 200

    def test_return_list_get_all_pessoas(self, client):
        response = client.get(f"{base_url}")
        all_pessoas = json.loads(response.data)
        assert type(all_pessoas) == list


class TestPessoaUsername:

    def test_can_get_pessoa_by_username(self, client):
        response = client.get(f"{base_url}/username/ricturco")
        assert response.status_code == 200

    def test_return_dict_pessoa_by_username(self, client):
        response = client.get(f"{base_url}/username/ricturco")
        pessoa = json.loads(response.data)
        assert type(pessoa) == dict

    def test_return_when_pessoa_not_exists(self, client):
        response = client.get(f"{base_url}/username/XXXX")
        assert response.status_code == 404

    def test_msg_when_pessoa_not_exists(self, client):
        message = "Pessoa not found"
        response_ret = client.get(f"{base_url}/username/XXX")
        response = json.loads(response_ret.data)
        assert response["message"] == message


class TestPessoaCpf:

    def test_can_get_pessoa_by_cpf(self, client):
        response = client.get(f"{base_url}/cpf/77777777777")
        assert response.status_code == 200

    def test_return_dict_pessoa_by_username(self, client):
        response = client.get(f"{base_url}/cpf/77777777777")
        pessoa = json.loads(response.data)
        assert type(pessoa) == dict

    def test_return_when_pessoa_not_exists(self, client):
        response = client.get(f"{base_url}/cpf/12312312312")
        assert response.status_code == 404

    def test_msg_when_pessoa_not_exists(self, client):
        message = "Pessoa not found"
        response_ret = client.get(f"{base_url}/cpf/12312312312")
        response = json.loads(response_ret.data)
        assert response["message"] == message


class TestPessoaId:

    def test_can_get_pessoa_by_cpf(self, client):
        response = client.get(f"{base_url}/id/da0f2859-2de3-4e46-8017-37b0a3ce0e57")
        assert response.status_code == 200

    def test_return_dict_pessoa_by_username(self, client):
        response = client.get(f"{base_url}/id/da0f2859-2de3-4e46-8017-37b0a3ce0e57")
        pessoa = json.loads(response.data)
        assert type(pessoa) == dict

    def test_return_when_pessoa_not_exists(self, client):
        response = client.get(f"{base_url}/id/da0f2859-2de3-4e46-8017-37b0a3ce0e68")
        assert response.status_code == 404

    def test_msg_when_pessoa_not_exists(self, client):
        message = "Pessoa not found"
        response_ret = client.get(f"{base_url}/id/da0f2859-2de3-4e46-8017-37b0a3ce0e68")
        response = json.loads(response_ret.data)
        assert response["message"] == message
