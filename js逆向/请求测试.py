import asyncio
import aiohttp
import random
import string
import time

# 按照 API 的要求构造请求参数
api_url = 'http://localhost:5000/get_sign'

async def send_request(session, url, data):
    async with session.post(url, data=data) as response:
        print(await response.text())

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):
            timestamp_ms = str(int(time.time() * 1000))
            input_content = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            print(f"timestamp_ms: {timestamp_ms}, input_content: {input_content}")
            payload = {
                'timestamp_ms': timestamp_ms,
                'input_content': input_content
            }
            task = asyncio.ensure_future(send_request(session, api_url, payload))
            tasks.append(task)
        await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

