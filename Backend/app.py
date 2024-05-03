from flask import Flask
from user_management import login_page_bp,sign_in_page_bp,logout_page_bp,dashboard_bp
from product_page import product_page_bp
from search_page import search_page_bp
from root import root_page_bp


def create_app():
    
    app = Flask(__name__,template_folder='../Frontend/Templates')
    app.register_blueprint(login_page_bp)
    app.register_blueprint(logout_page_bp)
    app.register_blueprint(sign_in_page_bp)
    app.register_blueprint(dashboard_bp)
    #app.register_blueprint(product_page_bp)
    app.register_blueprint(search_page_bp)
    app.register_blueprint(root_page_bp)
    app.secret_key = "@todo"
    return app


if __name__ == "__main__":

    app = create_app()
    app.run(debug=True)
    
    