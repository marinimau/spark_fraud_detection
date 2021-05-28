#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 15/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

from pyspark.ml.classification import GBTClassifier
from pyspark.ml.linalg import DenseVector

from variables import classifier_variables


class Classifier:
    """
    This class implements the classifier and the methods to prepare the dataframe for the classification task
    """

    spark_session = None
    training_dataframe = None
    test_dataframe = None

    def __init__(self, spark_dataframe, spark_session):
        """
        :param
            spark_dataframe: The preprocessed dataframe
        :param
            spark_session: The spark session declared in the main
        """
        self.spark_session = spark_session
        self.training_dataframe, self.test_dataframe = self.split_training_test(spark_dataframe)
        self.training_dataframe.cache()

    def split_training_test(self, spark_dataframe):
        """Given a dataframe in input perform the mapping in index, features and label and then split it in training set
        and test_set
        :param
            spark_dataframe: The input spark dataframe
        :return:
            the training set and the test_set
        """
        # mapping the dataframe in features, label and index (added before)
        tmp = spark_dataframe.rdd.map(lambda x: (DenseVector(x[0:29]), x[30], x[31]))
        # create a dataframe using the previous step mapping
        training_df = self.spark_session.createDataFrame(tmp, ["features", "label", "index"])
        # ordering the attributes
        training_df = training_df.select("index", "features", "label")
        # split the created dataframe in training (80%) and test (20%)
        return training_df.randomSplit(
            [classifier_variables["percentage_split_training"], 1 - classifier_variables["percentage_split_training"]],
            seed=classifier_variables["training_test_splitting_seed"])

    def classify(self):
        """Classify the data
        :return:
            the prediction
        """
        gbt = GBTClassifier(featuresCol="features", maxIter=100, maxDepth=8)
        model = gbt.fit(self.training_dataframe)
        return model.transform(self.test_dataframe)
