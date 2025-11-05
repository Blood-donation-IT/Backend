import asyncio
import json
import os
import grpc

# from src.infrastructure.grpc.application_management_server import ApplicationManagementService
# from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
# from src.infrastructure.repositories.sqlalchemy_application_repository import SQlAlchemyUserRepository
# from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
# from src.infrastructure.repositories.factory import get_application_repo
# from contracts.application_management import application_management_pb2_grpc
# from src.application.use_cases.create_application import CreateApplicationUseCase
# from src.application.use_cases.update_application import UpdateApplicationUseCase
# from src.application.use_cases.get_application import GetApplicationUseCase

#----
from pydantic import BaseModel,ValidationError
from aiokafka import AIOKafkaConsumer
import sys
class UserRegisteredEvent(BaseModel):
    user_id: int
    email: str
    blood_type: str
    
async def run_kafka_consumer() -> None:
    consumer = None
    while consumer is None:
        try:
            consumer = AIOKafkaConsumer(
                "user_registered",
                bootstrap_servers="kafka:9092",
                group_id="temp_verification_group",
                retry_backoff_ms=5000,
                enable_auto_commit=False
                
            )    
            
            print("Kafka consumer connected successfully.",file=sys.stderr)
            await consumer.start()
        except Exception as e:
            print(f"Kafka Consumer failed to start (retrying...): {e}", file=sys.stderr)
            if consumer:
                await consumer.stop()
            consumer = None
            await asyncio.sleep(5)
            
    print("Dirty Kafka Consumer started. Waiting for messages...", file=sys.stderr)
    try:
        async for msg in consumer:
            print("Testing message reception...", file=sys.stderr)
            print(f"Received message: {msg.value.decode('utf-8')}", file=sys.stderr)
            try:
                data = json.loads(msg.value.decode("utf-8"))
                event= UserRegisteredEvent(**data)
                print(f"SUCCESS! Parsed event for user_id: {event.user_id}", file=sys.stderr)
                print(f"Data: {event.model_dump_json()}", file=sys.stderr)
                await asyncio.sleep(1) # Даємо логу вивестися
                
                # os._exit(1) - це "жорстке вбивство" процесу.
                # Блок 'finally' НЕ буде виконаний.
                # 'await consumer.commit()' НЕ буде викликаний.
                # os._exit(1)
                await consumer.commit()
            except ValidationError as e:
                print(f"ERROR: Received invalid data: {e}", file=sys.stderr)
            except Exception as e:
                print(f"ERROR: Could not process message: {e}", file=sys.stderr)
            
            print(f"-----------------------------\n", file=sys.stderr)
    finally:
        if consumer:
            await consumer.stop()
        print("Dirty Kafka Consumer stopped.", file=sys.stderr)
            
    
#---

async def serve() -> None:
    # server = grpc.aio.server()
    # async with get_application_repo() as repo:
    #     id_gen = SnowflakeIDGenerator(instance=2)  
    #     create_use_case = CreateApplicationUseCase(repository=repo, id_generator=id_gen)
    #     update_use_case = UpdateApplicationUseCase(repository=repo)
    #     get_use_case = GetApplicationUseCase(repository=repo)

    #     application_management_service = ApplicationManagementService(
    #         create_use_case=create_use_case,
    #         update_use_case=update_use_case,
    #         get_use_case=get_use_case
    #     )

    #     application_management_pb2_grpc.add_ApplicationManagementServiceServicer_to_server(application_management_service, server)
    #     server.add_insecure_port("[::]:50052")  
        print("Async gRPC server started on port 50052")
        # await server.start()
        # await server.wait_for_termination()

async def main()->None:
    grpc_task = asyncio.create_task(serve())
    
    kafka_task = asyncio.create_task(run_kafka_consumer())
    
    
    await asyncio.gather(kafka_task)

if __name__ == "__main__":
    asyncio.run(run_kafka_consumer())