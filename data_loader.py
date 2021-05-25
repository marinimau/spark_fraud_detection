#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 11/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

from variables import data_load_variables


def loader(spark_session):
    """Load the data from a csv file stored on S3
        :parameter:
            spark_session: the Spark session
        :return:
            a dataframe that contains the data
    """
    if data_load_variables["use_lite_dataset"]:
        path = data_load_variables["lite_dataset_path"]
    else:
        path = data_load_variables["dataset_path"]
    df = spark_session.read.csv(path)
    # note: check variables.py to alter the dataset path
    return df
