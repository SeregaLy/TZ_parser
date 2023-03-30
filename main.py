import asyncio
import os
import aiohttp


async def download_file(url, temp_dir):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as resp:
            content_type = resp.headers.get('content-type')
            content_length = int(resp.headers.get('content-length', 0))
            file_name = f'{os.path.basename(url)}-{content_length}.{content_type.split("/")[1]}'
            file_path = os.path.join(temp_dir, file_name)
            async with session.get(url) as resp:
                with open(file_path, 'wb') as f:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)


async def download_repository():
    repository_url = 'https://gitea.radium.group/radium/project-configuration'
    temp_dir = '/tmp'
    tasks = []
    for i in range(3):
        task = asyncio.create_task(download_file(repository_url, temp_dir))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(download_repository())
