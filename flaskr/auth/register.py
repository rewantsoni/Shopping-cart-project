import re
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash
import flaskr.database.db_user as db_user
bp = Blueprint('register', __name__)
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        card_number = request.form['card_number']
        card_expire_date = request.form['card_expire_date']
        address = request.form['address']
        phone_number = request.form['phone_number']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        # elif not validate_email(email):
        #     error = 'Invalid Email'
        elif not phone_number:
            error = 'Phone Number is required.'
        elif not Pattern.match(phone_number):
            error = 'Invalid Phone Number'
        elif not card_number:
            error = 'Card Number is required.'
        elif not card_expire_date:
            error = 'Card Expire Date is required.'
        elif not address:
            error = 'Address is required.'
        elif db_user.getuser_id(username) is not None:
            error = 'Username {} is already registered.'.format(username)
        elif db_user.getuser_id_from_email(email) is not None:
            error = 'Email {} is already registered.'.format(email)
        if error is None:
            user={
            'username':username,
            'email':email,
            'password':generate_password_hash(password),
            'card_number':card_number,
            'card_expire_date':card_expire_date,
            'address':address,
            'phone_number':phone_number
            }
            db_user.register_user(user)
            return redirect(url_for('login.login'))
        flash(error)
    return render_template('auth/register.html')