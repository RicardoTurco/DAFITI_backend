import uuid
from flask import current_app


# Conect to 'tipo_contas' collection in DB
def set_tipo_contas():
    db = current_app.config.get('DB', None)
    tipo_contas_ref = db['tipo_contas']
    return tipo_contas_ref


class TipoContas:

    def __init__(self):
        pass

    @staticmethod
    def get_all_tipo_contas():
        tipo_contas_ref = set_tipo_contas()

        all_tipo_contas = []
        for doc in tipo_contas_ref.find():
            dc = {}
            dc['id'] = doc.pop('_id')
            dc['tipoconta'] = doc['tipoconta']
            all_tipo_contas.append(dc)

        return all_tipo_contas

    @staticmethod
    def insert_tipo_conta(tipo_conta):
        tipo_contas_ref = set_tipo_contas()

        try:
            tipo_conta['idtipoconta'] = str(uuid.uuid4())

            tipo_conta_json = {
                "_id": tipo_conta.get('idtipoconta'),
                "tipoconta": tipo_conta.get('tipoconta')
            }

            tipo_contas_ref.insert_one(tipo_conta_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def get_tipo_conta(**kwargs):
        tipo_contas_ref = set_tipo_contas()

        key = "_id" if "id" in kwargs.keys() else "tipoconta"
        value = kwargs["id"] if "id" in kwargs.keys() else kwargs["nome_tipo_conta"]

        tipo_conta_ret = tipo_contas_ref.find_one({key: value}, {})

        tipo_conta = {}
        if tipo_conta_ret:
            tipo_conta['id'] = tipo_conta_ret.pop('_id')
            tipo_conta['tipoconta'] = tipo_conta_ret['tipoconta']

        return tipo_conta

    @staticmethod
    def delete_tipo_conta(id):
        tipo_contas_ref = set_tipo_contas()

        tipo_contas_ref.delete_one({'_id': id})

    @staticmethod
    def update_tipo_conta(id, tipo_conta):
        tipo_contas_ref = set_tipo_contas()

        try:

            tipo_contas_ref.update_one({"_id": id}, {'$set': {'tipoconta': tipo_conta.get('tipoconta')}})

        except Exception as e:
            return f"An Error Ocurred: {e}"
