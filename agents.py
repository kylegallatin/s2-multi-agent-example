import asyncio
import json
import os
from streamstore import S2
from streamstore.schemas import AppendInput, Record, ReadLimit, TailOffset
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def send_message(basin_name: str, stream_name: str, message: str) -> str:
    async with S2(access_token=os.environ.get("S2_ACCESS_TOKEN")) as s2:
        basin = s2.basin(basin_name)
        stream = basin[stream_name]
        
        try:
            await basin.get_stream_config(stream_name)
        except:
            await basin.create_stream(stream_name)
        
        user_record = Record(body=json.dumps({"role": "user", "content": message}).encode())
        await stream.append(AppendInput([user_record]))
        
        result = await stream.read(TailOffset(100), limit=ReadLimit(count=100))
        messages = []
        if isinstance(result, list):
            for record in result:
                data = json.loads(record.body)
                if data.get("role"):
                    messages.append({"role": data["role"], "content": data["content"]})
        
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4o-mini",
            messages=messages,
            store=True
        )
        
        reply = response.choices[0].message.content
        assistant_record = Record(body=json.dumps({"role": "assistant", "content": reply}).encode())
        await stream.append(AppendInput([assistant_record]))
        
        return reply

