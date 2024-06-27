import aiohttp

# Web settings
root_address = "https://dokapp-server.vercel.app/"
# root_address = "http://127.0.0.1:8000"


# Выбор работы по сети или локально
async def set_the_connection():
    try:
        session = aiohttp.ClientSession(root_address)

        # Checking out the connection
        async with session.get('/') as resp:
            print(resp.status)
            json_content = await resp.json()
            print(json_content)

    except aiohttp.ClientConnectorError:
        session = None
        print('Started in local mode')
    return session
