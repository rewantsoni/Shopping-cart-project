import sqlite3

import click
from flask import current_app, g,flash
from flask.cli import with_appcontext


def get_db():
    # if 'db' not in g:
    g.db = sqlite3.connect(
        current_app.config['DATABASE_PRODUCT'],
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

    with current_app.open_resource('schema/schema_product.sql') as f:
        db.executescript(f.read().decode('utf8'))
def getall():
    return get_db().execute('SELECT * FROM product').fetchall()

def get_product_from_id(incart):
    product=[]
    for each in incart:
        product += [get_db().execute(
            'SELECT * FROM product WHERE id = ?', (each['product_id'],)
            ).fetchone()]
    return product
def getcost(incart):
    total=0
    for each in incart:
        total +=(dict(get_db().execute(
            'SELECT * FROM product WHERE id = ?', (each['product_id'],)
            ).fetchone())['cost'])
    return total

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the Product database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)