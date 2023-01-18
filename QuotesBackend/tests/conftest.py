import pytest 
import http.client 
from quotes_backend import create_app
from quotes_backend import token_validation
from faker import faker
fake = Faker()

@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    application.db.create_all()

    return application


@pytest.fixture
def quote_fixture(client):
    '''
    Generate 4 quotes in the system
    '''

    quote_ids = []
    for _ in range(4):
        quote = {
            'text': fake.text(120),
        }
        header = token_validation.generate_token_header(fake.name(), PRIVATE_KEY)

        headers = {
            'Authorization': header,
        }
        response = client.post('/api/me/quotes/', data=quote, headers=headers)
        assert http.client.CREATED == response.status_code
        result = response.json
        quote_ids.append(result['id'])

    yield quote_ids

    # Clean up all the quotes
    response = client.get('/api/quotes/')
    quotes = response.json
    for quote in quotes:
        quote_id = quote['id']
        url = f'/admin/quotes/{quote_id}'
        response = client.delete(url)
        assert http.client.NO_CONTENT == response.status_code