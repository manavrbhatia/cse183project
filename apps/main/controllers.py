"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

import uuid
import random

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
        load_search_results_url = URL('load_results', signer=url_signer),
        results_url = URL('results', signer=url_signer),
        search_url=URL('search', signer=url_signer),
        property_url=URL('property', signer=url_signer),
        load_posts_url=URL('load_posts', signer=url_signer),
        mid = -1
    )

@action('search', method=["GET"])
@action.uses(url_signer.verify())
def search():
    q = request.params.get("q")
    is_address = request.params.get("is_address")
    redirect(URL('results', q, is_address)) #also need type
    # return "ok"

@action('propertyFull/<mid:int>',method=['GET', 'POST'])
@action.uses(db, auth, 'property.html')
def property(mid=None): # pass in the prop manager id 
    assert mid is not None
    manager_info = db(db.propertyManager.id == mid).select().as_list()
    return dict(mid=mid, name=manager_info[0]['name'], city=manager_info[0]['city'], state=manager_info[0]['state'], zip=manager_info[0]['zip'],
    add_post_url=URL('add_post', signer=url_signer),
    load_posts_url=URL('load_posts', signer=url_signer),
    load_search_results_url = URL('load_results', signer=url_signer),)

@action('property',method=['GET', 'POST'])
@action.uses(db, auth)
def property(): # pass in the prop manager id 
    mid = request.json.get('mid')
    manager_info = db(db.propertyManager.id == mid).select().as_list()
    url = URL('propertyFull', mid)
    return dict(url=url, name=manager_info[0]['name'], city=manager_info[0]['city'], state=manager_info[0]['state'], zip=manager_info[0]['zip'],
    add_post_url=URL('add_post', signer=url_signer),
    load_posts_url=URL('load_posts', signer=url_signer),
    load_search_results_url = URL('load_results', signer=url_signer),)

@action('results/<query>/<is_address:int>', method=["GET"])
@action.uses(db, auth, 'results.html')
def results(query=None, is_address=None): # add flag for city/manager as param
    assert query is not None and is_address is not None
    print(query)
    print(is_address)
    # redirect(URL('property'))
    return dict(my_callback_url = URL('my_callback', signer=url_signer),
    load_search_results_url = URL('load_results', signer=url_signer),
    property_url=URL('property', signer=url_signer),
    load_property_url=URL('load-property', signer=url_signer),
    load_posts_url=URL('load_posts', signer=url_signer),
    query=query,
    is_address=is_address,
    mid=-1)

@action('load_results')
@action.uses(url_signer.verify(), db)
def load_results():
    manager_list = db(db.propertyManager).select().as_list()
    return dict(manager_list=manager_list)

@action('add_post', method='POST')
@action.uses(auth, url_signer.verify(), db)
def add_post():
    print(request.json.get('mid'))
    id = db.reviews.insert(
        content=request.json.get('content'),
        stars=request.json.get('stars'),
        property_manager_id=request.json.get('mid'),
        user_email=get_user_email(),
    )
    return dict(
        id=id,
        email=get_user_email(),
    )

@action('load_posts')
@action.uses(auth, url_signer.verify(), db)
def load_posts():
    rows = db(db.reviews).select().as_list()
    return dict(rows= rows,)