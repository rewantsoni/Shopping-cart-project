import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flaskr.database.db_user import getuser_id

def get_dbincart():
    # if 'db' not in g:
    g.db = sqlite3.connect(
        current_app.config['DATABASE_INCART'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
def init_db():
    db = get_dbincart()

    with current_app.open_resource('schema/schema_incart.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get(id,user):
    return get_dbincart().execute(
        'SELECT * FROM incart WHERE (product_id,cart_id) = (?,?)', (id,getuser_id(user)['id'])
        ).fetchone()

def getcount(user):
    return get_dbincart().execute(
        'SELECT COUNT(*) FROM incart WHERE cart_id  = ?', (getuser_id(user)['id'],)
        ).fetchone();

def getincart(user):
    return get_dbincart().execute(
        'SELECT product_id FROM incart WHERE cart_id = ?', (getuser_id(user)['id'],)
        ).fetchall()
    
def delete_incart_id(id):
    db=get_dbincart()
    db.execute('DELETE FROM incart WHERE cart_id = ?', (id,))
    db.commit()
    db.close()

def delete_incart(user,id):
    db=get_dbincart()
    db.execute('DELETE FROM incart WHERE (product_id,cart_id) = (?,?)', (id,getuser_id(user)['id']))
    db.commit()
    db.close()

def addtocart(user,id):
    db=get_dbincart()
    error = None
    if get(id,user) is not None:
        error = 'Product is already in Cart.'
    if error is None:
        db.execute('INSERT INTO incart (product_id,cart_id) VALUES (?,?)',(id,getuser_id(user)['id']))
        db.commit()
        db.close()
        error="Added to cart"
    return error

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the Incart database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)