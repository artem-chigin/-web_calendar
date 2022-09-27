import sys
from datetime import date

from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

parser.add_argument('event', type=str, help="The event name is required!", required=True)
parser.add_argument('date', type=inputs.date,
                    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                    required=True)


class Event(Resource):
    def get(self):
        return {"data": "There are no events for today!"}

    def post(self):
        data = parser.parse_args()
        data["date"] = date.strftime(data["date"], "%Y-%M-%d")
        msg = {"message": "The event has been added!"}
        msg.update(data)
        return msg


api.add_resource(Event, "/event")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
