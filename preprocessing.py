#
#   spark_fraud_detection copyright © 2021 - all rights reserved
#   Created at: 15/05/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/spark_fraud_detection
#   Credits: @marinimau (https://github.com/marinimau)
#

import pandas as pd
import numpy as np
from scipy import stats

from variables import preprocessing_variables
from conf import conf


def remove_outliers(dataframe):
    """Filter the dataframe removing rows having one or more attributes with z-score >= 3
    :param
        dataframe: the Pandas dataframe with outliers
    :return:
        the Pandas dataframe without outliers
    """
    if preprocessing_variables["remove_outliers"]:
        return dataframe[(np.abs(stats.zscore(dataframe.iloc[:, 1:29])) < 3).all(axis=1)]
    else:
        return dataframe


def balance_data(dataframe):
    """Create a balanced dataframe from an unbalanced dataframe
    :param
        dataframe: the unbalanced Pandas dataframe
    :return:
        a balanced Pandas dataframe
    """
    if preprocessing_variables["balance_dataframe"]:
        if conf["VERBOSE"]:
            print("start balancing data...\n")
        fraud_dataframe = dataframe[dataframe['Class'] == 1]
        fraud_records_count = len(fraud_dataframe)
        not_fraud_dataframe = dataframe[dataframe['Class'] == 0].sample(n=fraud_records_count, random_state=1)
        if conf["VERBOSE"]:
            print("balancing data OK\n")
        return pd.concat([fraud_dataframe, not_fraud_dataframe]).sample(frac=1, random_state=47)
    else:
        return dataframe
