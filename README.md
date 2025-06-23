# Proyecto de Pipeline de Streaming con Apache Kafka, Airflow, Spark y Cassandra

Este proyecto consiste en un pipeline de procesamiento de datos en tiempo real utilizando Airflow para orquestación, Kafka para ingesta de datos en streaming, Spark para procesamiento distribuido y Cassandra como base de datos NoSQL para almacenamiento.

---

## Arquitectura General

```
API (randomuser.me) --> Airflow DAG --> Kafka Topic --> Spark Structured Streaming --> Cassandra
```

## Componentes Explicados

### 🔁 Apache Airflow

Orquesta tareas y ejecuta DAGs (Directed Acyclic Graphs) definidos en Python. En este caso, el DAG se encarga de:

* Llamar a la API `randomuser.me`.
* Formatear la respuesta.
* Enviar los datos formateados a Kafka.

### 🐘 PostgreSQL

Utilizado como base de datos interna para Airflow. No se utiliza para almacenar datos del pipeline.

### 🐳 Kafka + Zookeeper

Kafka maneja los mensajes en tiempo real (usuarios generados por la API). Zookeeper coordina los brokers de Kafka.

* **Broker**: Maneja los topics, productores y consumidores.
* **Schema Registry**: Registra los esquemas de los mensajes.
* **Control Center**: Interfaz visual para monitorear Kafka, topics, alertas, flujos de mensajes.

### ⚡ Apache Spark

Spark Structured Streaming actúa como consumidor de Kafka. Lee los mensajes del topic `users_created`, los transforma y los guarda en Cassandra.

* **Spark Master**: Nodo principal del cluster Spark.
* **Spark Worker**: Nodo que ejecuta las tareas distribuidas.

### 🗄️ Apache Cassandra

Base de datos NoSQL distribuida que almacena los usuarios generados por el sistema. Es ideal para escalabilidad horizontal y escritura rápida.

---

## Requisitos del Proyecto

### requirements.txt

```txt
requests
kafka-python
pyspark==4.0.0
cassandra-driver==3.29.2
```

### Dockerfile personalizado para Airflow

```Dockerfile
FROM apache/airflow:2.6.0-python3.9
USER root
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"
USER airflow
```

---

## 🧪 Cómo probar el pipeline paso a paso

### 1. Activar integración WSL2 con Docker (si estás en Windows)

* Docker Desktop → Settings → Resources → WSL Integration → Activar.

### 2. Reconstruir y levantar los contenedores

```bash
docker-compose down -v --remove-orphans
docker-compose build
docker-compose up -d
```

Esperá que todos estén **healthy**.

### 3. Crear el topic en Kafka (si no existe)

```bash
docker exec -it broker kafka-topics --create \
  --bootstrap-server broker:29092 \
  --replication-factor 1 --partitions 1 --topic users_created
```

### 4. Ingresar al Airflow UI ([http://localhost:8080](http://localhost:8080))

* Activar el DAG `user_automation`
* Ejecutarlo manualmente o esperar la programación diaria.

### 5. Verificar Kafka

```bash
docker exec -it broker kafka-console-consumer \
  --bootstrap-server broker:29092 \
  --topic users_created --from-beginning
```

O visitar `http://localhost:9021` para usar el Control Center.

### 6. Ejecutar el script de Spark (por ahora manual)

```bash
source venv/bin/activate
python spark_stream.py
```

Este script:

* Conecta a Kafka.
* Lee desde el topic.
* Procesa los datos.
* Guarda en Cassandra.

### 7. Verificar los datos en Cassandra

```bash
docker exec -it cassandra cqlsh
> SELECT * FROM users_stream.users;
```

---

## 💡 Diferencias con un pipeline de producción

| Tu proyecto                   | Producción real                 |
| ----------------------------- | ------------------------------- |
| DAG con trigger manual        | DAG con disparadores continuos  |
| Spark manual                  | Spark streaming 24/7            |
| Cassandra local               | Cassandra en clúster multi-nodo |
| Kafka local y sin TLS         | Kafka seguro + monitoreo        |
| Sin almacenamiento intermedio | S3, HDFS, Lakehouse             |

---

## Próximos pasos sugeridos

* Mas data.

---

¿Listo para escalar esto a producción? 🚀

No, pero si.

