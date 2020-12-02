from flask import Blueprint, render_template, request, redirect

from .extensions import db
from .models import Link

import re

def url_valid(url):
    """Validates a url by parsing it with a regular expression.

    Parameters:
    url - string representing a url to be validated.

    Return values:
    Boolean, indicating the validity of the url.
    """

    # From https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not#7160778
    # Slightly modified to not use ftp.
    regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None

short = Blueprint('short', __name__)

@short.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    if link.visits >= 5:
        return render_template('404.html', status_code=500, message=f'Shortened code {link.short_url} has exceeded number of visits ({link.visits}) and is no longer valid. '), 500

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.original_url) 

@short.route('/')
def index():
    return render_template('index.html')

@short.route('/add_link', methods=['POST'])
def add_link():
    url = request.form['original_url']
    
    if url[:4] != 'http':
        url = 'http://' + url

    if not url_valid(url):
        return render_template('404.html', status_code=400, message=f'{url} is not a valid url.'), 400

    link = Link(original_url=url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html', 
        short_url=link.short_url, original_url=link.original_url)

@short.route('/stats')
def stats():
    links = Link.query.all()

    return render_template('stats.html', links=links)

@short.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', status_code=404), 404