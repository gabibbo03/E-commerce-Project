from flask import Flask
from extention import login_manager
from user_management import user_manager_bp
from product_page import product_page_bp
from search_page import search_page_bp
from root import root_page_bp

def create_app():
    
    app = Flask(__name__,template_folder='../Templates')
    app.config['SECRET_KEY'] = 'todo'
    login_manager.init_app(app)
    app.register_blueprint(user_manager_bp)
    #app.register_blueprint(product_page_bp)
    app.register_blueprint(search_page_bp)
    app.register_blueprint(root_page_bp)
    return app

if __name__ == "__main__":

    app = create_app()
    app.run(debug=True)
    
    