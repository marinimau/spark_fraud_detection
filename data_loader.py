#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 11/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

import pandas as pd
import boto3

from variables import data_load_variables


def loader():
    """Load the data from a csv file stored on S3
        :return:
            a dataframe that contains the data
    """
    bucket = data_load_variables["bucket"]

    if data_load_variables["use_lite_dataset"]:
        dataset_name = data_load_variables["lite_dataset_name"]
    else:
        dataset_name = data_load_variables["dataset_name"]

    s3 = boto3.client('s3')

    obj = s3.get_object(Bucket=bucket, Key=dataset_name)
    # get object and file (key) from bucket

    df = pd.read_csv(obj['Body'])
    return df
