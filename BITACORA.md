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

## 📓 Bitácora de Desarrollo (verificar lo marcado con ⚠️)

### 🔹 Setup inicial fallido en Windows

* Intento fallido de usar Airflow con PowerShell debido a restricciones del sistema para ejecutar scripts (`ExecutionPolicy`).
* Instalación de Airflow falló con error de launcher → causado por rutas rotas al mover carpetas del entorno virtual ⚠️.

### 🔹 Decisión: migrar a WSL2

* Se instaló Ubuntu via WSL2.
* Problemas al crear `venv` por `ensurepip` ausente → se solucionó con `sudo apt install python3.10-venv` ⚠️.
* Activación exitosa del entorno y prueba de Airflow en entorno Linux.

### 🔹 Composición del entorno Docker

* Se definieron servicios en `docker-compose.yml`: Zookeeper, Kafka, Schema Registry, Control Center, Airflow (webserver y scheduler), PostgreSQL, Spark Master & Worker, Cassandra.
* Se añadió un `entrypoint.sh` para inicializar correctamente el webserver de Airflow.
* Se agregó Cassandra y Spark con sus respectivas configuraciones internas ⚠️.

### 🔹 Conexión y pruebas de Kafka

* Se ejecutó comando para listar topics y crear el topic `users_created` si no existía.
* Se validó que Kafka estaba recibiendo datos desde Airflow usando Kafka CLI y Control Center.

### 🔹 Errores encontrados

* DAG no ejecutaba porque faltaba librería `kafka-python` → se agregó a `requirements.txt` ⚠️.
* DAG no corría porque `catchup` no estaba habilitado o mal configurado ⚠️.
* Spark inicialmente sin entender del todo su rol → se revisó e implementó manualmente ⚠️.

### 🔹 Observaciones técnicas

* El topic de Kafka no se define en YAML, sino que se crea manualmente o automáticamente (dependiendo del `auto.create.topics.enable`).
* Los datos en Kafka viven en `/var/lib/kafka/data` pero no se gestionan directamente ahí.
* Spark y Cassandra se comunican vía drivers (`pyspark`, `cassandra-driver`).
* Se usa `broker:29092` como dirección del broker desde contenedores internos.

### 🔹 Mejoras futuras sugeridas ⚠️

* Configurar Spark como proceso 24/7.
* Permitir creación segura de topics.
* Separar desarrollo de producción vía volúmenes persistentes.
* Automatizar ejecución de `spark_stream.py` desde Airflow u otro scheduler.

---

¿Listo para escalar esto a producción? 🚀

No, pero si.

