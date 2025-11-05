import sys
import os
from contextlib import asynccontextmanager 
from aiokafka import AIOKafkaProducer

KAFKA_BOOTSTRAP_SERVERS:str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

@asynccontextmanager
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    try:
        await producer.start()
        yield producer
    except Exception as e:
        print(f"Error starting Kafka producer: {e}", file=sys.stderr)
        raise
    finally:
        await producer.stop()
        
    
