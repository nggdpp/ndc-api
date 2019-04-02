from flask import request
from flask_restplus import Namespace, Resource, reqparse
import pynggdpp.rest_api
from functools import wraps
import os


api = Namespace(
    "items",
    description="Items in the National Digital Catalog are descriptors of physical artifacts from "
                "collections (e.g., scientific samples, 'paper' records, physical specimens, etc.). Items "
                "may include geospatial coordinates making them searchable spatially and mappable. Item "
                "information schemas vary somewhat across the catalog depending on source. This API route "
                "provides various tools for searching and interacting with items in the catalog."
)


def token_required(f):
    @wraps(f)

    def decorated(*args, **kwargs):
        token = None

        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if not token or token != os.environ["API_TOKEN"]:
            return {"message": "A token is required for some routes due to potential for server load "
                               "limits to be exceeded, causing issues for everyone else. Once we move "
                               "the API to a production platform, restrictions will be lifted. A token "
                               "for this experimental API can be obtained by contacting sbristol@usgs.gov."}, 401

        print(f'TOKEN: {token}')

        return f(*args, **kwargs)

    return decorated


rest_mongo = pynggdpp.rest_api.Mongo()

query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'q',
    type=str,
    help='Optional query string (Lucene syntax) to search',
    default="*"
)


@api.route('/v0.1/search')
class QueryItems(Resource):
    @api.doc(parser=query_parser, security="apikey")
    @token_required
    def get(self):
        args = query_parser.parse_args()
        q_response = rest_mongo.query_items(q=args["q"])
        return q_response

@api.route('/v0.1/search/<ndc_collection_id>')
@api.param('ndc_collection_id', 'ScienceBase Identifier for the collection')
class QueryItemsInCollection(Resource):
    @api.doc(parser=query_parser)
    def get(self, ndc_collection_id):
        args = query_parser.parse_args()
        q_response = rest_mongo.query_items(ndc_collection_id=ndc_collection_id, q=args["q"])
        return q_response

