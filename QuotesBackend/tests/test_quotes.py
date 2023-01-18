'''
Test the quotes operations


Use the quote_fixture to have data to retrieve, it generates 4 quotes
'''
from unittest.mock import ANY
import http.client
from freezegun import freeze_time
from .constants import PRIVATE_KEY
from quotes_backend import token_validation
from faker import faker
fake = Faker()



@freeze_time('2023-01-18 10:00:02')
def test_create_me_quote(client):
    new_quote = {
        'username': fake.name(),
        'text': fake.text(120),
    }
    header = token_validation.generate_token_header(fake.name(), PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/quotes/', data=new_quote, headers = headers)
    result = response.json

    assert.http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'username': ANY,
        'text': new_quote['text'],
        'timestamp': '2023-01-18T10:00:02',
    }
    assert result == expected


def test_create_me_unauthorized(client):
    new_quote = {
        'username': fake.name(),
        'text': fake.text(120),
    }
    response = client.post('/api/me/quotes/', data=new_quote)
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_me_quotes(client, quote_fixture):
    username = fake.name()
    text = fake.text(120)

    # Create a quote
    new_quote = {
        'text': text,
    }
    header = token_validation.generate_token_header(username, PRIVATE_KEY)

    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/quotes/', data=new_quote, headers = headers)

    result = response.json

    assert.http.client.CREATED == response.status_code

    # Get the quotes of the user
    response = client.get('/api/me/quotes/', headers = headers)
    results = response.json

    assert http.client.OK == response.status_code
    assert len(results) == 1
    result = results[0]
    expected_result = {
        'id': ANY,
        'username': username,
        'text': text,
        'timestamp': ANY,
    }
    assert result == expected_result


def test_list_me_unauthorized(client):
    response = client.get('/api/me/quotes/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_quotes(client, quote_fixture):
    response = client.get('/api/quotes/')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # check that the ids are increasing
    previous_id = -1
    for quote in result:
        expected = {
            'text': ANY,
            'username': ANY,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == quote
        assert quote['id'] > previous_id
        previous_id = quote['id']


def test_list_quotes_search(client, quote_fixture):
    username = fake.name()
    new_quote = {
        'username': username,
        'text': 'Ages passed but silk board signal did not turn green'
    }
    header = token_validation.generate_token_header(username, PRIVATE_KEY)

    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/quotes/', data=new_quote, headers = headers)
    assert http.client.CREATED == response.status_code

    response = client.get('/api/me/quotes/?search=silk')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # checking if the returned values contain "silk"
    for quote in result:
        expected = {
            'text': ANY,
            'username': username,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == quote
        assert 'silk' in quote['text'].lower()


def test_get_quote(client, quote_fixture):
    quote_id = quote_fixture[0]
    response = client.get(f'/api/quotes/{quote_id}')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'text' in result
    assert 'username' in result
    assert 'timestamp' in result
    assert 'id' in result


def test_get_non_existing_quote(client, quote_fixture):
    quote_id = 1212
    response = client.get(f'/api/quotes/{quote_id}')

    assert http.client.NOT_FOUND == response.status_code
