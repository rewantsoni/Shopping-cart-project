from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,current_app
)
from werkzeug.exceptions import abort
import random
from flaskr.auth.auth import login_required
from flaskr.database.db_user import getuser,update_credit
import flaskr.database.db_product as db_product
import flaskr.database.db_incart as db_incart
import flaskr.database.db_order_id as db_order_id
import flaskr.database.db_payment as db_payment

bp = Blueprint('payment', __name__)
@bp.route('/<username>/payment/', methods=('GET', 'POST'))
@login_required
def index(username):
    user= getuser(username)
    incart = db_incart.getincart(username)
    total=db_product.getcost(incart)
    product = db_product.get_product_from_id(incart)
    if request.method =='POST':
        if request.form['action'] == 'Pay':
            card_no=request.form['card_number']
            card_exp=request.form['card_expire_date']
            if not (str(card_no) == str(user['card_number']) or str(card_exp) == str(user['card_expire_date'])):
                flash("Invalid details")
            else:
                db_incart.delete_incart_id(user['id'])
                order_id = db_order_id.update_order_id(user['id'],incart)
                db_payment.update_payment(order_id,total)
                update_credit(user['id'],max(0,total-user['credit']))
                flash("Thank You! Your Shipment will be delivered in few Hours! Shop more!")
                return redirect(url_for('home.loggedindex',username=username))
    return render_template('payment/payment.html',user=user,products=product,total=total)