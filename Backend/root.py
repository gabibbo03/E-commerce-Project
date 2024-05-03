from flask import Flask, render_template, request, Blueprint,session


# pagina della lista prodotti

root_page_bp = Blueprint('root', __name__)

@root_page_bp.route('/')
def root ():
     
    return render_template('Home_Page.html')
