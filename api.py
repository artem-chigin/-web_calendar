import sys
import os
from datetime import date

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'

parser = reqparse.RequestParser()
url_parser = reqparse.RequestParser()

parser.add_argument('event', type=str, help="The event name is required!", required=True)
parser.add_argument('date', type=inputs.date,
                    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                    required=True)
url_parser.add_argument("start_time", type=inputs.date, required=False, location='args')
url_parser.add_argument("end_time", type=inputs.date, required=False, location='args')


class Calendar(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db_path = os.path.join("/", "calendar.db")
if not os.access(db_path, os.F_OK):
    db.create_all()


class EventToday(Resource):
    def get(self):
        result = []
        today = date.today()
        from_db = Calendar.query.filter(Calendar.date == today).all()
        for entry in from_db:
            entry_date = str(entry.date)
            info = {"id": entry.id, "event": entry.event, "date": entry_date}
            result.append(info)

        return result


class Event(Resource):
    def get(self):
        result = []
        args = url_parser.parse_args()
        if args["start_time"] is not None and args["end_time"] is not None:
            from_db = Calendar.query.filter(Calendar.date >= args["start_time"], Calendar.date <= args["end_time"]).all()
            for entry in from_db:
                entry_date = str(entry.date)
                info = {"id": entry.id, "event": entry.event, "date": entry_date}
                result.append(info)
            return result
        else:
            from_db = Calendar.query.all()
            for entry in from_db:
                entry_date = str(entry.date)
                info = {"id": entry.id, "event": entry.event, "date": entry_date}
                result.append(info)
            return result

    def post(self):
        data = parser.parse_args()
        d = data["date"]
        response_date = date.strftime(data["date"], "%Y-%m-%d")
        event = data["event"]
        msg = {"message": "The event has been added!", "event": event, "date": response_date}
        new_entry = Calendar(event=event, date=d)
        db.session.add(new_entry)
        db.session.commit()
        return msg


class EventByID(Resource):
    def get(self, event_id):
        from_db = Calendar.query.filter(Calendar.id == event_id).first()
        if from_db is None:
            abort(404, "The event doesn't exist!")
        else:
            return {"id": from_db.id, "event": from_db.event, "date": str(from_db.date)}

    def delete(self, event_id):
        event = Calendar.query.filter(Calendar.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        else:
            db.session.delete(event)
            db.session.commit()
            return {"message": "The event has been deleted!"}


api.add_resource(EventToday, "/event/today")
api.add_resource(Event, "/event")
api.add_resource(EventByID, '/event/<int:event_id>')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
