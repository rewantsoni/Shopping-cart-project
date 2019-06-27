from flask import (
    Blueprint, redirect, session, url_for
)
bp = Blueprint('logout', __name__)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))
    