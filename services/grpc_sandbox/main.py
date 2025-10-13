import asyncio
import sys
from src.clients.user_profile_client import UserProfileClient

async def run():
    client = UserProfileClient()
    resp = await client.create_profile("Test User", "test@example.com", "1234567890")
    print(f"Response: {resp}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(run())