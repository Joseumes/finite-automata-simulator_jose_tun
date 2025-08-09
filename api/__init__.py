from flask import Flask 

def create_app():
    app= Flask(__name__)
    app.config['jSON_SORT_KEYS'] = False
    app.config['GENERATE_DIT'] = 'generd_diagram'
    return app

