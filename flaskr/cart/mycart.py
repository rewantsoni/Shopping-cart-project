from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth.auth import login_required
import flaskr.database.db_product as db_product
import flaskr.database.db_incart as db_incart


bp = Blueprint('mycart', __name__,url_prefix='/cart/')

@bp.route('/<username>', methods=('GET', 'POST'))
@login_required
def index(username):
    count = db_incart.getcount(username)
    incart = db_incart.getincart(username)
    product = db_product.get_product_from_id(incart)

    if request.method =='POST':
        if request.form['action'] == 'Remove from Cart':
            db_incart.delete_incart(username,request.form['id'])#only first product id? why? delete not happening properly
            return redirect(url_for('mycart.index',username=username))
        if request.form['action'] == 'Proceed to Payment':
            return redirect(url_for('payment.index',username=username))
    return render_template('cart/mycart.html', products=product,user=username,number=count[0])