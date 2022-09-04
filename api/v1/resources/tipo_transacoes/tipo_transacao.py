from flask_restplus import Resource, Namespace
from .serializers import tipo_transacao, create_tipo_transacao
from .views import TipoTransacoes


api = Namespace('tipo-transacoes', 'Tipo Transacoes Endpoint')


@api.route('')
class TipoTransacaoList(Resource):

    @api.marshal_list_with(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all tipo transacoes
        """
        return TipoTransacoes.get_all_tipo_transacoes(), 200

    @api.expect(create_tipo_transacao)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        409: 'Tipo Transacao already exists',
        422: 'Cannot create tipo transacao',
        500: 'Internal Server Error'})
    def post(self):
        """
        Creates a new tipo transacao
        """
        tipo_transacao_by_name = TipoTransacoes.get_tipo_transacao(nome_tipo_transacao=api.payload.get('tipotransacao'))
        if tipo_transacao_by_name:
            api.abort(409, 'Tipo Transacao already exists')

        TipoTransacoes.insert_tipo_transacao(api.payload)
        return {"msg": "Tipo Transacao created."}, 201


@api.route('/nome/<string:nome>')
class TipoTransacaoNome(Resource):

    @api.marshal_with(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        404: 'Tipo Transacao not found',
        500: 'Internal Server Error'
    }, params={'nome': 'Nome Tipo Transacao'})
    def get(self, nome):
        """
        Get tipo transacao by Nome
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao(nome_tipo_transacao=nome)
        if not tipo_transacao:
            api.abort(404, 'Tipo Transacao not found')
        return tipo_transacao, 200


@api.route('/id/<string:id>')
class TipoTransacaoId(Resource):

    @api.marshal_with(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        404: 'Tipo Transacao not found',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Transacao ID'})
    def get(self, id):
        """
        Get tipo transacao by ID
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao(id=id)
        if not tipo_transacao:
            api.abort(404, 'Tipo Transacao not found')
        return tipo_transacao, 200

    @api.doc(responses={
        200: 'OK',
        404: 'Tipo Transacao not found',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Transacao ID'})
    def delete(self, id):
        """
        Delete tipo transacao by ID
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao(id=id)
        if not tipo_transacao:
            api.abort(404, 'Tipo Transacao not found')

        TipoTransacoes.delete_tipo_transacao(id)
        return {"msg": "Tipo Transacao deleted."}, 200

    @api.expect(create_tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        400: 'Input payload validation failed',
        404: 'Tipo Transacao not found',
        422: 'No tipo transacao updated',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Transacao ID'})
    def put(self, id):
        """
        Updates the tipo transacao
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao(id=id)
        if not tipo_transacao:
            api.abort(404, 'Tipo Transacao not found')

        TipoTransacoes.update_tipo_transacao(id, api.payload)
        return {"msg": "Tipo Transacao Updated."}, 200
