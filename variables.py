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
    "java_home": "/usr/lib/jvm/java-8-openjdk-amd64" if conf['REMOTE'] else "<YOUR_JAVA_PATH>",
    "spark_home": "/opt/spark-3.0.1-bin-hadoop2.7/" if conf['REMOTE'] else "<YOUR_SPARK_HOME_PATH>"
}

spark_args = "--packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://s01:7077  --executor-cores 2 --executor-memory 20g"

app_info = {
    "app_name": "FraudDetection" if conf['REMOTE'] else "spark"
}

conf_variables = {
    "master_ip": "172.31.80.101" if conf['REMOTE'] else "127.0.0.1",
    "master_port": "7077" if conf["REMOTE"] else "<YOUR_MASTER_PORT>",
    "protocol": "spark://"
}

data_load_variables = {
    "use_lite_dataset": True,
    "bucket": 'marinimau',
    "dataset_name": "s3://marinimau/1.csv",
    "lite_dataset_name": "s3://marinimau/1.csv",
}

preprocessing_variables = {
    "balance_dataframe": True,
    "remove_outliers": True,
    "remove_threshold": 5
}

classifier_variables = {
    "percentage_split_training": 0.8,
    "training_test_splitting_seed": 698
}
