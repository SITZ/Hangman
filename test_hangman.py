import pytest
import hangman
from bs4 import BeautifulSoup


@pytest.fixture
def client():
    hangman.app.config['TESTING'] = True
    client = hangman.app.test_client()

    yield client


def test_demo():
    assert True


def test_about(client):
    rv = client.get('/about')

    assert 200 == rv._status_code

    active_link = BeautifulSoup(rv.data, 'html.parser').body.find('a', attrs={'class': 'nav-item nav-link active'})

    # Validate active link correctly indicates /about page
    assert active_link.get('href') == '/about'


def test_api(client):
    rv = client.get('/api')

    assert 200 == rv._status_code

    active_link = BeautifulSoup(rv.data, 'html.parser').body.find('a', attrs={'class': 'nav-item nav-link active'})

    # Validate active link correctly indicates /api page
    assert active_link.get('href') == '/api'


def test_index(client):
    rv = client.get('/')

    assert 200 == rv._status_code

    soup = BeautifulSoup(rv.data, 'html.parser')

    # All possible input buttons (26 alphabets + 10 digits + 1 reset) count match
    assert 37 == len(soup.find_all('form'))

    # Hangman display area is visible to user
    assert '_ ' in soup.find('span', attrs={'class': 'display-1'}).text

    # Reset button is available to user
    assert 0 <= len(soup.find('form', attrs={'action': '/reset'}))


def test_reset(client):
    rv = client.post('/reset')

    assert 302 == rv._status_code

    rv = client.post('/reset', follow_redirects=True)

    assert 200 == rv._status_code

    soup = BeautifulSoup(rv.data, 'html.parser')

    # Hangman display area is cleared
    assert set(' _') == set(soup.find('span', attrs={'class': 'display-1'}).text.strip())

    # All input buttons are enabled
    input_buttons = soup.find_all('button', attrs={'class': 'btn-secondary'})
    assert 36 == len(input_buttons)

    for input_button in input_buttons:
        assert 'disabled' not in input_button.attrs


def test_guess(client):
    rv = client.post('/guess/0')

    assert 302 == rv._status_code

    rv = client.post('/guess/0', follow_redirects=True)

    assert 200 == rv._status_code

    soup = BeautifulSoup(rv.data, 'html.parser')

    # Guessed input should still be visible
    form_0 = soup.find('form', attrs={'action': '/guess/0'})
    assert 0 < len(form_0)

    # Guessed input should be further disabled
    button_0 = form_0.select('button')[0]
    assert 'disabled' in button_0.attrs

    # Guessed input's text content is correct
    text_0 = button_0.get_text(strip=True)
    assert '0' == text_0
