import sys
from src.domain.events.base import DomainEvent
from src.domain.services.i_event_publisher import IEventPublisher
from aiokafka import AIOKafkaProducer
class KafkaEventPublisher(IEventPublisher):
    def __init__(self, producer:AIOKafkaProducer):
        self._producer = producer
    async def publish(self, event:DomainEvent, topic:str) -> None:
        message = event.model_dump_json().encode('utf-8')
        try:
            await self._producer.send_and_wait(topic,message)
        except Exception as e:
            #TODO: Implement proper logging
            #TODO: implement retry mechanism
            #TODO: implement dead-letter queue
            print(f"CRITICAL: Error publishing event to Kafka: {e}", file=sys.stderr)
        