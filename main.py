import aiohttp
import asyncio
import hashlib
import os

async def download_repo_contents():
    url = 'https://gitea.radium.group/radium/project-configuration'
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url}/src/ref/heads/master/') as response:
            files = await response.text()
    return files
async def download_files():
    files = []
    tasks = []
    for i in range(3):
        task = asyncio.create_task(download_repo_contents())
        tasks.append(task)
    for result in asyncio.as_completed(tasks):
        files += await result
    return files
async def main():
    files = await download_files()
    for file in files:
        filepath = os.path.join('temp_folder', file)
        with open(filepath, 'wb') as f:
            f.write(file.content)
    return files
async def hash_files():
    files = await main()
    results = []
    for file in files:
        filepath = os.path.join('temp_folder', file)
        with open(filepath, 'rb') as f:
            contents = f.read()
        hasher = hashlib.sha256()
        hasher.update(contents)
        result = hasher.hexdigest()
        results.append(result)
    return results
