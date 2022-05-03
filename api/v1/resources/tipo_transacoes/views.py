import uuid
from flask import current_app


# Conect to 'tipo_transacoes' collection in DB
def set_tipo_transacoes():
    db = current_app.config.get('DB', None)
    tipo_transacoes_ref = db['tipo_transacoes']
    return tipo_transacoes_ref


class TipoTransacoes:
    
    def __init__(self):
        pass

    @staticmethod
    def get_all_tipo_transacoes():
        tipo_transacoes_ref = set_tipo_transacoes()

        all_tipo_transacoes = []
        for doc in tipo_transacoes_ref.find():
            dc = {}
            dc['id'] = doc.pop('_id')
            dc['tipotransacao'] = doc['tipotransacao']
            dc['operacao'] = doc['operacao']
            all_tipo_transacoes.append(dc)

        return all_tipo_transacoes

    @staticmethod
    def insert_tipo_transacao(tipo_transacao):
        tipo_transacoes_ref = set_tipo_transacoes()

        try:
            tipo_transacao['idtipotransacao'] = str(uuid.uuid4())

            tipo_transacao_json = {
                "_id": tipo_transacao.get('idtipotransacao'),
                "tipotransacao": tipo_transacao.get('tipotransacao'),
                "operacao": tipo_transacao.get('operacao')
            }

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
            tipo_transacao['id'] = tipo_transacao_ret.pop('_id')
            tipo_transacao['tipotransacao'] = tipo_transacao_ret['tipotransacao']
            tipo_transacao['operacao'] = tipo_transacao_ret['operacao']

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
