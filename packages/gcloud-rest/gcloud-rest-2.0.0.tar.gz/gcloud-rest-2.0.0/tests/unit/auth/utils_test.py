import pickle

import pytest

import gcloud.rest.auth.utils as utils


@pytest.mark.parametrize('str_or_bytes', ['Hello Test',
                                          'UTF-8 Bytes'.encode('utf-8'),
                                          pickle.dumps([])])
def test_encode_decode(str_or_bytes):
    encoded = utils.encode(str_or_bytes)
    expected = str_or_bytes
    if isinstance(expected, str):
        try:
            expected = str_or_bytes.encode('utf-8')
        except UnicodeDecodeError:
            pass
    assert expected == utils.decode(encoded)
