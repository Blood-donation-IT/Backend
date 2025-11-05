import asyncio
import sys
from src.clients.user_profile_client import UserProfileClient
from faker import Faker

async def run():
    try:
        client = UserProfileClient()
        for _ in range(100000):
            fake = Faker()
            
            resp = await client.create_profile(fake.name()+"3", str(fake.email())+"3", str(fake.phone_number())+"3")
            print(f"Response: {resp}", file=sys.stderr)
    except Exception as e:
        print(f"Error during client operation", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(run())