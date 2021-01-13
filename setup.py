# run this once to create SQLite tables

from url_shortener import create_app
from url_shortener.extensions import db
from url_shortener.models import Link

# make necessary changes in settings.py, give the database URI as is, from .env file.

db.create_all(app=create_app())

# the yml file was got like this:
# conda env export | grep -v "^prefix: " > environment.yml