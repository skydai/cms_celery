from flask import Flask

from api import blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(5000))