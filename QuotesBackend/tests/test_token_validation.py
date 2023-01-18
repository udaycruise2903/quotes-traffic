import delorean
from freezegun import freeze_time
from quotes_backend import token_validation
from .constants import PRIVATE_KEY, PUBLIC_KEY


INVALID_PUBLIC_KEY = '''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzFbNIq6zGCTrdecsDY8U
Hbd0tVUndqCY7E6wOwt0bH7sV3fl69QR7Mic1G5lVNNro30aBY6nZZRVy3sNEkns
9e3OL5IlcGmzzZXZFrw3NM4hRLLPAnbT6jEbBKjrR6bsN/42a3GLnEAv62/pBMEH
znQI8EEZshP+aWNvrxi4kftTHVdQlCrrgAhESZ1cWXDqJI1IlmKu7PDeDKP8ViHN
qcYiTEWOHTpefL4sFOO06KGi5ahKgnx/AuNBeQID86IA1yfGPQl9IDOPSRYA1Hn0
medsHodhFtJ+qeMsM+mnhDEblJfKG3DYrIk6EC9/Rszvh+dXruRrTDCQt5o8datP
OQIDAQAB
-----END PUBLIC KEY-----
'''


def test_encode_and_decode():
    payload = {
        'example': 'payload', 
    }

    token = token_validation.encode_token(payload, PRIVATE_KEY)
    assert payload == token_validation.deocode_token(token, PUBLIC_KEY)


def test_invalid_token_header_invalid_format():
    header = 'bad header'
    result = token_validation.validate_token_header(header, PUBLIC_KEY)
    assert None is result


def test_invalid_token_header_bad_token():
    header = 'Bearer baddata'
    result = token_validation.validate_token_header(header, PUBLIC_KEY)
    assert None is result


def test_invalid_token_no_header():
    header = None 
    result = token_validation.validate_token_header(header, PUBLIC_KEY)
    assert None is result 


def test_invalid_token_header_not_expiry_time():
    payload = {
        'username': 'uday kiran',
    }
    token = token_validation.validate_token_header(payload, PRIVATE_KEY)
    token = decode('utf8')
    header = f'Bearer{token}'
    result = token_validation.validate_token_header(header, PUBLIC_KEY)
    assert None is result


@freeze_time('2018-05-17 10:02:02')
def test_invalid_token_header_expired():
    expiry = delorean.parse('2018-05-17 10:02:00').datetime
    payload = {
        'username': 'uday kiran',
        'exp': expiry,
    }
    token = token_validation.validate_token_header(payload, PRIVATE_KEY)
    token = token.decode('utf8')
    header = f'Bearer {token}'
    result = token_validation.validate_token_header(header, PUBLIC_KEY)
    assert None is result


@freeze_time('2018-05-17 10:02:02')
def test_invalid_token_header_no_username():
    expiry = delorean.parse('2018-05-17 10:02:02').datetime
    payload = {
        'exp': expiry,
    }
    token = token_validation.validate_token_header(payload, PRIVATE_KEY)
    token = token.decode('utf8')
    header = f'Bearer {token}'
    result = token_validation.validate_token_header(header, PUBLIC_KEY)
    assert None is result


def test_valid_token_header_invalid_key():
    header = token_validation.validate_token_header('uday kiran', PRIVATE_KEY)
    result = token_validation.validate_token_header(header, INVALID_PUBLIC_KEY)
    assert None is result


def test_valid_token_header():
    header = token_validation.validate_token_header('uday kiran', PRIVATE_KEY)
    result = token_validation.validate_token_header(header, PUBLIC_KEY)
    assert 'uday kiran' == result