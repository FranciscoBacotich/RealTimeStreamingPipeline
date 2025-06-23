👉 Setting up a data pipeline with Apache Airflow<br> 
👉 Streaming data with Kafka and Kafka Connect<br> 
👉 Using Zookeeper for distributed synchronization<br> 
👉 Data processing with Apache Spark<br> 
👉 Data storage solutions with Cassandra and PostgreSQL<br> 
👉 Containerizing your data engineering environment with Docker<br> 

Summary of architecture: 

    We will be calling an api, called Random User Generator, which creates synthetic user data. (randomuser.me)
    We will have a DAG in Apache Airflow which is going to be fetching data from our API, by running the configuration in postgreSQL as language to interact with the api data source.

    The fetch data will be streamed into Kafka and inside kafka to Control Center (to visualize the data of a broadcast. Works as our UI, to visualize what is going on with the topics, etc.) and Schema Registry (seven layer of metadata. It is a restful interface. Our storage for the schema, useful when spinning up Kafka to have the schema of the data that is to be expected in the broadcast, already in kafka). Kafka will be sitting in Apache ZooKeeper. This is a manager to manage all the multiple tasks or broadcast, that will be going on in kafka.

    Apache Spark is a powerful, open-source framework for processing large amounts of data quickly. It's like a super-fast engine for handling big data, capable of performing various tasks like data analysis, machine learning, and real-time processing. It's designed to handle huge datasets and can run on clusters of computers, making it much faster than older methods. 

    All of this data will be streamed with Apache Spark. With a master worker architecture, that divides jobs of running data, tasks and flows. The task in our case is going to be streamming the data to Cassandra. So the master worker is going to get the data from kafka, define the flow and job division, to get the data into Cassandra. Our end user"

    All of this architecture running as a Docker Container.


We define functions in a python script, where our dags in Airflow live, where we get the data, define how the response it is going to be parsed, and then sent into our Kafka-Zookeper enviroment.
# Default parameters for tasks within a DAG
    default_args = {
        'owner': 'airscholar',
        'start_date': datetime(2025, 5, 7, 12, 00)
    }


    def get_data():
        import requests                      #to get data from the api, and filter the result response accordingly

    res = requests.get("https://randomuser.me/api/")  
    res = res.json()                          #Setting this up now early on helps with being able to test it out with the stream_data() function
                                                #Aca podemos hacer un test para ver como imprime la respuesta y que partes queremos
    
    res = res['results'][0]                   #Select part of the array we want and the index of the record number. Because the api requests comes with multiple fields sometimes and we want to make sure we are just getting the ones we want.
    #print(res)                             
    
    return res
## Thats why even though we started by getting the data from our source, I went ahead and created the Docker containers for our infrastructure.<br>
The configuration for the invoking of the componentes in the docker-compose file was fairly simple and normal. Nothing out of this world. Basically I look for the component documentation, read through it, find some reference as a guide for the implementation, and write down the fields. 

## When defining Docker Compose components (services) — such as a Kafka web server — the main points of interest revolve around service configuration, networking, volumes, and dependencies.
    
    zookeeper:
          image: confluentinc/cp-zookeeper:7.4.0
          hostname: zookeeper
          container_name: zookeeper
          ports:
            - "2181:2181"
          environment:
            ZOOKEEPER_CLIENT_PORT: 2181
            ZOOKEEPER_TICK_TIME: 2000
          healthcheck:
            test: ['CMD', 'bash', '-c', "echo 'ruok' | nc localhost 2181"]
            interval: 10s
            timeout: 5s
            retries: 5
          networks:
            - confluent


Once those images are runnig, you can access the UI for control center ( check what hostname is placed at ) and visualize the broker or images that are up, basically you see the stream of data.
When we see the control center, we see the consumptuion and other information. but we want to focus on the Topic tab. 

    docker-compose -d up
    docker-compose -d down

# 🧠 Bug ¿Qué pasó?
Docker Desktop en Windows tiene que estar instalado, corriendo y con la integración WSL2 activada para que puedas usar docker desde tu terminal Ubuntu.

