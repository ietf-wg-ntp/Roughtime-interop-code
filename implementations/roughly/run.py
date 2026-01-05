#!/usr/bin/env python3

import asyncio
import base64

from roughly import send_request


async def main():
    try:
        async with asyncio.timeout(1):
            response = await send_request(
                host="roughtime-server",
                port=2002,
                public_key=base64.b64decode(b"Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE="),
            )
            print("yay!")
    except Exception as e:
        print(f":( {e})")

if __name__ == "__main__":
    asyncio.run(main())