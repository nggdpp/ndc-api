from flask import request
from flask_restplus import Api
from functools import wraps

#from .maintenance import api as ns_maintenance
from .collections import api as ns_collections
from .organizations import api as ns_organizations
from .items import api as ns_items

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY"
    }
}

api = Api(
    doc='/docs/',
    version="0.1",
    title="National Digital Catalog API",
    description="Application Programming Interface for the National Digital Catalog of Geological and Geophysical Data",
    authorizations=authorizations
)

#api.add_namespace(ns_maintenance)
api.add_namespace(ns_collections)
api.add_namespace(ns_organizations)
api.add_namespace(ns_items)
