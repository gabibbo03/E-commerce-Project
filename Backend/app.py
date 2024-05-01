from flask import Flask
from login_page import login_page_bp
from product_page import product_page_bp
from search_page import search_page_bp

app = Flask(__name__, template_folder='../Frontend/Templates')

app.register_blueprint(login_page_bp)
app.register_blueprint(product_page_bp)
app.register_blueprint(search_page_bp)


if __name__ == "__main__":
    app.run()