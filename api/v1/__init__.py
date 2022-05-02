from flask import Blueprint
from flask_restplus import Api


v1_blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(v1_blueprint,
          doc='/docs',
          title='API for DAFITI Test',
          version='1.0',
          description='API for DAFITI Test',
          security='Bearer Auth',
          authorizations=authorizations)


from .resources.tipo_contas.tipo_conta import api as tipo_contas_ns


api.add_namespace(tipo_contas_ns)
