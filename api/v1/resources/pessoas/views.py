import uuid
import datetime
from flask import current_app
from api.helpers import encrypt_password


# Conect to 'pessoas' collection in DB
def set_pessoas():
    db = current_app.config.get('DB', None)
    pessoas_ref = db['pessoas']
    return pessoas_ref


def date_in(date):
    date_str = date + ' 00:00:00'
    date_f = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
    return date_f


def exist_pessoa(username, cpf):
    pessoas_ref = set_pessoas()

    pessoa = pessoas_ref.find_one({'username': username, 'cpf': cpf}, {})
    if pessoa:
        return True
    return False


def create_pessoa_dict(pessoa_dict, is_inserting=False):

    pessoa = {}

    if is_inserting:
        pessoa['_id'] = pessoa_dict.pop('idpessoa')
    else:
        pessoa['id'] = pessoa_dict.pop('_id')

    pessoa['nome'] = pessoa_dict['nome']
    pessoa['cpf'] = pessoa_dict['cpf']
    pessoa['datanascimento'] = pessoa_dict['datanascimento']
    pessoa['username'] = pessoa_dict['username']
    pessoa['email'] = pessoa_dict['email']
    pessoa['password'] = pessoa_dict['password']

    return pessoa


class Pessoas:

    def __init__(self):
        pass

    @staticmethod
    def get_all_pessoas():
        pessoas_ref = set_pessoas()

        all_pessoas = []
        for doc in pessoas_ref.find():
            pessoa = create_pessoa_dict(doc)
            all_pessoas.append(pessoa)

        return all_pessoas

    @staticmethod
    def insert_pessoa(pessoa):
        pessoas_ref = set_pessoas()

        try:
            pessoa['idpessoa'] = str(uuid.uuid4())
            pessoa['password'] = encrypt_password(pessoa.get('password', 'changeme'))
            pessoa['datanascimento'] = date_in(pessoa.get('datanascimento'))

            pessoa_json = create_pessoa_dict(pessoa, True)

            pessoas_ref.insert_one(pessoa_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def get_pessoa(**kwargs):
        """
        Here, 'kwargs' receive just ONE key/value
        """
        pessoas_ref = set_pessoas()

        param_key = list(kwargs.keys())
        param_value = list(kwargs.values())

        key = "_id" if "id" in kwargs.keys() else param_key[0]
        value = kwargs["id"] if "id" in kwargs.keys() else param_value[0]

        pessoa_ret = pessoas_ref.find_one({key: value}, {})

        pessoa = {}
        if pessoa_ret:
            pessoa = create_pessoa_dict(pessoa_ret)

        return pessoa

    @staticmethod
    def delete_pessoa(id):
        pessoas_ref = set_pessoas()

        pessoas_ref.delete_one({'_id': id})

    @staticmethod
    def update_pessoa(id, pessoa):
        pessoas_ref = set_pessoas()

        try:

            pessoa['datanascimento'] = date_in(pessoa.get('datanascimento'))

            to_change = {
                'nome': pessoa.get('nome'),
                'cpf': pessoa.get('cpf'),
                'datanascimento': pessoa.get('datanascimento'),
                'username': pessoa.get('username'),
                'email': pessoa.get('email')
            }

            pessoas_ref.update_one({"_id": id}, {'$set': to_change})

        except Exception as e:
            return f"An Error Ocurred: {e}"
