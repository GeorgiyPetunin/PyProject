from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/api/v1/hello-world-22')
def hello_world():
    return 'Hello World 22 !'


serv = WSGIServer(('127.0.0.1', 5000), app)
serv.serve_forever()
