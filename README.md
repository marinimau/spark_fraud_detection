# Spark fraud detection

An implementation of a machine learning algorithm on Spark able to identify fraud in credit card transactions.<br><br>
The algorithm is divided in the following phases:

1. Spark initialization
2. Data retrieval from Amazon S3
3. Data preprocessing (removing outliers and balancing)
4. Dataset split (training / test)
5. Model construction and classification
8. Results evaluation

## Contents

* [Dataset](#Dataset)
* [Project structure](#Progect-structure)
* [Instructions](#Instructions)
* [Configuration](#Configuration)
* [Dependencies](#Dependencies)

## Dataset 

The dataset contains transactions made by credit cards in September 2013 by European cardholders. 
This dataset presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions. The dataset is highly unbalanced, the positive class (frauds) account for 0.172% of all transactions.

It contains only numerical input variables which are the result of a PCA transformation. Unfortunately, due to confidentiality issues, we cannot provide the original features and more background information about the data.

## Project structure

```
+ - + spark_fraud_detection
    |
    + - + classifier.py: Model construction and classification
    |
    + - + conf.py (variables)
    |
    + - + data_loader.py: Data retrieval from Amazon S3
    |
    + - + main.py: Spark initialization and main
    |
    + - + preprocessing.py: Data preprocessing (removing outliers and balancing)
    |
    + - + result_evaluator.py: Results evaluation phase
    |
    + - + utils.py: Utility functions
    |
    + - + variables.py (variables)
```

## Instructions


## Configuration

***Required only to customize the configuration: nothing in this section is necessary for normal operation.*<br>

The editable params are organized in 2 files: 
* conf.py 
* variables.py

#### conf.py

| Name           |  Type   | Description                                | Default               |
|----------------|---------|--------------------------------------------|-----------------------|
| REMOTE         |  bool   | if True use the params optimized for aws   | True                  |
| VERBOSE        |  bool   | log in the standard output                 | True                  |

#### variables.py

| Name           |  Type   | Description                                | Default               |
|----------------|---------|--------------------------------------------|-----------------------|
| REMOTE         |  bool   | if True use the params optimized for aws   | True                  |
| VERBOSE        |  bool   | log in the standard output                 | True                  |

## Dependencies

* [Pyspark](https://pypi.org/project/pyspark/)
* [Pandas](https://pypi.org/project/pandas/)
* [Numpy](https://pypi.org/project/numpy/)
* [Scipy](https://pypi.org/project/scipy/)
* [Boto3](https://pypi.org/project/boto3/)



