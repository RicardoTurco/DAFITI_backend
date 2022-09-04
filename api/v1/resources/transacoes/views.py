import uuid
import datetime
from flask import current_app

from api.v1.resources.contas.views import set_contas, Contas
from api.v1.resources.tipo_transacoes.views import TipoTransacoes


# Conect to 'transacoes' collection in DB
def set_transacoes():
    db = current_app.config.get('DB', None)
    transacoes_ref = db['transacoes']
    return transacoes_ref


def date_in(date):
    dates = date.strftime("%d/%m/%Y")
    date_str = dates + ' 00:00:00'
    date_f = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
    return date_f


def delete_transacao(transacao):
    transacoes_ref = set_transacoes()

    transacoes_ref.delete_one({'_id': transacao['id']})

    conta = Contas.get_conta(id=transacao['idconta'])
    tipo_transacao = TipoTransacoes.get_tipo_transacao(id=transacao['idtipotransacao'])

    update_saldo_conta(conta,
                       tipo_transacao,
                       transacao['valor'],
                       'D')


def create_transacao_dict(transacao_dict):

    transacao = {}

    transacao['id'] = transacao_dict.pop('_id')

    tipo_transacao = TipoTransacoes.get_tipo_transacao(id=transacao_dict['idtipotransacao'])
    transacao['idtipotransacao'] = tipo_transacao['id']
    transacao['tipotransacao'] = tipo_transacao['tipotransacao']
    transacao['operacao'] = tipo_transacao['operacao']

    transacao['idconta'] = transacao_dict['idconta']
    transacao['valor'] = transacao_dict['valor']
    transacao['datatransacao'] = transacao_dict['datatransacao']

    return transacao


def update_saldo_conta(conta, tipo_transacao, valor, origin):
    """
    Param 'origin':

    Only can be ("I" or "D"). Defines how the 'saldo' of 'conta' will be adjusted.
    Any other option, the 'saldo' remain the same.
    """
    new_saldo = conta['saldo']
    if origin == 'I':
        if tipo_transacao['operacao'] == 'D':
            new_saldo = conta['saldo'] - valor
        elif tipo_transacao['operacao'] == 'C':
            new_saldo = conta['saldo'] + valor
    elif origin == 'D':
        if tipo_transacao['operacao'] == 'D':
            new_saldo = conta['saldo'] + valor
        elif tipo_transacao['operacao'] == 'C':
            new_saldo = conta['saldo'] - valor

    contas_ref = set_contas()
    to_change = {"saldo": new_saldo}
    contas_ref.update_one({"_id": conta['id']}, {'$set': to_change})


class Transacoes:

    def __init__(self):
        pass

    @staticmethod
    def get_all_transacoes():
        transacoes_ref = set_transacoes()

        all_transacoes = []
        for doc in transacoes_ref.find():
            transacao = create_transacao_dict(doc)
            all_transacoes.append(transacao)

        return all_transacoes

    @staticmethod
    def get_all_transacoes_params(**kwargs):
        transacoes_ref = set_transacoes()

        param_key = list(kwargs.keys())
        param_value = list(kwargs.values())

        key = "_id" if "id" in kwargs.keys() else param_key[0]
        value = kwargs["id"] if "id" in kwargs.keys() else param_value[0]

        all_transacoes = []
        for doc in transacoes_ref.find({key: value}, {}):
            transacao = create_transacao_dict(doc)
            all_transacoes.append(transacao)

        return all_transacoes

    @staticmethod
    def get_transacao(**kwargs):
        """
        Here, 'kwargs' receive just ONE key/value
        """
        transacoes_ref = set_transacoes()

        param_key = list(kwargs.keys())
        param_value = list(kwargs.values())

        key = "_id" if "id" in kwargs.keys() else param_key[0]
        value = kwargs["id"] if "id" in kwargs.keys() else param_value[0]

        transacao_ret = transacoes_ref.find_one({key: value}, {})

        transacao = {}
        if transacao_ret:
            transacao = create_transacao_dict(transacao_ret)

        return transacao

    @staticmethod
    def insert_transacao(conta, tipo_transacao, transacao):
        transacoes_ref = set_transacoes()

        try:

            transacao['idtransacao'] = str(uuid.uuid4())
            transacao['datatransacao'] = date_in(datetime.datetime.now())

            transacao_json = {
                "_id": transacao.get('idtransacao'),
                "idconta": transacao.get('idconta'),
                "idtipotransacao": transacao.get('idtipotransacao'),
                "valor": transacao.get('valor'),
                "datatransacao": transacao.get('datatransacao')
            }
            transacoes_ref.insert_one(transacao_json)

            update_saldo_conta(conta,
                               tipo_transacao,
                               transacao_json['valor'],
                               'I')

        except Exception as e:
            return f"An Error Occured: {e}"

    @staticmethod
    def delete_transacoes_conta(transacoes):
        for item in range(len(transacoes)):
            delete_transacao(transacoes[item])

    @staticmethod
    def delete_transacao(transacao):
        delete_transacao(transacao)
