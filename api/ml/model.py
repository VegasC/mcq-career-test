import pickle
import os
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from flask import Blueprint, request, jsonify, abort
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

csv_dir = os.path.abspath('api/ml/csv_file')
pkfile_dir = os.path.abspath('api/ml/pk_file')

ml_blueprint = Blueprint('index', __name__)


@ml_blueprint.route('/api/v1/results', methods=['POST'])
def index():
    if not request.json:
        abort(404)

    # load correct answer from csv_file
    correct_answer = np.asarray(pd.DataFrame(pd.read_csv(
        os.path.join(csv_dir, 'mcq_data.csv'), encoding='utf-8', header=None)))
    correct_answer = correct_answer[1:, -1]

    # get user input and sort questions answered correctly only
    answered_correctly = list()
    for index, question in enumerate(request.get_json()['questions']):
        for questx, user_answer in question.items():
            if user_answer == correct_answer[index]:
                answered_correctly.append(questx)

    # convert correct answered list to np.array
    answered_correctly = np.array(answered_correctly)

    # load magic multinomialNB classifier model from pickel file
    model_path = os.path.join(
        pkfile_dir, 'Magic-MultinomialNB-99.0-Wed Mar 25 10:42:06 2020.pickel')

    with open(model_path, 'rb') as file:
        magicMultinomialNBClassifer = pickle.load(file)

    # predict correct answered department
    correct_answer_department_predictions = magicMultinomialNBClassifer.predict(
        answered_correctly)

    # load magic KMeanCluster model from pickel file
    model_path = os.path.join(
        pkfile_dir, 'Model-73.0-Wed Mar 25 10:49:06 2020.pickel')

    with open(model_path, 'rb') as file:
        magicKmeanCluster = pickle.load(file)

    # cluster correct answered questions into departments
    correct_answer_cluster_predictions = magicKmeanCluster.predict(
        answered_correctly)

    correct_answer_cluster_predictions_department = list()
    for correct_answer_cluster_prediction in correct_answer_cluster_predictions:
        if correct_answer_cluster_prediction == 2:
            correct_answer_cluster_predictions_department.append('computer')
        elif correct_answer_cluster_prediction == 1:
            correct_answer_cluster_predictions_department.append('mechanical')
        elif correct_answer_cluster_prediction == 0:
            correct_answer_cluster_predictions_department.append('electrical')

    correct_answer_cluster_predictions_department_counter = Counter(
        correct_answer_cluster_predictions_department)

    response = {
        "amount_of_questions_attend": len(request.get_json()['questions']),
        "amount_of_questions_answered_correctly": answered_correctly.shape[0],
        "precentage_of_answered_questions_(%)": round((answered_correctly.shape[0] / len(request.get_json()['questions'])) * 100, 2),
        "answered_correctly_departments": list(correct_answer_department_predictions),
        "mcq_career_test_prediction": dict(correct_answer_cluster_predictions_department_counter)
    }
    correct_answer_cluster_predictions_department_counter.clear()
    return jsonify({'response': response})
