import asyncio
import os
from uuid import uuid4
from agents import send_message


async def main():
    basin = os.environ.get("MY_BASIN")
    stream = os.environ.get("MY_STREAM")
    session = str(uuid4())[:8]
    
    while True:
        user_input = input(f"[{session}] > ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        if user_input:
            reply = await send_message(basin, stream, user_input)
            print(f"{reply}\n")


if __name__ == "__main__":
    asyncio.run(main())
