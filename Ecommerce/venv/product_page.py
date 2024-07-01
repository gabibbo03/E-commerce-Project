import os
from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, request, url_for
from werkzeug.utils import secure_filename

from sqlclass import engine, func
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlclass import Prodotti
from flask_login import current_user, login_required
from extention import *

product_page_bp = Blueprint('product', __name__)


@product_page_bp.route('/<int:product_id>')
def product_page(product_id):
    with  Session(engine) as s:
        p = s.get(Prodotti, product_id)
    s.close()
    folderpath = os.path.join(UPLOAD_FOLDER, str(p.autore), str(p.id_prodotto))
    if os.path.exists(folderpath) and os.path.isdir(folderpath):
        files = os.listdir(folderpath)
        files_list= []
        for f in files:
            files_list.append(os.path.join(folderpath, f))

        return render_template('Product_Page_Template.html', product=p,img=files_list)

    else:
        f = [placeholder]
        return render_template('Product_Page_Template.html', product=p,img=f)




@product_page_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def product_upload():
    if request.method == 'POST':
        # Hello from hell GNU + Richard Stallman + Linux + Anime Girl
        title = request.form['Titolo']
        content = request.form['Descrizione']
        payment_methods = request.form.getlist('payment_methods')
        price = request.form['prezzo']
        shipment = request.form['shipment']
        place = request.form.get('luogo')
        quantity = request.form['quantita']
        condition = request.form['condition']

        images = request.files.getlist('images[]')
        image_paths = []

        last_id = 0
        with Session(engine) as s:
            p = s.query(func.max(Prodotti.id_prodotto)).scalar()
            s.close()

            if p is None:
                last_id = 0
            else:
                last_id = p

        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)

                filepath = os.path.join(UPLOAD_FOLDER, str(current_user.id), str(last_id + 1))

                os.makedirs(filepath, exist_ok=True)
                filepath = os.path.join(str(filepath), str(filename))
                image.save(filepath)
                image_paths.append(filepath)

        with Session(engine) as s:

            new_prod = Prodotti(Titolo=title,
                                Descrizione=content,
                                Prezzo=price,
                                visa='visa' in payment_methods,
                                contanti='cash' in payment_methods,
                                baratto='barter' in payment_methods,
                                spedizione= shipment == 'yes',
                                luogo=place,
                                disponibilita=quantity,
                                data_pubblicazione=datetime.utcnow().date(),
                                nuovo=condition == 'yes',
                                autore=current_user.id
                                )
            s.add(new_prod)
            s.commit()


        return redirect(url_for('product.product_page', product_id=last_id + 1))
    else:
        return render_template('Upload_Form_Template.html')
