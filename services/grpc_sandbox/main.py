import asyncio
import sys
from src.clients.user_profile_client import UserProfileClient
from faker import Faker

async def run():
    client = UserProfileClient()
    fake = Faker()
    
    resp = await client.create_profile(fake.name(), fake.email(), fake.phone_number())
    print(f"Response: {resp}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(run())