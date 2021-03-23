from flask import Flask, render_template, request, redirect, url_for
from main import main
app = Flask(__name__)

from flask_restful import Resource, Api
from api import Password
api = Api(app)
api.add_resource(Password, '/api/<password>')

def getApp():
    return app

if __name__ == '__main__':
    app.run()