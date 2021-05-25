#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 17/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

import csv
from datetime import datetime

from conf import conf
from variables import preprocessing_variables
from variables import classifier_variables


def print_prediction_metrics(metrics):
    """Print the prediction evaluation metrics
    :param
        metrics: a dictionary containing the calculated metrics
    :return:
    """
    print(
        "Confusion matrix:\n" + str(metrics["confusion_matrix"]) + "\n\nPrecision: " + str(
            metrics["precision"]) + "\nRecall: " +
        str(metrics["recall"]) + "\nAccuracy: " + str(metrics["accuracy"]) + "\nF-measure: " + str(
            metrics["f-measure"]) + "\n\n")


def calculate_elapsed_time(start_time, end_time):
    """Calculate the time and print it in the standard output
    :param
        stat_time: the starting time
    :param
        end_time: the end time
    :return: the elapsed time
    """
    elapsed_time = end_time - start_time
    if conf["VERBOSE"]:
        print("Elapsed time: " + str(elapsed_time) + "\n")
    return elapsed_time


def write_time_on_file(elapsed_time):
    """Write test params end elapsed time in a .csv file named result_<current_datetime>
    :param
        elapsed_time: the elapsed time
    :return:
    """
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
    with open('result_' + date_time + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["remote", "balanced_dataframe", "remove_outliers", "training_set_percentage", "time"])
        writer.writerow(
            [conf["REMOTE"], preprocessing_variables["balance_dataframe"], preprocessing_variables["remove_outliers"],
             classifier_variables["percentage_split_training"], elapsed_time])
