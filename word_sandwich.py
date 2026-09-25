import flask
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from slugify import slugify
from livereload import Server
from url_normalize import url_normalize
import url_transforms
import time
import logging
import random

app = flask.Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1'
]

# Function to normalize and encode URLs
def normalize_and_encode_url(url):
    return url_normalize(url)

@app.route('/')
def index():
    url = flask.request.args.get('q')
    if not url:
        return flask.render_template('no-url.html')

    try:
        res = requests.get(normalize_and_encode_url(url))
        soup = BeautifulSoup(res.text, features="html.parser")
        links = [urljoin(url, anchor.get('href')) for anchor in soup.find_all('a')]
    except Exception as e:
        return flask.render_template('error.html', error=str(e))

    sites = {}
    for raw_link in links:
        link = url_transforms.apply(raw_link)
        if link == '__ANTI_INCEPTION__' or link == '__ANTI_ANCHOR__':
            continue
        key = slugify(link)
        sites[key] = {
            'src': link,
            'title': raw_link
        }

    return flask.render_template('index.html', sites=sites)

@app.route('/fetch')
def fetch():
    link = flask.request.args.get('url')
    data = {}

    # Rotate the User-Agent for diverse behavior
    user_agent = random.choice(user_agents)

    headers = {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    # Normalize the URL
    normalized_link = normalize_and_encode_url(link)
    app.logger.debug(f"Normalized URL: {normalized_link}")

    try:
        if flask.request.host_url == normalized_link:
            raise requests.HTTPError('Transgreption!')

        app.logger.debug(f"Fetching URL: {normalized_link} with user-agent: {str(user_agent)}")
        response = requests.get(normalized_link, headers=headers)
        response.raise_for_status()
        content_type = response.headers.get('content-type')

        app.logger.debug(f"Fetched URL: {normalized_link} with status code: {response.status_code} and content type: {content_type}")

        if content_type.startswith('text/html'):
            link_soup = BeautifulSoup(response.text, features="html.parser")
            data['title'] = ''.join(str(tag) for tag in link_soup.find('title'))
            data['body'] = ''.join(str(tag) for tag in link_soup.body)
        elif content_type.startswith('text/plain'):
            data['body'] = response.text
        else:
            raise requests.HTTPError('Wrong content type')

    except Exception as e:
        app.logger.error(f"Error fetching URL: {normalized_link} - {e}")
        data['body'] = str(e)
        return data, 500

    return data

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.watch('static/*')  # Watch static files for livereload
    server.serve()