import asyncio
import hashlib
import os
import tempfile

import aiohttp
import pytest

from main import download_repo_contents, download_files, hash_files


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def temp_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        files = ['file1.txt', 'file2.txt', 'file3.txt']
        for filename in files:
            filepath = os.path.join(tmpdir, filename)
            with open(filepath, 'wb') as f:
                f.write(b'Test data')
        yield tmpdir


@pytest.mark.asyncio
async def test_download_repo_contents():
    url = 'https://gitea.radium.group/radium/project-configuration'
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url}/src/ref/heads/master/') as response:
            assert response.status == 200
            assert 'Test data' in await response.text()


@pytest.mark.asyncio
async def test_download_files(temp_files):
    files = await download_files()
    assert len(files) == 9


@pytest.mark.asyncio
async def test_main(temp_files):
    files = await main()
    assert len(files) == 9
    for file in files:
        filepath = os.path.join('temp_folder', file)
        assert os.path.exists(filepath)


@pytest.mark.asyncio
async def test_hash_files(temp_files):
    results = await hash_files()
    assert len(results) == 9
    for result in results:
        assert isinstance(result, str)
        assert len(result) == 64
