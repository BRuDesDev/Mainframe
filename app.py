from flask import Flask
from routes.api import api
from routes.pages import pages

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(pages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
