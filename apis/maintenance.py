from flask import request
from flask_restplus import Namespace, Resource, reqparse
import pynggdpp.rest_api


api = Namespace(
    "maintenance",
    description="This API route provides a number of tools for reporting on the status of "
                "operations within the National Digital Catalog infrastructure"
)


rest_search = pynggdpp.rest_api.Search()
rest_maintenance = pynggdpp.rest_api.Maintenance()

query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'q',
    type=str,
    help='Optional query string (Lucene syntax) to search',
    default="*"
)


@api.route('/v0.1/queues')
class ListQueues(Resource):
    @api.doc(security="apikey")
    def get(self):
        queue_list = list()
        for queue_url in rest_maintenance.list_queues():
            queue_name = queue_url.split("/")[-1]
            this_queue = {
                "QueueUrl": queue_url,
                "CheckQueue": f"{request.base_url.replace('queues','queue')}/{queue_name}"
            }
            queue_list.append(this_queue)
        return queue_list


@api.route('/v0.1/queue/<queue_name>')
@api.param('queue_name', 'Name of queue to poll for messages')
class QueueActions(Resource):
    def get(self, queue_name):
        response = {
            "queue_name": queue_name,
            "messages": rest_maintenance.check_messages(queue_name)
        }
        return response


@api.route('/v0.1/processing_logs')
class ProcessingLogsSearch(Resource):
    @api.doc(parser=query_parser)
    def get(self):
        args = query_parser.parse_args()
        q_response = rest_search.index_search(index_name="processing_log", q=args["q"])
        return q_response
