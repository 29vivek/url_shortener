import string
from datetime import datetime
from base64 import b64encode
from hashlib import blake2b
import random

from .extensions import db 

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(12), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link(self.original_url)

    def generate_short_link(self, url):
        """
        Shortens a url by generating a 9 byte hash, and then
        converting it to a 12 character long base 64 url friendly string.

        Parameters:
        url - the url to be shortened.

        Return values:
        String, the unique shortened url, acting as a key for the entered long url.
        """
        url_hash = blake2b(str.encode(url), digest_size=9)
        b64 = b64encode(url_hash.digest(), altchars=b'-_').decode('utf-8')

        already_shortened = self.query.filter_by(short_url=b64).first()

        if already_shortened:
            url += str(random.randint(0, 9))
            return self.generate_short_link(url)
        
        return b64