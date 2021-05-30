# Spark fraud detection

An implementation of a machine learning algorithm on Spark able to identify fraud in credit card transactions.<br><br>
The algorithm is divided in the following phases:

1. Spark initialization
2. Data retrieval from Amazon S3
3. Data preprocessing (removing outliers and balancing)
4. Dataset split (training / test)
5. Model construction and classification
8. Results evaluation

To run this project you need to have an AWS account.
Detailed instructions are in the [this](#Instructions) section.

## Contents

* [Dataset](#Dataset)
* [Project structure](#Project-structure)
* [Instructions](#Instructions)
* [Configuration](#Configuration)
* [Dependencies](#Dependencies)
* [Results](#Results)
* [Credits](#Credits)

## Dataset 

The dataset contains transactions made by credit cards in September 2013 by European cardholders. 
This dataset presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions. The dataset is highly unbalanced, the positive class (frauds) account for 0.172% of all transactions.

It contains only numerical input variables which are the result of a PCA transformation. Unfortunately, due to confidentiality issues, we cannot provide the original features and more background information about the data.

## Project structure

```
    
+ - + spark_fraud_detection
    |
    + - + configuration_files: file to configure the infrastructure, all the files contained in this directory are passed to ec2 instances by terraform
    |   | 
    |   + - + core-sites.xml
    |   | 
    |   + - + datanode_hostnames.txt: the list of datanodes (hostname only)
    |   | 
    |   + - + hadoop_paths.sh: hadoop installation paths
    |   | 
    |   + - + hdfs-site.xml
    |   | 
    |   + - + hosts.txt: a list of pair (IP, hostname) of the hosts (namenonde and datanode)
    |   | 
    |   + - + mapred-sites.xml
    |   | 
    |   + - + namenode_hostname.txt:  the list of namenodes (hostname only)
    |   | 
    |   + - + packets.sh: a script to install the required packets
    |   | 
    |   + - + paths.sh: generic paths (Java and Python)
    |   | 
    |   + - + requirements.txt: required Python libraries
    |   | 
    |   + - + spark-env-paths.sh
    |   | 
    |   + - + spark_paths.sh
    |   | 
    |   + - + yarn-site.xml
    |
    |
    |
    + - + spark_fraud_detection
    |   |
    |   + - + classifier.py: Model construction and classification
    |   |
    |   + - + conf.py (variables)
    |   |
    |   + - + data_loader.py: Data retrieval from Amazon S3
    |   |
    |   + - + main.py: Spark initialization and main
    |   |
    |   + - + preprocessing.py: Data preprocessing (removing outliers and balancing)
    |   |
    |   + - + result_evaluator.py: Results evaluation phase
    |   |
    |   + - + utils.py: Utility functions
    |   |
    |   + - + variables.py (variables)
    |
    |
    + - + main.tf: Terraform main
    |    
    + - + output.tf: Terraform success output
    |    
    + - + variables.tf: Terraform variables
```

## Instructions


#### Download required resources and configure credentials

1. Download and install [Terraform](https://terraform.io)

2. Download this repository

```shell script
git clone https://github.com/marinimau/spark_fraud_detection.git
```

3. Get your credentials from aws console and set them in the "terraform.tfvars"


4. Get a .pem AWS key (following the [docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair)) and put it in the root of the project. **Call it amzkey** 


5. Go to the project root
```shell script
cd spark_fraud_detection
```

6. Generate a ssh key called localkey (you are in the root of the project) 

```shell script
ssh-keygen -f localkey
```

7. Remember to change the permissions of the amzkey.pem
```shell script
chmod 400 amzkey.pem
```


#### Launch Terraform

8. Now you are ready to execute Terraform. Launch
```shell script
terraform init
```

and then

```shell script
terraform apply
```

It requires some time...

If all it's ok skip the following section, otherwise you probably have an error related to the subnet id.


#### Fix subnet-id error

If you have an error related to the subnet-id:

1. Open the aws terminal from the aws console and paste this command:

```shell script
aws ec2 describe-subnets
```

2. Copy the value of the field "subnet-id" of the second subnet and paste it as value of the field "subnet-id" in the file "variables.tf"

3. Ensure that the IPs in the variables "namenode_ips" and "datanode_ips" are included in the subnet, if not change them in:

* ./variables.tf 
```

...

variable "namenode_ips" {
    description = "the IPs for the namenode instances (each IP must be compatible with the subnet_id)"
    default = {
        "0" = "172.31.64.101" # change it
    }
}

...

variable "datanodes_ips" {
    description = "the IPs for the datanode instances (each IP must be compatible with the subnet_id)"
    default = {
        "0" = "172.31.64.102" # change it
        "1" = "172.31.64.103" # change it
        "2" = "172.31.64.104" # change it
        "3" = "172.31.64.105" # change it
        "4" = "172.31.64.106" # change it
        "5" = "172.31.64.107" # change it
    }
}

...

```
* ./configuration_files/hosts.txt (namenode ips and datanode ips, don't change the hostnames)
* ./spark_fraud_detection/variables.py (conf_variables\["master_ip"])

```python
conf_variables = {
    "master_ip": "172.31.64.101" if conf['REMOTE'] else "127.0.0.1",
    "master_port": "7077" if conf["REMOTE"] else "<YOUR_MASTER_PORT>",
    "protocol": "spark://"
}
```

*change in "master_ip" before the "if"*

Launch Terraform again with "terraform apply"


#### Connect to the namenode instance

1. Connect to the namenode instance using ssh

```shell script
ssh -i <PATH_TO_SPARK_TERRAFORM>/amzkey.pem ubuntu@<PUBLIC_DNS>
 ```

you can find the <PUBLIC_DNS> of the namenode instance in the output of terraform apply when the configuration ends.

2. After login execute on the master (one by one):
 ```
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slaves.sh spark://s01:7077
```

3. Configure your aws credential

```shell script
aws configure
```

put, when required, the same values used in the file terraform.tfvars

**IMPORTANT**: region is '**us-east-1**'

4. Launch the application
```
/opt/spark-3.0.1-bin-hadoop2.7/bin/spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://s01:7077  --executor-cores 2 --executor-memory 14g main.py
```

5. Remember to do `terraform destroy` to delete your EC2 instances

## Configuration

***Required only to customize the configuration: nothing in this section is necessary for normal operation.*<br>

The editable params are organized in 2 files: 
* conf.py 
* variables.py

#### conf.py (do not edit)

| Name           |  Type   | Description                                | Default               |
|----------------|---------|--------------------------------------------|-----------------------|
| REMOTE         |  bool   | local/remote configuration                 | True                  |
| VERBOSE        |  bool   | enable log in the standard output          | True                  |

#### variables.py

| Name           |  Type   | Description                                | Default               |
|----------------|---------|--------------------------------------------|-----------------------|
| REMOTE         |  bool   | if True use the params optimized for aws   | True                  |
| VERBOSE        |  bool   | log in the standard output                 | True                  |

| Name           |  Type   | Description                                | Default               |
|----------------|---------|--------------------------------------------|-----------------------|
| region         | string  | The region for your EC2 instances          | us-east-1             |
| access_key     | string  | Your AWS access key (don't change here)    |                       |
| secret_key     | string  | Your AWS secret key (don't change here)    |                       |
| token          | string  | Your AWS token (don't change here)         | null                  |
| instance_type  | string  | EC2 instance type                          | m5.xlarge             |
| ami_image      | string  | AMI code for the EC2 instances (OS image)  | ami-0885b1f6bd170450c |
| key_name       | string  | The name of the local key                  | localkey              |
| key_path       | string  | The directory that contain the local key   | .                     |
| aws_key_name   | string  | The name of the key generated on AWS       | amzkey                |
| amz_key_path   | string  | The path of the key generated on AWS       | ./amzkey.pem          |
| subnet_id      | string  | The subnet-id for ec2 (see instructions)   | subnet-1eac9110       |
| namenode_count | integer | The number of namenode EC2 instances       | 1                     |
| datanode_count | integer | The number of datanode ec2 instances       | 3                     |
| datanode_count | integer | The number of datanode ec2 instances       | 3                     |
| hostnames      |  bool   | Default private hostnames used for nodes   | See variables.tf      |

## Dependencies

* [Pyspark](https://pypi.org/project/pyspark/)
* [Pandas](https://pypi.org/project/pandas/)
* [Numpy](https://pypi.org/project/numpy/)
* [Scipy](https://pypi.org/project/scipy/)
* [Boto3](https://pypi.org/project/boto3/)

## Results

#### Classification

#### Time

| #Instances     |  Time   |
|----------------|---------|
| 1              |  -   |
| 2              |  -   |
| 3              |  -   |
| 4              |  -   |
| 5              |  -   |
| 6              |  -   |


## Credits
 * [spark-terraform](https://github.com/conema/spark-terraform): a starting point for the Terraform configuration
