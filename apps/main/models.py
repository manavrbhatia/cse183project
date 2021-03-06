"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_name():
    return auth.current_user.get('first_name') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


db.define_table(
    'user',
    Field('user_email', default=get_user_email),
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('last_name', requires=IS_NOT_EMPTY()),
    Field('age', 'integer'),
    Field('location'),
)

db.define_table(
    'propertyManager',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('city', requires=IS_NOT_EMPTY()),
    Field('state', requires=IS_NOT_EMPTY()),
    Field('zip', 'integer'),
    Field('averageRating', 'integer'),
    Field('bio'),
    Field('img_str', 'text'),
)
db.propertyManager.img_str.readable = db.propertyManager.img_str.writable = False

db.define_table(
    'reviews',
    Field('property_manager_id', 'reference propertyManager'),
    Field('content', requires=IS_NOT_EMPTY()),
    Field('stars', 'integer'),
    Field('name', default=get_user_name()),
    Field('user_email', default=get_user_email()),
    Field('day'),
    Field('likers', 'integer', default=0),
    Field('dislikers', 'integer', default=0),
)

db.define_table(
    'savedReviews',
    Field('user_id', 'reference user'),
    Field('review_id', 'reference reviews'),
)

db.define_table('thumbs',
    Field('post_id', 'reference reviews'),
    Field('email', requires=IS_NOT_EMPTY()),
    Field('rating', 'integer', default=4),
)
db.propertyManager.averageRating.readable = db.propertyManager.averageRating.writable = False

db.commit()
