# [DAFITI] Backend API
This project is the API for DAFITI test.  

## MongoDB

For data storage, the MongoDB database is used.

SUGESTION: `Up your MongoDB in a local container ...` 

![Alt text](imgs/entidades.png?raw=true)

## Installing

To install and execution the API in your local machine, you will need to:

```
git clone https://github.com/RicardoTurco/DAFITI_backend.git && cd DAFITI_backend

Checkout to DEVELOP branch
(git checkout develop)

Create and activate one "virtualenv"
(using any valid form) 

This next 2 steps are OPTIONAL, but HIGH recommended !!!
a) python -m pip install --upgrade pip
b) pip install -U setuptools

pip install -r requirements.txt

You need export one environment variable with a "conection string" to your MongoDB:
export MONGO_URI=mongodb://<user>:<password>@<your_host> 
(ex: MONGO_URI=mongodb://root:1234@localhost:27017/)

python run.py
```

## Swagger

After the application goes up, open your browser on `localhost:5000/api/v1/docs` to see the self-documented interactive API.

## Basic WorkFlow (using Postman)

```   
- Import DAFITI_backend.postman_collection.json in Postman to access the URLs and payloads;

- Create a "environment" and a "base_url" environment variable in this environment;

a) Create TIPO-CONTA;
(POST > http://127.0.0.1:5000/api/v1/tipo-contas)

b) Create TIPO-TRANSACAO;
(POST > http://127.0.0.1:5000/api/v1/tipo-transacoes)

c) Create a PESSOA;
(POST > http://127.0.0.1:5000/api/v1/pessoas)

d) Create CONTA to Pessoa;
(POST > http://127.0.0.1:5000/api/v1/contas)

g) Create TRANSACAO to Conta;
(POST > http://127.0.0.1:5000/api/v1/transacoes)
```


## Project Structure

The project structure is based on the official [Scaling your project](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-apis-with-reusable-namespaces) doc with some adaptations (e.g `v1` folder to agroup versioned resources).

```
.
├── api
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── parsers.py
│   │   └── password.py
│   └── v1
│   │   ├── __init__.py
│   │   └── resources
│   │       └── contas
│   │       │   ├── __init__.py
│   │       │   ├── conta.py
│   │       │   ├── serializers.py
│   │       │   └── views.py
│   │       └── pessoas
│   │       │   ├── __init__.py
│   │       │   ├── pessoa.py
│   │       │   ├── serializers.py
│   │       │   └── views.py
│   │       └── tipo_contas
│   │       │   ├── __init__.py
│   │       │   ├── serializers.py
│   │       │   ├── tipo_conta.py
│   │       │   └── views.py
│   │       └── tipo_transacoes
│   │       │   ├── __init__.py
│   │       │   ├── serializers.py
│   │       │   ├── tipo_transacao.py
│   │       │   └── views.py
│   │       └── transacoes
│   │       │   ├── __init__.py
│   │       │   ├── serializers.py
│   │       │   ├── transacao.py
│   │       │   └── views.py
│   │       ├── __init__.py
│   ├── __init__.py
├── imgs
│   ├── images files
├── .gitignore
├── config.py
├── DAFITI_backend.postman_collection.json
├── README.md
├── requirements.txt
├── run.py

```
### Folders

* `api` - All the RESTful API implementation is here.
* `api/helpers` - Useful function/class helpers for all modules.
* `api/v1` - Resource agroupment for all `v1` [Namespaces](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-namespaces).
* `api/v1/resources` - All `v1` resources are implemented here.
* `imgs` - All images files of API project/documentation.

### Files

* `api/__init__.py` - The Flask Application factory (`create_app()`) and it's configuration are done here. Your [Blueprints](https://flask-restplus.readthedocs.io/en/stable/scaling.html#use-with-blueprints) are registered here.
* `api/v1/__init__.py` - The Flask RESTPlus API is created here with the versioned Blueprint (e.g `v1`). Your [Namespaces](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-namespaces) are registered here.
* `.gitignore` - Lists files and directories which should not be added to git repository.
* `config.py` - Config file for envs, global config vars and so on. 
* `DAFITI_backend.postman_collection.json` - File to import in Postman.
* `README.md` - Instructions and informations of this "challenge".
* `requirements.txt` - All project dependencies.
* `run.py` - The Application entrypoint.

### API Versioning

If you need to create another API version (like `/api/v2`), follow these steps:

First, create your `v2` API structure folder:

```
mkdir api/v2
touch api/v2/__init__.py
```

Inside your `api/v2/__init__.py` create your Blueprint:

```
from flask import Blueprint
from flask_restplus import Api

v2_blueprint = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(v2_blueprint,
          doc='/docs',
          title='Flask App',
          version='2.0',
          description='Flask RESTful API V2')
```

Create your resources and namespaces inside `api/v2/resources` (like the `api/v1/resources`) and register them:

```
# api/v2/__init__.py

from flask import Blueprint
from flask_restplus import Api

v2_blueprint = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(v2_blueprint,
          doc='/docs',
          title='Flask App',
          version='2.0',
          description='Flask RESTful API V2')


# Fictious resource example
from .resources.auth.login import api as auth_ns
api.add_namespace(auth_ns)

```

And finally, register your Blueprint with the Flask Application:

```
# api/__init__.py

# config code...
from api.v1 import v1_blueprint
    api.register_blueprint(v1_blueprint)

from api.v2 import v2_blueprint
    api.register_blueprint(v2_blueprint)

```

Now you have your new endpoints with the base path `/api/v2` :) !

OBS: Your swagger docs for this new API version will be under this base path too. Ex: `localhost:5000/api/v2/docs`.

