from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    

class Name(Resource):
    def post(self, name):
        return {'name': name}

api.add_resource(HelloWorld, '/')
api.add_resource(Name, '/name/<name>')

if __name__ == '__main__':
    app.run(debug=True)