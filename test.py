

import asyncio
from core.schema import schema

async def main(schema):
    subscription = 'subscription { showTime }'
    result = await schema.subscribe(subscription)
    async for item in result:
        print(item.data['showTime'])

asyncio.run(main(schema))