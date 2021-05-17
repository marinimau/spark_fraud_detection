#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 11/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

from variables import dataset_path


def loader(spark_session):
    """Load the data from a csv file stored on S3
        :parameter:
            spark_session: the Spark session
        :return:
            a dataframe that contains the data
    """
    df = spark_session.read.load(dataset_path, format="csv", sep=",", inferSchema="true", header="true")
    # note: check variables.py to alter the dataset path

    return df
