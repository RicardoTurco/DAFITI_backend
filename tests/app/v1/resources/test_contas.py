import json


base_url = "http://localhost:5000/api/v1/contas"


class TestContaList:

    def test_can_get_all_contas(self, client):
        response = client.get(f"{base_url}")
        assert response.status_code == 200

    def test_return_list_get_all_contas(self, client):
        response = client.get(f"{base_url}")
        all_contas = json.loads(response.data)
        assert type(all_contas) == list


class TestContaIdpessoa:

    def test_can_get_all_contas_of_pessoa(self, client):
        response = client.get(f"{base_url}/idpessoa/da0f2859-2de3-4e46-8017-37b0a3ce0e57")
        assert response.status_code == 200

    def test_return_list_all_contas_of_pessoa(self, client):
        response = client.get(f"{base_url}/idpessoa/da0f2859-2de3-4e46-8017-37b0a3ce0e57")
        all_contas = json.loads(response.data)
        assert type(all_contas) == list

    def test_return_when_pessoa_not_exists(self, client):
        response = client.get(f"{base_url}/idpessoa/da0f2859-2de3-4e46-8017-37b0a3ce0e68")
        assert response.status_code == 404

    def test_msg_when_pessoa_not_exists(self, client):
        message = "Pessoa not have contas"
        response_ret = client.get(f"{base_url}/idpessoa/da0f2859-2de3-4e46-8017-37b0a3ce0e68")
        response = json.loads(response_ret.data)
        assert response["message"] == message


class TestContaId:

    def test_can_get_conta_by_id(self, client):
        response = client.get(f"{base_url}/id/76572c00-9691-483f-ad1b-38c983d7f3c8")
        assert response.status_code == 200

    def test_return_dict_conta_by_id(self, client):
        response = client.get(f"{base_url}/id/76572c00-9691-483f-ad1b-38c983d7f3c8")
        conta = json.loads(response.data)
        assert type(conta) == dict

    def test_return_when_conta_not_exists(self, client):
        response = client.get(f"{base_url}/id/76572c00-9691-483f-ad1b-38c983d7f3d9")
        assert response.status_code == 404

    def test_msg_when_conta_not_exists(self, client):
        message = "Conta not found"
        response_ret = client.get(f"{base_url}/id/76572c00-9691-483f-ad1b-38c983d7f3d9")
        response = json.loads(response_ret.data)
        assert response["message"] == message
