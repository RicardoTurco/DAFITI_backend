import json


base_url = "http://localhost:5000/api/v1/tipo-transacoes"


class TestTipoTransacaoList:

    def test_can_get_all_tipo_transacoes(self, client):
        response = client.get(f"{base_url}")
        assert response.status_code == 200

    def test_return_list_get_all_tipo_transacoes(self, client):
        response = client.get(f"{base_url}")
        all_tipo_transacoes = json.loads(response.data)
        assert type(all_tipo_transacoes) == list


class TestTipoTransacaoNome:

    def test_can_get_tipo_transacao_by_nome(self, client):
        response = client.get(f"{base_url}/nome/Credito")
        assert response.status_code == 200

    def test_return_dict_get_tipo_transacao_by_nome(self, client):
        response = client.get(f"{base_url}/nome/Credito")
        all_tipo_contas = json.loads(response.data)
        assert type(all_tipo_contas) == dict


class TestTipoTransacaoId:

    def test_can_get_tipo_transacao_by_id(self, client):
        response = client.get(f"{base_url}/id/fbeeb4fe-6c65-4b4d-a7e4-7a27d36bfa48")
        assert response.status_code == 200

    def test_return_dict_get_tipo_transacao_by_id(self, client):
        response = client.get(f"{base_url}/id/fbeeb4fe-6c65-4b4d-a7e4-7a27d36bfa48")
        all_tipo_contas = json.loads(response.data)
        assert type(all_tipo_contas) == dict
