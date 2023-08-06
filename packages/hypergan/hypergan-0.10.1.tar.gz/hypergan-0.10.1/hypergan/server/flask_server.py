"""
Flask server for hosting a model


routes:

    GET /
    GET /g/:id returns a sample with the associated id
    GET /d/:url runs the discriminator on the target url and returns the result
    GET /model returns model information
    GET /model.json returns model configuration

"""
class FlaskServer():
    def __init__(self, gan):
        self.gan = gan

        from flask import Flask
        app = Flask("HyperGAN")
        @app.route("/")
        def index():
            return "<h1>HyperGAN</h1> web server is running"
        @app.route("/g/<string:id>")
        def g(id):
            return "g placeholder"
        @app.route("/d/<string:url>")
        def d(url):
            return "d placeholder"
        @app.route("/model")
        def model(url):
            return "model placeholder"
        @app.route("/model.json")
        def modeljson():
            return gan.config
        app.run()
        print("Creating server")


