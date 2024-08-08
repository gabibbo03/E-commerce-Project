from extention import *
from flask import render_template,Blueprint
from sqlalchemy.orm import Session
from sqlclass import *

# pagina della lista prodotti

root_page_bp = Blueprint('root', __name__)

@root_page_bp.route('/')
def root ():

    with Session(engine) as s:
        prodotti = s.query(Prodotti).all()

    _prodotti = []
    img_src = []
    for p in prodotti:
        get_images_for_products(_prodotti, p, img_src)

    s.commit()

    return render_template("list_of_products_page_template.html", products=_prodotti, img_src=img_src, zip=zip)


