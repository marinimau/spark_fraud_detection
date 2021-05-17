#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 17/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#


def print_prediction_metrics(metrics):
    """Print the prediction evaluation metrics
    :param
        metrics: a dictionary containing the calculated metrics
    :return:
    """
    print(
        "Confusion matrix:\n" + metrics["confusion_matrix"] + "\n\nPrecision: " + metrics["precision"] + "\nRecall: " +
        metrics["recall"] + "\nAccuracy: " + metrics["accuracy"] + "\nF-measure: " + metrics["f-measure"] + "\n\n")
