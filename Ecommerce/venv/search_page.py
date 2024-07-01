from flask import Blueprint, render_template,request
from numpy import double

from sqlclass import  engine, and_, Prodotti
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from extention import *


search_page_bp = Blueprint('search', __name__)

"""
  Spiegone : creo una lista di filtri da passare alla query principale.
  Controllo quindi quali filtri sono stati selezionati con una serie infinita
  di if.
  Non è la soluzione migliore ma è la più veloce.
"""

def filters(prezzo_min,prezzo_max,data_min,data_max,condition,payment_methods,sped):

    filt = []
    max_date = datetime.now().date()
    if prezzo_min:
        if double(prezzo_min) >= DOUBLEMIN:
            filt.append(Prodotti.Prezzo >= double(prezzo_min))
    if prezzo_max:
        if double(prezzo_max) <= DOUBLEMAX:
            filt.append(Prodotti.Prezzo <= double(prezzo_max))
    if data_min:
            filt.append(Prodotti.data_pubblicazione >= data_min)
    if data_max:
            filt.append(Prodotti.data_pubblicazione <= data_max)

    if condition and condition != '':
        if condition == 'new':
            filt.append(Prodotti.nuovo == True)
        else:
            filt.append(Prodotti.nuovo == False)

    if payment_methods and '' not in payment_methods:
         if 'visa' in payment_methods:
             filt.append(Prodotti.visa == True)
         if 'cash' in payment_methods:
             filt.append(Prodotti.contanti == True)
         if 'barter' in payment_methods:
             filt.append(Prodotti.baratto == True)
    if sped and sped != '':
        if sped == "new":
            filt.append(Prodotti.spedizione == True)
        else :
            filt.append(Prodotti.spedizione == False)
    return  filt

@search_page_bp.route('/search',methods= ['GET','POST'])
def search_page():

    """
    valori possibili che ricevo :
        min 0
        max maxDouble
        data_min : 01/01/2024
        data_max : current_date
        usato : undefined,new,second_hand

        Spiegazione :

        nel primo caso uso la search bar per filtrare i prodotti.
        nel secondo caso uso i filtri per ottenere i prodotti desiderati.
        La parte più difficile è stata fare i filtri
    """

    if request.method == 'GET':

        _prodotti = []
        img_src  = []
        query = request.args

        print(query) # V
        with Session(engine) as s:
            if len(query) == 1 and "query" in query.keys():
                prodotti = s.query(Prodotti).all()
                for p in prodotti:
                    if query["query"] in p.Descrizione or query["query"] in p.Titolo:
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
            else:
                prezzo_min = request.args.get('prezzo_min')
                prezzo_max = request.args.get('prezzo_max')
                data_min = request.args.get('data_min')
                data_max = request.args.get('data_max')
                condition = request.args.get('condition')
                payment_methods = request.args.getlist('payment_methods[]')
                sped = request.args.get('Sped')

                ris = filters(prezzo_min,prezzo_max,data_min,data_max,condition,payment_methods,sped)
                prodotti = s.query(Prodotti).where(and_(*ris)).all()

                for p in prodotti:

                    _prodotti.append(p)
                    folderpath = os.path.join(UPLOAD_FOLDER, str(p.autore), str(p.id_prodotto))
                    print("folderpath = ", folderpath)
                    if os.path.exists(folderpath) and os.path.isdir(folderpath):
                        files = os.listdir(folderpath)
                        filepath = os.path.join(folderpath, files[0])

                        img_src.append(filepath)
                        print(filepath)

                    else:
                        img_src.append(placeholder)
                        print(placeholder)

        return render_template("list_of_products_page_template.html",products=_prodotti, img_src=img_src, zip=zip)
        s.commit()

    return render_template("list_of_products_page_template.html")

@search_page_bp.route("/filter")
def filter_query():
    return  render_template("Filters_Form_Template.html")