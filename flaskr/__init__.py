import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_USER=os.path.join(app.instance_path, 'database_user.sqlite'),
        DATABASE_PRODUCT=os.path.join(app.instance_path, 'database_product.sqlite'),
        DATABASE_INCART=os.path.join(app.instance_path, 'database_incart.sqlite'),
        DATABASE_ORDERS=os.path.join(app.instance_path, 'database_orders.sqlite'),
        DATABASE_ORDER_ID=os.path.join(app.instance_path, 'database_order_id.sqlite'),
        DATABASE_PAYMENT=os.path.join(app.instance_path, 'database_payment.sqlite'),

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists 
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # from flaskr.database import db_user
    # db_user.init_app(app)
    # from flaskr.database import db_product
    # db_product.init_app(app)
    # from flaskr.database import db_incart
    # db_incart.init_app(app)
    # from flaskr.database import db_orders
    # db_orders.init_app(app)
    # from flaskr.database import db_order_id
    # db_order_id.init_app(app)
    # from flaskr.database import db_payment
    # db_payment.init_app(app)

    from flaskr.auth import auth
    app.register_blueprint(auth.bp)

    from flaskr.auth import register
    app.register_blueprint(register.bp)
    from flaskr.auth import login

    app.register_blueprint(login.bp)
    from flaskr.auth import logout
    app.register_blueprint(logout.bp)

    from flaskr.category import category
    app.register_blueprint(category.bp)

    from flaskr.cart import mycart
    app.register_blueprint(mycart.bp)

    from flaskr.payment import payment
    app.register_blueprint(payment.bp)

    from flaskr.orders import myorders
    app.register_blueprint(myorders.bp)
    
    return app