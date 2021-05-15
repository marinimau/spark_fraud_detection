#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 11/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

from pyspark.sql import SparkSession
import os

from utils import load_from_csv
from variables import path_variables, conf_variables, app_info

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


def load_data(spark_instance):
    """Load the data
        :parameter:
            spark_instance: the Spark instance
        :return:
        a dataframe that contains the data
    """
    return load_from_csv(spark_instance, 1)


def main():
    """The main function
    :return:
    """
    spark_session, spark_context = initialize_spark()


if __name__ == '__main__':
    main()
