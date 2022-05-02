import os
import sys
from pymongo import MongoClient


class BaseConfig:

    DEBUG = True
    RESTPLUS_VALIDATE = True
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False
    JWT_SECRET_KEY = "SECRET_KEY"

    try:
        # Connecting MongoDB
        MONGO_URI = os.getenv("MONGO_URI")
        client = MongoClient(MONGO_URI)

        DB = client["dafiti"]
    except Exception as e:
        print(e)
        sys.exit()


class ProdConfig(BaseConfig):

    DEBUG = False


class DevConfig(BaseConfig):

    pass
