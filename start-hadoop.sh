#!/bin/bash
/etc/init.d/ssh start
$HADOOP_HOME/bin/hdfs namenode -format
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver

#Permissions for marlabs user
hdfs dfs -mkdir /user/marlabs && hdfs dfs -chown marlabs:supergroup /user/marlabs
hdfs dfs -chown marlabs:supergroup /tmp

 
tail -f /dev/null 
