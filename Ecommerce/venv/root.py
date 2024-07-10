from extention import *
from flask import Flask, render_template, request, Blueprint,session
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

        _prodotti.append(p)
        folderpath = os.path.join(UPLOAD_FOLDER, str(p.autore), str(p.id_prodotto))
        if os.path.exists(folderpath) and os.path.isdir(folderpath):
            files = os.listdir(folderpath)
            filepath = os.path.join(folderpath, files[0])

            img_src.append(filepath)
            print(filepath)
        else:
            img_src.append(placeholder)
            print(placeholder)

    s.commit()

    return render_template("list_of_products_page_template.html", products=_prodotti, img_src=img_src, zip=zip)


