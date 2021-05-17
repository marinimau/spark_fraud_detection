#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 11/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

from conf import conf
from classifier import Classifier
from data_loader import loader
from preprocessing import balance_data, remove_outliers
from result_evaluator import evaluate_predictions
from variables import path_variables, conf_variables, app_info
from utils import print_prediction_metrics

os.environ["JAVA_HOME"] = path_variables["java_home"]
os.environ["SPARK_HOME"] = path_variables["spark_home"]


def initialize_spark():
    """Initialize a Spark session and context
        :parameter:
        :return:
            the Spark session and the Spark context
    """
    spark_session = SparkSession.builder.master(
        "spark://" + conf_variables["master_ip"] + ":" + conf_variables["master_port"]).appName(
        app_info["app_name"]).enableHiveSupport().getOrCreate()
    spark_context = spark_session.sparkContext
    spark_context.setLogLevel("Error")
    return spark_session, spark_context


def preprocessing(spark_dataframe):
    """Preprocessing the data
    :param
        spark_dataframe: the raw data dataframe
    :return:
        the preprocessed dataframe
    """
    # convert dataframe to pandas
    pd_dataframe = spark_dataframe.toPandas()
    pd_dataframe = pd_dataframe.sample(frac=1)

    # remove outliers
    no_outliers_pd_dataframe = remove_outliers(pd_dataframe)

    # balance dataframe
    pd_balanced_dataframe = balance_data(no_outliers_pd_dataframe)

    return pd_balanced_dataframe


def main():
    """The main function
    :return:
    """
    spark_session, spark_context = initialize_spark()
    preprocessed_pd_dataframe = preprocessing(loader(spark_session))

    # return to spark dataframe
    preprocessed_spark_dataframe = spark_session.createDataFrame(preprocessed_pd_dataframe)
    w = Window().orderBy('Time')
    preprocessed_spark_dataframe = preprocessed_spark_dataframe.withColumn("ID", row_number().over(w))

    # initialize the classifier class and classify
    classifier = Classifier(preprocessed_spark_dataframe, spark_session)
    predictions = classifier.classify()

    # get the evaluation metrics
    binary_evaluator, metrics = evaluate_predictions(predictions)

    if conf["VERBOSE"]:
        print_prediction_metrics(metrics)


if __name__ == '__main__':
    main()
