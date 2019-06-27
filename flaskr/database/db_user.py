import sqlite3
import click
from flask import current_app, g,flash
from flask.cli import with_appcontext

def get_db():
    # if 'db' not in g:
    g.db = sqlite3.connect(
        current_app.config['DATABASE_USER'],
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
    with current_app.open_resource('schema/schema_user.sql') as f:
        db.executescript(f.read().decode('utf8'))

def getuser_id(username):
    user= get_db().execute(
        'SELECT id FROM user WHERE username = ?',(username,)
        ).fetchone()
    return user

def getusername_id(id):
    user= get_db().execute(
        'SELECT username FROM user WHERE id = ?', (id,)
        ).fetchone()
    return user
    close_db()
def getuser_id_from_email(email):
    user= get_db().execute(
        'SELECT id FROM user WHERE email = ?',(email,)
        ).fetchone()
    return user
def getuser(username):
    user= get_db().execute(
        'SELECT * FROM user WHERE username = ?',(username,)
        ).fetchone()
    return user
    close_db()
def register_user(user):
    db=get_db()
    db.execute(
        'INSERT INTO user (username, email, password, card_number, card_expire_date, address, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (user['username'], user['email'], user['password'], user['card_number'], user['card_expire_date'], user['address'], user['phone_number'])
        )
    db.commit()
    close_db()

def update_credit(user,new):
    db=get_db()
    db.execute('UPDATE user SET credit = ?  WHERE id = ?',(new, user))
    db.commit()
    db.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the User database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)