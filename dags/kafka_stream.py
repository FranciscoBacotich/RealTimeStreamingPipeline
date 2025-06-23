from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import uuid
from airflow.decorators import dag, task

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2025, 5, 7, 12, 00)
}


def get_data():
    import requests                      

    res = requests.get("https://randomuser.me/api/")  
    res = res.json()                          
    
    res = res['results'][0]                   
    
    return res


#Function to define the response format. (1) 
def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['adress'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data


def stream_data():
    import json                         
    from kafka import KafkaProducer
    import time
    import logging

    logging.basicConfig(level=logging.INFO)

    try:
        producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)       #(2)
    except Exception as e:                                                                    #(3)
        logging.error(f'Could not connect to Kafka: {e}')
        return
    
    curr_time = time.time()
    
    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        try:
            res = get_data()
            res= format_data(res)
            logging.info(f"Sending: {res}") #(4)       
            producer.send('users_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error ocurred: {e}')
            continue # Log the error and continue
                     # (4)
# (5)
with DAG('user_automation',
        default_args = default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:
    print("DAG loaded successfully")
    #As we need the stream data function, we need to create it before.
    streaming_task = PythonOperator(
        task_id = 'stream_data_from_api',                 #(6)
        python_callable = stream_data
    )

            

   






