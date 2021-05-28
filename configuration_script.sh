#/bin/bash

# wait that the boot finish, otherwise apt-get could fail
until [[ -f /var/lib/cloud/instance/boot-finished ]]; do
  sleep 1
done

# install some packages
sudo chmod +x /home/ubuntu/packets.sh
sudo /home/ubuntu/packets.sh

# install python libraries
pip3 install -r /home/ubuntu/requirements.txt

# master and slaves ip (you can add more if needed)
cat /home/ubuntu/hosts.txt | sudo tee --append /etc/hosts > /dev/null

sudo chmod 700 /home/ubuntu/.ssh
sudo chmod 600 /home/ubuntu/.ssh/id_rsa

cat /home/ubuntu/paths.sh | sudo tee --append /home/ubuntu/.bashrc > /dev/null

# install hadoop 2.7.7
cd /opt/
sudo wget https://archive.apache.org/dist/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz > /dev/null
sudo tar zxvf hadoop-2.7.7.tar.gz > /dev/null

# hadoop configuration files
cat /home/ubuntu/hadoop_paths.sh | sudo tee --append /home/ubuntu/.bashrc > /dev/null
sudo cp /home/ubuntu/core-sites.xml /opt/hadoop-2.7.7/etc/hadoop/core-site.xml
sudo cp /home/ubuntu/yarn-site.xml /opt/hadoop-2.7.7/etc/hadoop/yarn-site.xml
sudo cp /opt/hadoop-2.7.7/etc/hadoop/mapred-site.xml.template /opt/hadoop-2.7.7/etc/hadoop/mapred-site.xml
sudo cp /home/ubuntu/mapred-site.xml /opt/hadoop-2.7.7/etc/hadoop/mapred-site.xml
sudo cp /home/ubuntu/hdfs-site.xml /opt/hadoop-2.7.7/etc/hadoop/hdfs-site.xml

# host configuration
cat /home/ubuntu/namenode_hostname.txt | sudo tee --append /opt/hadoop-2.7.7/etc/hadoop/masters > /dev/null
cat /home/ubuntu/datanode_hostnames.txt | sudo tee /opt/hadoop-2.7.7/etc/hadoop/slaves > /dev/null

sudo sed -i -e 's/export\ JAVA_HOME=\${JAVA_HOME}/export\ JAVA_HOME=\/usr\/lib\/jvm\/java-8-openjdk-amd64/g' /opt/hadoop-2.7.7/etc/hadoop/hadoop-env.sh

sudo mkdir -p /opt/hadoop-2.7.7/hadoop_data/hdfs/namenode
sudo mkdir -p /opt/hadoop-2.7.7/hadoop_data/hdfs/datanode

sudo chown -R ubuntu /opt/hadoop-2.7.7


# spark installation
cd /opt/
sudo wget https://archive.apache.org/dist/spark/spark-3.0.1/spark-3.0.1-bin-hadoop2.7.tgz > /dev/null
sudo tar -xvzf spark-3.0.1-bin-hadoop2.7.tgz > /dev/null
cat /home/ubuntu/spark_paths.sh | sudo tee --append /home/ubuntu/.bashrc > /dev/null
sudo chown -R ubuntu /opt/spark-3.0.1-bin-hadoop2.7

cd spark-3.0.1-bin-hadoop2.7
cp conf/spark-env.sh.template conf/spark-env.sh

# spark configuration files
cat /home/ubuntu/spark-env-paths.sh | sudo tee --append conf/spark-env.sh > /dev/null
cat /home/ubuntu/datanode_hostnames.txt | sudo tee --append conf/slaves > /dev/null
cp conf/spark-defaults.conf.template conf/spark-defaults.conf

echo -e '$HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/sbin/start-yarn.sh && $HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver' > /home/ubuntu/hadoop-start-master.sh
echo '$SPARK_HOME/sbin/start-master.sh' > /home/ubuntu/spark-start-master.sh
echo '$SPARK_HOME/sbin/start-slave.sh spark://s01:7077' > /home/ubuntu/spark-start-slave.sh
