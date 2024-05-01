from flask import Blueprint, render_template

login_page_bp = Blueprint('login', __name__)

@login_page_bp.route('/login')
def login_page():
    """
    metodo post per gestione login
    """
    #return render_template("Login_Page_Template")
    return "@TODO: Login page"