✅ PASO A PASO PARA SOLUCIONARLO
1. 🟢 Asegurate de que Docker Desktop esté instalado y abierto
Abrí Docker Desktop desde el menú de Windows.


### What is a topic in Apache Kafka(ControlCenter)? 
The fundamental unit for organizing and categorizing messages. It's essentially a named channel or feed where producers (applications that send messages) write data, and consumers (applications that read data) subscribe to receive it. Think of it like a specific category or subject for your messages. 

In Apache Kafka, a topic is the fundamental unit for organizing and categorizing messages. It's essentially a named channel or feed where producers (applications that send messages) write data, and consumers (applications that read data) subscribe to receive it. Think of it like a specific category or subject for your messages. 


## 🧠 Entonces… ¿Dónde está el topic?
Un topic de Kafka:

No es un archivo o configuración fija en el YAML del servicio broker.

Se guarda internamente en los directorios de logs del contenedor broker, típicamente en /var/lib/kafka/data o similar.

Pero para interactuar con ellos, se usa la CLI dentro del contenedor broker.

## 🔍 ¿Cómo ver si el topic existe?
Usá este comando en tu terminal para inspeccionar los topics existentes en el broker:

bash
docker exec -it broker kafka-topics --list --bootstrap-server broker:29092
Si users_created aparece ahí, ¡existe!

## 📌 ¿Y si querés crearlo?
Si el topic no está y auto.create.topics.enable=true está deshabilitado (nota: no está configurado explícitamente en tu YAML, pero por defecto suele estar en true), podés crearlo así:

    bash
    docker exec -it broker kafka-topics --create \
      --bootstrap-server broker:29092 \
      --replication-factor 1 \
      --partitions 1 \
      --topic users_created
      
📁 ¿Dónde se guarda físicamente?
Dentro del contenedor Kafka (broker), los datos del topic se guardan en:

kotlin
/var/lib/kafka/data/
Pero no necesitás tocar eso manualmente. Kafka maneja internamente esa estructura.

## ✅ Resumen
Qué querés saber	Respuesta técnica
¿Dónde se define un topic?	Se crea automáticamente o con CLI dentro del contenedor Kafka
¿Dónde están físicamente?	En /var/lib/kafka/data dentro del contenedor
¿Cómo los veo?	kafka-topics --list --bootstrap-server broker:29092
¿Cómo creo uno?	Usando el comando --create en el contenedor broker

## Here's a more detailed breakdown:
#### Organization:
Topics are the way Kafka structures data, allowing for logical separation of different streams of messages. 
#### Naming:
Each topic has a unique name, making it easy to identify and differentiate different data streams. 
#### Partitions:
Topics can be divided into partitions, which are distributed across multiple brokers (servers) in the Kafka cluster. This partitioning allows for parallel processing and increased throughput. 
#### Producers and Consumers:
Producers write messages to specific topics, while consumers subscribe to topics to read those messages. 
#### Ordering:
Kafka guarantees the order of messages within a partition. 
#### Data Retention:
Topics store messages for a configurable period, after which they are typically purged. 
In Confluent Control Center, you can manage and monitor topics, including creating, editing, and viewing their details. You can also browse messages within a topic and monitor its performance. 


Considering this, we want to connect it to our kafka stream function, or que. To do this, we need kafka-python PACKAGE. So that by the time we get the data, we format it, and then we publish the data to kafka.

This is so that we can build a KafkA Producer to give out Kafka Topic data to workl with. A Kafka Producer is an essential component of this platform, responsible for publishing (producing) messages to Kafka topics. Producers send data to Kafka brokers, which then store the data until it's consumed. To use this type of component, as well as Kafka Consumer, this are add ons libraries for python you need to install in your repo, so remember to add it in the container requirements build.

Now that the control Zookepeer is connected, with Control Center working with Schema Registry. Now that part is build, we need to push constantly the data from airflow into our structure. 

We go into the docker compose and build up our web server for Airflow. 
We create the image in the docker compose, and then we need to add a script folder with the entrypoint.sh file where we put a secuence of commands that airflow should follow when it is trying to initalize the webserver.

Once you created dont forget to add it the volumes field in the webserver docker file. So that spins up the dags and the entrypoint when building up the server.

