import uuid
import datetime
from flask import current_app

from api.v1.resources.pessoas.views import Pessoas
from api.v1.resources.tipo_contas.views import TipoContas


# Conect to 'contas' collection in DB
def set_contas():
    db = current_app.config.get('DB', None)
    contas_ref = db['contas']
    return contas_ref


def date_in(date):
    dates = date.strftime("%d/%m/%Y")
    date_str = dates + ' 00:00:00'
    date_f = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
    return date_f


def exist_conta(idpessoa, idtipoconta):
    contas_ref = set_contas()

    conta = contas_ref.find_one({'idpessoa': idpessoa, 'idtipoconta': idtipoconta}, {})
    if conta:
        return True
    return False


def create_conta_dict(conta_dict):

    conta = {}

    conta['id'] = conta_dict.pop('_id')

    tipo_conta = TipoContas.get_tipo_conta(id=conta_dict['idtipoconta'])
    conta['tipoconta'] = tipo_conta['tipoconta']

    pessoa = Pessoas.get_pessoa(id=conta_dict['idpessoa'])
    conta['nome'] = pessoa['nome']

    conta['saldo'] = conta_dict['saldo']
    conta['limitesaquediario'] = conta_dict['limitesaquediario']
    conta['flagativo'] = conta_dict['flagativo']
    conta['datacriacao'] = conta_dict['datacriacao']

    return conta


class Contas:

    def __init__(self):
        pass

    @staticmethod
    def get_all_contas():
        contas_ref = set_contas()

        all_contas = []
        for doc in contas_ref.find():
            conta = create_conta_dict(doc)
            all_contas.append(conta)

        return all_contas

    @staticmethod
    def get_all_contas_params(**kwargs):
        contas_ref = set_contas()

        param_key = list(kwargs.keys())
        param_value = list(kwargs.values())

        key = "_id" if "id" in kwargs.keys() else param_key[0]
        value = kwargs["id"] if "id" in kwargs.keys() else param_value[0]

        all_contas = []
        for doc in contas_ref.find({key: value}, {}):
            conta = create_conta_dict(doc)
            all_contas.append(conta)

        return all_contas

    @staticmethod
    def get_conta(**kwargs):
        """
        Here, 'kwargs' receive just ONE key/value
        """
        contas_ref = set_contas()

        param_key = list(kwargs.keys())
        param_value = list(kwargs.values())

        key = "_id" if "id" in kwargs.keys() else param_key[0]
        value = kwargs["id"] if "id" in kwargs.keys() else param_value[0]

        conta_ret = contas_ref.find_one({key: value}, {})

        conta = {}
        if conta_ret:
            conta = create_conta_dict(conta_ret)

        return conta

    @staticmethod
    def insert_conta(conta):
        contas_ref = set_contas()

        try:
            conta['idconta'] = str(uuid.uuid4())
            conta['datacriacao'] = date_in(datetime.datetime.now())

            conta_json = {
                "_id": conta.get('idconta'),
                "idpessoa": conta.get('idpessoa'),
                "saldo": 0.00,
                "limitesaquediario": conta.get('limitesaquediario'),
                "idtipoconta": conta.get('idtipoconta'),
                "flagativo": True,
                "datacriacao": conta.get('datacriacao')
            }

            contas_ref.insert_one(conta_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def delete_conta(id):
        contas_ref = set_contas()

        contas_ref.delete_one({'_id': id})

    @staticmethod
    def update_conta_flagativo(id, flagativo):
        contas_ref = set_contas()

        try:

            to_change = {'flagativo': flagativo}
            contas_ref.update_one({"_id": id}, {'$set': to_change})

        except Exception as e:
            return f"An Error Ocurred: {e}"
