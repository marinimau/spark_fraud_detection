#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 11/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

def load_from_csv(spark_instance, dataset_name):
    """Load the data from a csv file
        :parameter:
            spark_instance: the Spark instance
            dataset_name: the name of the dataset (integer)
        :return:
        a dataframe that contains the data
    """
    assert(dataset_name == 1 or dataset_name == 2)
    df = (spark_instance.read
          .format("csv")
          .option('header', 'true')
          .load('datasets/' + str(dataset_name) + ".csv"))
    return df


def load_from_s3(spark, dataset):
    pass