Here we see how we use postrgress when building the server so that with SQL aLCHEMY we make the request to the API to get the information, we store it temporaly and then stream it into the kafka broker structure we have created previously. 

BUT remember that is not just using the SQL ALCHEMY and postgres in the image that you want, in order to be able to do it, you have to spin uop a server postgres in the docker compose file. 

The scheduler is also a must for automating in this scenario. airflow-scheduler service represents the core component responsible for orchestrating and managing the execution of your data pipelines (DAGs).

Once we build up the webserver  and scheduler, build up again with the docker compose, go into the docker desktop ui, and look in rthe logs of the server. Look for something like this: 

[2025-06-21 17:03:21 +0000] [20] [INFO] Listening at: http://0.0.0.0:8080⁠ (20)

This means that pur webs erver is listening in that port for whatever is to come. 
Now you can go into the localhost:8080 and use the airflow UI.

iN THERE We first see a flag saying we are using the Sequential Executor in the scheduler, we can change that later.
https://airflow.apache.org/docs/apache-airflow/2.6.0/core-concepts/executor/index.html

To find the IP address of your Apache Kafka broker for your Airflow KafkaProducer, you'll need to look at the bootstrap.servers configuration in your Kafka producer settings. This setting specifies a list of host/port pairs that the producer uses to initially connect to the Kafka cluster. It's crucial for the producer to be able to resolve these addresses, so ensure they are correct and accessible from where your Airflow DAGs are running. 

We now can go into the UI, after connecting our server to our broker, and see the DAG for user_automation is up. 

At this staage we need to work on bringing more data in. Not just one run of it, so we need to modify the stream data function.We are building up a loop to set up a time frame

What we do is that we nest everything inside the loop, that way we have a control of when it will run how long etc


Once that is done we want to go back to our ui refresh and trigger the dag from the ui by  turning it on. 

BUG. nothing happens. WHy? Because we diddnt enable catch up. But we got a bug that he diddnt, We forgot to add the kafkapython in the sript that builds up the container, meaning the requirements, so the dag does not know what a python operator is if the library is not installed. 


NOw we are going to set up the spark with the master worker architecture with only one worker, but we could add more

IN THE docker compose, we see that the sparkl master will live where the ports specify.
We have 2 in this case, meaning we have to use 9090 in this case.

For the worker, we can replate it because we have more than one, we just do the same time after time with different naming convenitioons, it depends on the master on the dependency, using the Worker class. So the importan field in the worker is the "command" field.

Now for cassandra we a re going to use tha latest, choose the ports, and select the size. Almost same considerations as with the workers and spark.

With the instances running, you can do docker ps command that shows the containers that are up, same way that Docker Desktop does. 

Also we need to create a spark.py file to make the logic for the architecture.

To communicate with cassandra we need the cassandra driver:

   pip install cassandr-driver
   pip install pyspark

So we use this dependencies for communicating with cassandra and for creating the code for the spark stream.

In the MVN repo website, we check the veersion and then add them to the create connection function for our spark file, it is just a good practice as that is how is done in production. 

SPARK edta medio borroso lo que hace no entendi mucho. focus enb hacerlo y dps se revee.













docker compose up -d

we only need acess to the first json in the file.

Now after creating the kafka_stream file where we conneect to the api, and fix the response to a json format that is readble and has the information that we want ( take notes from how i did it)

now we need to setup kafka to receive this information. But before that we are not using our dockjer container. Apache is in our system,
we need to set up a docker compose file that is going to be initializing apache airflow, kafka, schema registry and control center, etc.

The goal is for the zookeeper is getting the dependencies down to kafka connected to control center and schema registry. Apache airflow is going to be a standalone instance, it is not connected to the architecture of our system.

Then we are going to have third system ( apache airflow, zookeeper/kafka env, and now) for the Apache Spark and another for Cassandra.

Control center is reliant in schema registry, because it needs to get feed the schema for the ui, the avg schema that the schema registry allows to be visualize in kafka is going to be a dependant in schema registry, that allows kafka to visualize the data in a certain way on the UI. Technically the control center is listening for events in schema registry to visualize the data living in kafka managed by the zookeeper.
