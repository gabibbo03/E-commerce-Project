from flask import Blueprint, render_template,redirect, request, url_for
from werkzeug.utils import secure_filename
from sqlclass import engine, func, Recensioni, ProdottiRecensioni
from sqlalchemy.orm import Session
from sqlclass import Prodotti
from flask_login import current_user, login_required
from extention import *

product_page_bp = Blueprint('product', __name__)


@product_page_bp.route('/<int:product_id>')
def product_page(product_id):

    """
    solo se l'utente è loggato , viene fuori se stesso sulla
    barra di ricerca
    """


    with Session(engine) as s:
        p = s.get(Prodotti, product_id)
        print("riga 22 product page: ", p)
        s.close()
    if p is None:
        return "Il prodotto non esiste"
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
        category = request.form['Tag']
        payment_methods = request.form.getlist('payment_methods')
        price_ = request.form['prezzo']
        shipment = request.form['shipment']
        place = request.form.get('luogo')
        quantity_ = request.form['quantita']
        condition = request.form['condition']

        try:
            quantity = int(quantity_)
            if quantity < 0:
                raise ValueError
        except:
            return "quantità non valida"

        try:
            price = float(price_)
            if price == 0:
                raise ValueError
        except:
            return "prezzo non valido"

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
                                autore=current_user.id,
                                tag=category
                                )
            s.add(new_prod)
            s.commit()
            id  = new_prod.id_prodotto

        images = request.files.getlist('images[]')
        image_paths = []

        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)

                filepath = os.path.join(UPLOAD_FOLDER, str(current_user.id), str(id))

                os.makedirs(filepath, exist_ok=True)
                filepath = os.path.join(str(filepath), str(filename))
                image.save(filepath)
                image_paths.append(filepath)

        return redirect(url_for('product.product_page', product_id=id))
    else:
        return render_template('Upload_Form_Template.html')

@product_page_bp.route("/write_review/<int:id>", methods=['GET', 'POST'])
@login_required
def review_upload(id):
    if request.method == 'POST':
        title = request.form['Titolo']
        content = request.form['Descrizione']
        stelline = request.form['star']

        with Session(engine) as s:
            # Aggiungi la nuova recensione e committala
            new_rec = Recensioni(titolo=title, descrizione=content, numero_stelle=stelline)
            s.add(new_rec)
            s.commit()

            # Recupera l'ID della nuova recensione
            new_rec_id = new_rec.id_recensione_entry

            # Aggiungi la relazione nella tabella ProdottiRecensioni
            s.add(ProdottiRecensioni(id_recensione_entry=new_rec_id, id_prodotto=id))
            s.commit()

        return redirect(url_for('product.product_page', product_id=id))
    else:
        return render_template('Write_review.html', product_id=id)

@product_page_bp.route("/reviews/<int:id>")
def reviews(id):

    with (Session(engine) as s):

        pr = aliased(ProdottiRecensioni)
        r = aliased(Recensioni)
        ris = s.query(r).join(pr, r.id_recensione_entry == pr.id_recensione_entry).filter(pr.id_prodotto == id).all()

        media = s.query(func.avg(r.numero_stelle)).join(pr, r.id_recensione_entry == pr.id_recensione_entry).filter(pr.id_prodotto == id).scalar()
        if media is None:
            media = 0
        else:
            media = round(media, 1)

    return render_template('Reviews_template.html', ris=ris, media=media)
