#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 15/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

from conf import conf

path_variables = {
    "java_home2": "/usr/lib/jvm/java-8-openjdk-amd64" if conf['REMOTE'] else "/usr/lib/jvm/java-8-openjdk-amd64",
    "spark_home": "/opt/spark-3.0.1-bin-hadoop2.7/" if conf['REMOTE'] else "/opt/spark-3.0.1-bin-hadoop2.7/"
}

app_info = {
    "app_name": "FraudDetection"
}

conf_variables = {
    "master_ip": "172.31.80.101" if conf['REMOTE'] else "127.0.0.1",
    "master_spark_port": "7077"
}

dataset_path = "s3://marinimau/1.csv" if conf['REMOTE'] else "datasets/1.csv",

preprocessing_variables = {
    "balance_dataframe": True,
    "remove_outliers": True,
}

classifier_variables = {
    "percentage_split_training": 0.8,
    "training_test_splitting_seed": 698
}

