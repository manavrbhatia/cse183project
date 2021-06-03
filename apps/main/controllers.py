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
from .models import get_user_email, get_user_name
from py4web.utils.form import Form, FormStyleBulma
from datetime import date
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
        set_rating_url = URL('set_rating', signer=url_signer),
        get_rating_url = URL('get_rating', signer=url_signer),
        mid = -1
    )

@action('search', method=["GET"])
@action.uses(url_signer.verify())
def search():
    q = request.params.get("q")
    is_address = request.params.get("is_address")
    # redirect(URL('results', q, is_address)) #also need type
    return dict(url=URL('results', q, is_address))

@action('propertyFull/<mid:int>',method=['GET', 'POST'])
@action.uses(db, auth, 'property.html')
def property(mid=None): # pass in the prop manager id 
    assert mid is not None
    star = []
    manager_info = db(db.propertyManager.id == mid).select().as_list()
    for row in db(db.reviews.property_manager_id == mid).select(db.reviews.stars):
        star.append(row.stars)
    if len(star) is not 0:
        avgstars = round(sum(star) / len(star))
    else: 
        avgstars = 0
    db.propertyManager.update_or_insert((db.propertyManager.id == mid), averageRating=avgstars)
    return dict(mid=mid, name=manager_info[0]['name'], avgstars=avgstars, city=manager_info[0]['city'], state=manager_info[0]['state'], zip=manager_info[0]['zip'],
    add_post_url=URL('add_post', signer=url_signer),
    load_posts_url=URL('load_posts', signer=url_signer),
    load_search_results_url = URL('load_results', signer=url_signer),
    set_rating_url = URL('set_rating', signer=url_signer),
    get_rating_url = URL('get_rating', signer=url_signer),)

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
    print("im in results")
    print(query)
    print(is_address)
    # redirect(URL('property'))
    return dict(my_callback_url = URL('my_callback', signer=url_signer),
    load_search_results_url = URL('load_results', query, is_address, signer=url_signer),
    property_url=URL('property', signer=url_signer),
    load_property_url=URL('load-property', signer=url_signer),
    load_posts_url=URL('load_posts', signer=url_signer),
    set_rating_url = URL('set_rating', signer=url_signer),
    get_rating_url = URL('get_rating', signer=url_signer),
    query=query,
    is_address=is_address,
    mid=-1)

@action('load_results/<query>/<is_address:int>')
@action.uses(url_signer.verify(), db)
def load_results(query=None, is_address=None):
    assert query is not None and is_address is not None
    manager_list = None
    if not query:
        manager_list = db(db.propertyManager).select().as_list()
    else:
        if is_address:
            address_arr = [s.strip() for s in query.split(',')]
            if len(address_arr) == 3:
                manager_list = db((db.propertyManager.city == address_arr[0]) & (db.propertyManager.state == address_arr[1]) & (db.propertyManager.zip == address_arr[2])).select().as_list()
            else:
                # entering bad input, should probably have smoething to deal with that, for now just make it empty
                manager_list = db(db.propertyManager.id == -1).select().as_list()
        else:
            # if it's anywhere in the name param
            manager_list = db(db.propertyManager.name.contains([query], all=True)).select().as_list()
    return dict(manager_list=manager_list)

@action('add_post', method='POST')
@action.uses(auth, url_signer.verify(), db)
def add_post():
    today = date.today()
    d1 = today.strftime("%m/%d/%Y")
    print(d1)
    id = db.reviews.insert(
        content=request.json.get('content'),
        stars=request.json.get('stars'),
        property_manager_id=request.json.get('mid'),
        name=get_user_name(),
        user_email=get_user_email(),
        day=d1,
    )
    return dict(
        id=id,
        name=get_user_name(),
        email=get_user_email(),
        day=d1,
    )

@action('load_posts')
@action.uses(auth, url_signer.verify(), db)
def load_posts():
    rows = db(db.reviews).select().as_list()
    return dict(rows= rows,)

@action('add', method=['GET','POST'])
@action.uses(db, session, auth.user, 'add.html')
def add():
    form = Form(db.propertyManager, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('set_rating', method="POST")
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    post_id = request.json.get('post_id')
    rating = request.json.get('rating')
    likers = request.json.get('likers')
    dislikers = request.json.get('dislikers')
    print(post_id)
    db.thumbs.update_or_insert(
        ((db.thumbs.post_id == post_id)  & (db.thumbs.email== get_user_email())),
        post_id = post_id,
        email = get_user_email(),
        rating = rating,
    )
    db.reviews.update_or_insert(
        (db.reviews.id == post_id),
        likers=likers,
        dislikers=dislikers,
    )
    return "ok"

@action('get_rating')
@action.uses(url_signer.verify(), db, auth.user)
def get_rating():
    post_id = int(request.params.get('post_id'))
    row = db((db.thumbs.post_id == post_id) & (db.thumbs.email == get_user_email())).select().first()
    rating = row.rating if row is not None else 4
    row2 = db(db.reviews.id == post_id).select().first()
    likers = row2.likers
    dislikers = row2.dislikers
    return dict(rating=rating, likers=likers, dislikers=dislikers)