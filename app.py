from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
from api.ml.model import ml_blueprint


# ml route
app = Flask(__name__)
CORS(app, support_credentials=True)

app.register_blueprint(ml_blueprint)

@cross_origin(supports_credentials=True)
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
