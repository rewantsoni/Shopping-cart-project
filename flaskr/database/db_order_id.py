import sqlite3
import random
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flaskr.database.db_user import getuser_id


def get_db():
    # if 'db' not in g:
    g.db = sqlite3.connect(
        current_app.config['DATABASE_ORDER_ID'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
def init_db():
    db = get_db()

    with current_app.open_resource('schema/schema_order_id.sql') as f:
        db.executescript(f.read().decode('utf8'))

def update_order_id(user_id,product):
    db=get_db()
    orderid='OD'+str(user_id)+""+str(random.randint(1000,1998292998))
    for each in product:
        db.execute('INSERT INTO order_id (id,product_id,user_id) VALUES (?,?,?)',(orderid,each['product_id'],user_id))
        db.commit()
    db.close()
    return orderid

def getcount(user):
    return get_db().execute(
        'SELECT COUNT(*) FROM order_id WHERE user_id  = ?', (getuser_id(user)['id'],)
        ).fetchone();

def getincart(user):
    return get_db().execute(
        'SELECT product_id FROM order_id WHERE user_id = ?', (getuser_id(user)['id'],)
        ).fetchall()
    

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the Order_ID database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)