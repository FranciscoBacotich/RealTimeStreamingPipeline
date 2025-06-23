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

