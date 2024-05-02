from flask import Flask, render_template, request, Blueprint


# pagina della lista prodotti

root_page_bp = Blueprint('root', __name__)

@root_page_bp.route('/')
def root ():

    return """root page"""
