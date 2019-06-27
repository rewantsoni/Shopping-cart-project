from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth.auth import login_required
import flaskr.database.db_incart as db_incart
import flaskr.database.db_product as db_product

bp = Blueprint('home', __name__)
@bp.route('/',methods=('GET', 'POST'))
def index():
    products = db_product.getall()
    if request.method =='POST':
        return redirect(url_for('login.login'))
    return render_template('category/index.html', products=products)

@bp.route('/user/<username>', methods=('GET', 'POST'))
@login_required
def loggedindex(username):
    products = db_product.getall()
    if request.method =='POST':
        if request.form['action'] == 'Buy Now':
            error= db_incart.addtocart(username,request.form['id'])
            return redirect(url_for('mycart.index',username=username))
        elif request.form['action'] =='Add to Cart':
            error = db_incart.addtocart(username,request.form['id'])
            flash(error)
            return redirect(url_for('home.loggedindex',username=username))
    return render_template('category/index.html', products=products,user=username)