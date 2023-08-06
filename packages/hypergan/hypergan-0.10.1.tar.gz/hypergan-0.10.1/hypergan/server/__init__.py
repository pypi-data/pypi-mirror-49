"""
Web server for hypergan


"""

from hypergan.server.flask_server import FlaskServer


def gan_server(gan):
    return FlaskServer(gan)
