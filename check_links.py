import asyncio
import aiohttp


async def check_links(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(await response.text())

if __name__=="__main__":
    url = input("Ввндите url: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_links(url))
   
    
