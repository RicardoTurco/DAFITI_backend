from flask_restplus import Resource, Namespace
from .serializers import tipo_conta, create_tipo_conta
from .views import TipoContas


api = Namespace("tipo-contas", "Tipo Contas Endpoint")


@api.route('')
class TipoContaList(Resource):

    @api.marshal_list_with(tipo_conta)
    @api.doc(responses={
        200: 'OK',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all tipo contas
        """
        return TipoContas.get_all_tipo_contas(), 200

    @api.expect(create_tipo_conta)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        409: 'Tipo Conta already exists',
        422: 'Cannot create tipo conta',
        500: 'Internal Server Error'})
    def post(self):
        """
        Creates a new tipo conta
        """
        tipo_conta_by_name = TipoContas.get_tipo_conta(nome_tipo_conta=api.payload.get('tipoconta'))
        if tipo_conta_by_name:
            api.abort(409, 'Tipo Conta already exists')

        TipoContas.insert_tipo_conta(api.payload)
        return {"msg": "Tipo Conta created."}, 201


@api.route('/nome/<string:nome>')
class TipoContaNome(Resource):

    @api.marshal_with(tipo_conta)
    @api.doc(responses={
        200: 'OK',
        404: 'Tipo Conta not found',
        500: 'Internal Server Error'
    }, params={'nome': 'Nome Tipo Conta'})
    def get(self, nome):
        """
        Get tipo conta by Nome
        """
        tipo_conta = TipoContas.get_tipo_conta(nome_tipo_conta=nome)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')
        return tipo_conta, 200


@api.route('/id/<string:id>')
class TipoContaId(Resource):

    @api.marshal_with(tipo_conta)
    @api.doc(responses={
        200: 'OK',
        404: 'Tipo Conta not found',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Conta ID'})
    def get(self, id):
        """
        Get tipo conta by ID
        """
        tipo_conta = TipoContas.get_tipo_conta(id=id)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')
        return tipo_conta, 200

    @api.doc(responses={
        200: 'OK',
        404: 'Tipo Conta not found',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Conta ID'})
    def delete(self, id):
        """
        Delete tipo conta by ID
        """
        tipo_conta = TipoContas.get_tipo_conta(id=id)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')

        TipoContas.delete_tipo_conta(id)
        return {"msg": "Tipo Conta deleted."}, 200

    @api.expect(create_tipo_conta)
    @api.doc(responses={
        200: 'OK',
        400: 'Input payload validation failed',
        404: 'Tipo Conta not found',
        422: 'No tipo conta updated',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Conta ID'})
    def put(self, id):
        """
        Updates the tipo conta
        """
        tipo_conta = TipoContas.get_tipo_conta(id=id)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')

        TipoContas.update_tipo_conta(id, api.payload)
        return {"msg": "Tipo Conta Updated."}, 200
