import uuid
from flask import current_app


# Conect to 'tipo_transacoes' collection in DB
def set_tipo_transacoes():
    db = current_app.config.get('DB', None)
    tipo_transacoes_ref = db['tipo_transacoes']
    return tipo_transacoes_ref


def create_tipo_transacao_dict(tipo_transacao_dict, is_inserting=False):

    tipo_transacao = {}

    if is_inserting:
        tipo_transacao['_id'] = tipo_transacao_dict.pop('idtipotransacao')
    else:
        tipo_transacao['id'] = tipo_transacao_dict.pop('_id')

    tipo_transacao['tipotransacao'] = tipo_transacao_dict['tipotransacao']
    tipo_transacao['operacao'] = tipo_transacao_dict['operacao']

    return tipo_transacao


class TipoTransacoes:
    
    def __init__(self):
        pass

    @staticmethod
    def get_all_tipo_transacoes():
        tipo_transacoes_ref = set_tipo_transacoes()

        all_tipo_transacoes = []
        for doc in tipo_transacoes_ref.find():
            tipo_transacao = create_tipo_transacao_dict(doc)
            all_tipo_transacoes.append(tipo_transacao)

        return all_tipo_transacoes

    @staticmethod
    def insert_tipo_transacao(tipo_transacao):
        tipo_transacoes_ref = set_tipo_transacoes()

        try:
            tipo_transacao['idtipotransacao'] = str(uuid.uuid4())

            tipo_transacao_json = create_tipo_transacao_dict(tipo_transacao, True)

            tipo_transacoes_ref.insert_one(tipo_transacao_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def get_tipo_transacao(**kwargs):
        tipo_transacoes_ref = set_tipo_transacoes()

        key = "_id" if "id" in kwargs.keys() else "tipotransacao"
        value = kwargs["id"] if "id" in kwargs.keys() else kwargs["nome_tipo_transacao"]

        tipo_transacao_ret = tipo_transacoes_ref.find_one({key: value}, {})

        tipo_transacao = {}
        if tipo_transacao_ret:
            tipo_transacao = create_tipo_transacao_dict(tipo_transacao_ret)

        return tipo_transacao

    @staticmethod
    def delete_tipo_transacao(id):
        tipo_transacoes_ref = set_tipo_transacoes()

        tipo_transacoes_ref.delete_one({'_id': id})

    @staticmethod
    def update_tipo_transacao(id, tipo_transacao):
        tipo_transacoes_ref = set_tipo_transacoes()

        try:

            to_change = {'tipotransacao': tipo_transacao.get('tipotransacao'),
                         'operacao': tipo_transacao.get('operacao')}

            tipo_transacoes_ref.update_one({"_id": id}, {'$set': to_change})

        except Exception as e:
            return f"An Error Ocurred: {e}"
