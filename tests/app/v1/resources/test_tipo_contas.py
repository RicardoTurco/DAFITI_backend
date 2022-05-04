import json


base_url = "http://localhost:5000/api/v1/tipo-contas"


class TestTipoContaList:

    def test_can_get_all_tipo_contas(self, client):
        response = client.get(f"{base_url}")
        assert response.status_code == 200

    def test_return_list_get_all_tipo_contas(self, client):
        response = client.get(f"{base_url}")
        all_tipo_contas = json.loads(response.data)
        assert type(all_tipo_contas) == list


class TestTipoContaNome:

    def test_can_get_tipo_conta_by_nome(self, client):
        response = client.get(f"{base_url}/nome/Corrente")
        assert response.status_code == 200

    def test_return_dict_get_tipo_contas_by_nome(self, client):
        response = client.get(f"{base_url}/nome/Corrente")
        all_tipo_contas = json.loads(response.data)
        assert type(all_tipo_contas) == dict


class TestTipoContaId:

    def test_can_get_tipo_conta_by_id(self, client):
        response = client.get(f"{base_url}/id/29906c58-3ecd-4c4b-b926-3e0ffcb826d8")
        assert response.status_code == 200

    def test_return_dict_get_tipo_conta_by_id(self, client):
        response = client.get(f"{base_url}/id/29906c58-3ecd-4c4b-b926-3e0ffcb826d8")
        all_tipo_contas = json.loads(response.data)
        assert type(all_tipo_contas) == dict
