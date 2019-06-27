from flask import (
    Blueprint, render_template,
)
from werkzeug.exceptions import abort
from flaskr.auth.auth import login_required
from flaskr.database.db_order_id import get_db as get_db_order #TODO: want to display order id also?
import flaskr.database.db_product as db_product
import flaskr.database.db_order_id as db_order_id

bp = Blueprint('myorders', __name__,url_prefix='/orders/')

@bp.route('/<username>', methods=('GET', 'POST'))
@login_required
def index(username):
    count = db_order_id.getcount(username)
    incart = db_order_id.getincart(username)
    product = db_product.get_product_from_id(incart)
    return render_template('orders/orders.html', products=product,user=username)
