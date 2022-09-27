# from flask import Flask
# from flask_restful import Resource, Api, reqparse
#
# app = Flask('main')
# api = Api(app)
#
# parser = reqparse.RequestParser()
# parser.add_argument('Writing', type=str, help='This is what You will see on The Wall', location='args')
#
#
# class HelloArgs(Resource):
#     def get(self):
#         data = parser.parse_args()
#         return {'data_from_url': data}
#
# # z
# api.add_resource(HelloArgs, '/')
#
# app.run()
