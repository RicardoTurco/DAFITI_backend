import json


base_url = "http://localhost:5000/api/v1/transacoes"


class TestTransacaoLIst:

    def test_can_get_all_transacoes(self, client):
        response = client.get(f"{base_url}")
        assert response.status_code == 200

    def test_return_list_get_all_transacoes(self, client):
        response = client.get(f"{base_url}")
        all_transacoes = json.loads(response.data)
        assert type(all_transacoes) == list


class TestTransacaoConta:

    def test_can_get_all_trasacoes_of_conta(self, client):
        response = client.get(f"{base_url}/conta/76572c00-9691-483f-ad1b-38c983d7f3c8")
        assert response.status_code == 200

    def test_return_list_all_transacoes_of_conta(self, client):
        response = client.get(f"{base_url}/conta/76572c00-9691-483f-ad1b-38c983d7f3c8")
        all_transacoes = json.loads(response.data)
        assert type(all_transacoes) == list


class TestTransacaoId:

    def test_can_get_transacao_by_id(self, client):
        response = client.get(f"{base_url}/id/196d53a2-6e13-4006-b3d6-99f4ab4337f4")
        assert response.status_code == 200

    def test_return_dict_transacao_by_id(self, client):
        response = client.get(f"{base_url}/id/196d53a2-6e13-4006-b3d6-99f4ab4337f4")
        conta = json.loads(response.data)
        assert type(conta) == dict

    def test_return_when_transacao_not_exists(self, client):
        response = client.get(f"{base_url}/id/196d53a2-6e13-4006-b3d6-99f4ab4337g5")
        assert response.status_code == 404

    def test_msg_when_transacao_not_exists(self, client):
        message = "Transacao not found"
        response_ret = client.get(f"{base_url}/id/196d53a2-6e13-4006-b3d6-99f4ab4337g5")
        response = json.loads(response_ret.data)
        assert response["message"] == message
