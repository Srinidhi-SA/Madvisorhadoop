FROM ubuntu:16.04
MAINTAINER marlabs
RUN groupadd -r marlabs && useradd -r -s /bin/false -g marlabs marlabs

ENV HADOOP_HOME /opt/hadoop
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN apt-get update
RUN \
    apt-get install -y \
    ssh \
    rsync \
    vim \
    openjdk-8-jdk \
    python-pip \
    virtualenv \
    telnet \
    net-tools

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
# install dependencies
RUN virtualenv --python=python2.7 myenv
RUN . myenv/bin/activate && pip install pywebhdfs==0.4.1

#Adding pbr
RUN pip install pbr
RUN pip install pywebhdfs==0.4.1 
RUN pip install python-sjsclient
RUN pip install --upgrade setuptools



RUN pip install pyspark==2.4.0
RUN pip3 install numpy
#RUN apt-get install enchant -y
#RUN apt-get install libmysqlclient-dev -y


#Adding requirements
#COPY ./requirements.txt /requirements.txt
#ADD ./requirements.tar.gz $pwd
#RUN pip install pyenchant && pip install sklearn2pmml && pip install -r requirements.txt
#RUN rm -rf myenv/
# Add this line OR ...
#ADD hadoop-3.0.0.tar.gz /
# ... uncomment the 2 first lines
RUN \
    wget http://archive.apache.org/dist/hadoop/common/hadoop-3.0.0/hadoop-3.0.0.tar.gz && \
    tar -xzf hadoop-3.0.0.tar.gz && \
    mv hadoop-3.0.0 $HADOOP_HOME && \
    for user in hadoop hdfs yarn mapred; do \
         useradd -U -M -d /opt/hadoop/ --shell /bin/bash ${user}; \
    done && \
    for user in root hdfs yarn mapred; do \
         usermod -G hadoop ${user}; \
    done && \
    echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_DATANODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
#    echo "export HDFS_DATANODE_SECURE_USER=hdfs" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_NAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_SECONDARYNAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export YARN_RESOURCEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/yarn-env.sh && \
    echo "export YARN_NODEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/yarn-env.sh && \
    echo "PATH=$PATH:$HADOOP_HOME/bin" >> ~/.bashrc
RUN \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys
ADD *xml $HADOOP_HOME/etc/hadoop/
ADD ssh_config /root/.ssh/config
RUN mkdir /opt/hadoop/start/
ADD start-hadoop.sh /opt/hadoop/start/start-hadoop.sh
RUN chmod +x /opt/hadoop/start/start-hadoop.sh
EXPOSE 8088 9870 9864 8030 8031 8032 8033 9000
RUN mkdir /opt/hadoop/name_node
RUN mkdir /opt/hadoop/data_node
CMD bash /opt/hadoop/start/start-hadoop.sh
