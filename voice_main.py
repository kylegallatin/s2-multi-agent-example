import asyncio
import os
from uuid import uuid4
from voice_agents import send_realtime_message


async def main():
    basin = os.environ.get("MY_BASIN")
    stream = os.environ.get("MY_STREAM")
    session = str(uuid4())[:8]
    
    print(f"Starting Realtime API session: {session}")
    print("Multiple users can run this script simultaneously to share context")
    print("Type 'quit' or 'exit' to end session\n")
    
    while True:
        user_input = input(f"[{session}] > ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        if user_input:
            try:
                reply = await send_realtime_message(basin, stream, user_input)
                print(f"Assistant: {reply}\n")
            except Exception as e:
                print(f"Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())


