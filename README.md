## To build hadoop container:
	docker build -t hadoop:latest .


## To start hadoop container:

	docker run --hostname=hadoop -p 8032:8032 -p 9000:9000 -p 8088:8088 -p 9870:9870 -p 9864:9864 -p 19888:19888 -p 8042:8042 -p 8888:8888 --name hadoop -d <image id>

#### To run hadoop container along with spark container using docker-compose refer README file present in hadoop_spark_compose directory
