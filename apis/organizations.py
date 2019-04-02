from flask import request
from flask_restplus import Namespace, Resource, Api, reqparse
import pynggdpp.rest_api


api = Namespace(
    "organizations",
    description="Organizations are the State Geological Survey, USGS, and other contributors to the "
                "National Digital Catalog. Tools in this area are used to explore organizations and "
                "their contributions and current status."
)


rest_mongo = pynggdpp.rest_api.Mongo()

query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'q',
    type=str,
    help='Optional query string (Lucene syntax) to search',
    default="*"
)


@api.route('/v0.1/organizations')
class Organizations(Resource):
    def get(self):
        q_response = rest_mongo.query_organizations(
            base_url=request.base_url
        )
        return q_response

