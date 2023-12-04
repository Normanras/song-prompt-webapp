import asyncio
import requests


async def grab_words():
    while True:
        await asyncio.sleep(.5)
        word = str(requests.get("https://random-word-api.herokuapp.com/word").text)[2:-2]
        print(word)


async def every(__seconds: float, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(__seconds)


async def main():
    asyncio.ensure_future(grab_words())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab_words())
    loop.run_forever()
    # loop.create_task(every(1, grab_words()))
