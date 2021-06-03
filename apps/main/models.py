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
    Field('bio'),
)

db.define_table(
    'reviews',
    Field('property_manager_id', 'reference propertyManager'),
    Field('content', requires=IS_NOT_EMPTY()),
    Field('stars', 'integer'),
    Field('name', default=get_user_name()),
    Field('user_email', default=get_user_email()),
    Field('day'),
)

db.define_table(
    'savedReviews',
    Field('user_id', 'reference user'),
    Field('review_id', 'reference reviews'),
)

db.define_table(
    'userRatingReview',
    Field('user_id', 'reference user'),
    Field('review_id', 'reference reviews'),
    Field('upvoted', 'boolean'),
)

db.commit()
