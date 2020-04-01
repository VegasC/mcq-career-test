from api.ml.model import ml_blueprint
from flask import Flask
from flask import jsonify, make_response


# ml route
app = Flask(__name__)
app.register_blueprint(ml_blueprint)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
