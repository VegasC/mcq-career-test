from flask import Blueprint
from flask import Flask
from flask import request, jsonify, abort
import ast


ml_blueprint = Blueprint('index', __name__)


@ml_blueprint.route('/api/v1/results', methods=['POST'])
def index():
    if not request.json:
        abort(404)

    questions = [dict(x) for x in ast.literal_eval(
        request.get_json()['questions'])]

    for question in questions:
        for key in question:
            print(key, question[key])

    return jsonify({'greet': 'Hello World'})

    # print(request.get_json()['questions'][0])
