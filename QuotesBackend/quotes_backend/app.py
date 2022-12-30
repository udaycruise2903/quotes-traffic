from flask import Flask


def create_app():
    application = Flask(__name__)
    
    return application