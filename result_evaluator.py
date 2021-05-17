#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 15/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

import numpy as np
from pyspark.ml.evaluation import BinaryClassificationEvaluator


def get_all_metrics(predictions):
    """Given the prediction get a dictionary of metrics
    :param
        predictions: the output prediction of classifier.classify()
    :return:
        a dictionary of metrics
    """
    true_positive = predictions[(predictions.label == 1) & (predictions.prediction == 1)].count()
    false_positive = predictions[(predictions.label == 0) & (predictions.prediction == 1)].count()
    true_negative = predictions[(predictions.label == 0) & (predictions.prediction == 0)].count()
    false_negative = predictions[(predictions.label == 1) & (predictions.prediction == 0)].count()

    return {
        "confusion_matrix": np.array([[true_positive, false_positive], [false_negative, true_negative]]),
        "precision": true_positive / (true_positive + false_positive),
        "recall": true_positive / (true_positive + false_negative),
        "accuracy": (true_positive + true_negative) / (true_positive + false_positive + false_negative + true_negative),
        "f-measure": (2 * true_positive) / (2 * true_positive + false_positive + false_negative)
    }


def get_evaluator_result(predictions):
    """Evaluate the prediction using the BinaryClassification evaluator
    :param
        predictions: the output prediction of classifier.classify()
    :return:
        the evaluator score
    """
    evaluator = BinaryClassificationEvaluator()
    evaluator.evaluate(predictions)
    return evaluator


def evaluate_predictions(predictions):
    """ Evaluate the prediction
    :param
        predictions: the output prediction of classifier.classify()
    :return:
        a set of metrics
    """
    evaluator = get_evaluator_result(predictions)
    metrics = get_all_metrics(predictions)
    return evaluator, metrics
