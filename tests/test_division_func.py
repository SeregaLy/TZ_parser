import asynctest
from asynctest.mock import patch, CoroutineMock, MagicMock
from hashlib import sha256
import os
import tempfile

from main import download_repo_contents, download_files, hash_files


async def test_download_repo_contents():
    mock_files = 'file1.txt\nfile2.txt\nfile3.txt\n'
    mock_response = CoroutineMock(text=mock_files)
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    mock_client_session = CoroutineMock()
    mock_client_session.return_value = mock_session

    result_files = await download_repo_contents(session=mock_client_session)

    assert result_files == ['file1.txt', 'file2.txt', 'file3.txt']


async def test_download_files():
    async def mock_download_repo_contents():
        return ['file1.txt', 'file2.txt', 'file3.txt']

    with patch('script.download_repo_contents',
               new=mock_download_repo_contents):
        result_files = await download_files()

    assert len(result_files) == 9


async def test_hash_files():
    async def mock_main():
        return ['file1.txt', 'file2.txt', 'file3.txt']

    with patch('script.main', new=mock_main):
        with tempfile.TemporaryDirectory() as tmpdir:
            # create mock files
            for filename in ['file1.txt', 'file2.txt', 'file3.txt']:
                filepath = os.path.join(tmpdir, filename)
                with open(filepath, 'wb') as f:
                    f.write(b'mock data')

            with patch('script.os.path.join',
                       side_effect=os.path.join) as mock_join:
                results = await hash_files()

            # check if sha256 hash is calculated correctly for each file
            for i in range(3):
                filepath = mock_join.return_value.return_value[i]
                with open(filepath, 'rb') as f:
                    contents = f.read()
                expected_hash = sha256(contents).hexdigest()
                assert results[i] == expected_hash
