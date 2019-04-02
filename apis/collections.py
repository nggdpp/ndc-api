from flask import request
from flask_restplus import Namespace, Resource, Api, reqparse
import pynggdpp.rest_api


api = Namespace(
    "collections",
    description="Collections are the basic organizing feature of the National Digital Catalog. They "
                "are cataloged in ScienceBase as metadata items that present information about the "
                "collection and one or more routes to access the items within a collection. This API "
                "route provides tools for interacting with collections and reviewing their status."
)


rest_mongo = pynggdpp.rest_api.Mongo()

query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'q',
    type=str,
    help='Optional query string (Lucene syntax) to search',
    default="*"
)


@api.route('/v0.1/collections')
class Collections(Resource):
    @api.doc(parser=query_parser)
    def get(self):
        args = query_parser.parse_args()
        q_response = rest_mongo.query_collections(
            base_url=request.base_url,
            q=args["q"]
        )
        return q_response


@api.route('/v0.1/collection/<ndc_collection_id>')
@api.param('ndc_collection_id', 'ScienceBase Identifier for the collection')
class CollectionById(Resource):
    def get(self, ndc_collection_id):
        q_response = rest_mongo.query_collections(
            ndc_collection_id=ndc_collection_id,
            base_url=request.base_url
        )
        return q_response


@api.route('/v0.1/collections/files')
class CollectionFiles(Resource):
    def get(self):
        q_response = rest_mongo.query_files(
            base_url=request.base_url
        )
        return q_response


@api.route('/v0.1/collections/files/<ndc_collection_id>')
@api.param('ndc_collection_id', 'ScienceBase Identifier for the collection')
class CollectionFileReports(Resource):
    def get(self, ndc_collection_id):
        q_response = rest_mongo.query_files(
            ndc_collection_id=ndc_collection_id,
            base_url=request.base_url
        )
        return q_response


