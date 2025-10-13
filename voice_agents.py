import asyncio
import json
import os
from streamstore import S2
from streamstore.schemas import AppendInput, Record, ReadLimit, TailOffset
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

REALTIME_MODEL = os.environ.get("REALTIME_MODEL", "gpt-realtime-mini")


async def send_realtime_message(basin_name: str, stream_name: str, message: str) -> str:
    async with S2(access_token=os.environ.get("S2_ACCESS_TOKEN")) as s2:
        basin = s2.basin(basin_name)
        stream = basin[stream_name]
        
        try:
            await basin.get_stream_config(stream_name)
        except:
            await basin.create_stream(stream_name)
        
        result = await stream.read(TailOffset(20), limit=ReadLimit(count=20))
        conversation_items = []
        if isinstance(result, list):
            for record in result:
                data = json.loads(record.body)
                if data.get("role"):
                    conversation_items.append({
                        "type": "message",
                        "role": data["role"],
                        "content": [{"type": "input_text", "text": data["content"]}]
                    })
        
        async with client.beta.realtime.connect(model=REALTIME_MODEL) as connection:
            await connection.session.update(session={
                "modalities": ["text"],
                "instructions": "You are a helpful debugging assistant. Multiple developers may be using you simultaneously to debug issues."
            })
            
            for item in conversation_items:
                await connection.conversation.item.create(item=item)
            
            user_item = {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": message}]
            }
            await connection.conversation.item.create(item=user_item)
            
            user_record = Record(
                body=json.dumps({"role": "user", "content": message}).encode()
            )
            await stream.append(AppendInput([user_record]))
            
            await connection.response.create()
            
            reply_text = ""
            
            async for event in connection:
                if event.type == "response.text.delta":
                    reply_text += event.delta
                elif event.type == "response.text.done":
                    reply_text = event.text
                elif event.type == "response.done":
                    break
            
            assistant_record = Record(
                body=json.dumps({"role": "assistant", "content": reply_text}).encode()
            )
            await stream.append(AppendInput([assistant_record]))
            
            return reply_text

