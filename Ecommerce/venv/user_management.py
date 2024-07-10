import hashlib
import os
import statistics

from flask import flash
from flask import Blueprint, render_template, redirect, url_for, request
from hashlib import sha256

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from extention import *
from flask_login import UserMixin,login_user,logout_user,current_user,login_required
from sqlclass import Utente, engine, select, and_, Prodotti, Carrello, ProdottiCarrelli, CarrelloUtenti, \
    ProdottiRecensioni, Recensioni, Utenti, ProdottiStorici,Storico
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

user_manager_bp = Blueprint('user_manager', __name__)


'''
Voglio ricordarmi quando un utente è loggato all'interno del sito :
Uso la classe session che mi permette di simulare questo meccanismo.

Ogni volta che faccio il login (dopo aver fatto il confronto dei dati con il dbms)
aggiungo nel campo user di session il fatto ho fatto il login corretto.

session['user'] = user , mi segno il nome utente


ogni utente quindi potenzialmente ha una sessione diversa che è criptata una chiave

Ogni volta che faccio logout invece rimuovo dalla sessione l'utente con cui ci siè
loggati.

  if session.get('user'): (controllo se effettivamente il campo user esiste)
        if session['user']: (controllo se nel capo user è presente qualcosa)
            session.pop('user',default=None) rimuovo il campo in modo da toglierlo dalla sessione
'''


class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password


@login_manager.user_loader
def user_loader(user_id):

    with Session(engine) as s:
        u = s.get(Utente, user_id)
        print("metodo load_user : " + u.user)
    return User(id=u.user, password=u.password)


def hash_password(password):
    salt = os.urandom(16)  # Genera un sale casuale di 16 byte
    pwd_hash = hashlib.sha256(salt + password.encode('utf-8')).digest()
    return salt + pwd_hash  # Concatena sale e hash


@user_manager_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':

        user = request.form['username']
        pwd = request.form['password'].encode('utf8')
        print(f' quello che ricevo da metodo post : {user} , {pwd}')
        with Session(engine) as s:
            try:
                u = s.query(Utente).where(Utente.user == user).one()
                stored_pwd = u.password
                salt = stored_pwd[:16]
                stored_pwd_hash = stored_pwd[16:]

                pwd_hash = sha256(salt + pwd).digest()

                if pwd_hash == stored_pwd_hash:
                    login_user(User(id=u.user, password=u.password))
                    return redirect(url_for('user_manager.dashboard'))
                else:
                    flash("Credenziali errate: username o password errati")
            except NoResultFound:
                    flash("Credenziali errate: username o password errati")
                    return render_template('Login_Page_Template.html')

    return  render_template("Login_Page_Template.html") # if not post method


@user_manager_bp.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('root.root'))


@user_manager_bp.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        user = request.form['username']
        pwd1 = request.form['password1']
        pwd2 = request.form['password2']

        '''
          per rendere più pulito il messaggio di errore : controllo
          sia che lo user al momento dell'inserimento sia univoco
          che anche la email.
        '''


        print(user, pwd1, pwd2)
        with Session(engine) as s:
            stmt2 = select(Utente).where(Utente.user == user)

            # controllo se esiste già un utente con lo stesso nome.
            # se non ne esistono, la variabile è none
            try:
                useres = s.execute(stmt2).one()
            except NoResultFound:
                useres = None
                print("exc")

            if useres is not None:
                flash("Nome utente già utilizzato da un altro utente")
                return redirect(url_for("user_manager.sign_in"))

        # se arrivo qui, l'utente può essere aggiunto senza problemi
        if pwd1 == pwd2:
            hashed_pwd = hash_password(pwd1)
            with Session(engine) as s:
                s.add(Utente(user= user,password=hashed_pwd,contatto_mail=email))
                s.commit()
                return render_template("Success_Sign_In.html")
        else:
            flash("le password immesse devono essere uguali")
            return redirect(url_for('user_manager.sign_in'))

    else:
        return render_template('Create_Account_Page.html')


@user_manager_bp.route('/dashboard')
@login_required
def dashboard():
    """
     da user carico tutti dati presenti nel dbms , perchè è chiave primaria
    """
    print(type(current_user))

    # visto che sono loggato posso caricare correttamente tutte le info dell'utente.

    with Session(engine) as s:
        u = s.get(Utente , current_user.id)



    return render_template('dashboard.html', user=current_user.id,
                           email=u.contatto_mail,telefono=u.contatto_tel)





@user_manager_bp.route('/carrello')
@login_required
def carrello():

    # visto che sono loggato posso caricare correttamente tutte le info dell'utente.

    _prodotti = []
    img_src = []
    id_carrello_entries = []
    query = request.args

    c = aliased(Carrello)
    p = aliased(Prodotti)
    pc = aliased(ProdottiCarrelli)
    cu = aliased(CarrelloUtenti)
    print(query) # V
    with Session(engine) as s:

        actualUser = current_user.id

        carrelloutente = (
            s.query(c, p)
            .join(cu, c.id_carrello_entry == cu.id_carrello_entry)
            .join(pc, c.id_carrello_entry == pc.id_carrello_entry)
            .join(p, pc.id_prodotto == p.id_prodotto)
            .filter(cu.user == actualUser)
            .all()
        )

        for c,p in carrelloutente:
            _prodotti.append(p)
            id_carrello_entries.append(c)
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
    return render_template("cart.html", products=_prodotti, img_src=img_src, zip=zip, id_carrello_entries=id_carrello_entries)

@user_manager_bp.route('/added')
@login_required
def add_cart():
    if len(request.args) == 0 or 'id' not in request.args or 'qta' not in request.args:
        return "IMPOSSIBILE AGGIUNGERE AL CARRELLO"



    id = request.args['id']
    qta = request.args['qta']

    try:
        qta_int = int(qta)
        if qta_int < 0:
            raise ValueError
    except:
        return "quantità non valida"


    with Session(engine) as s:
        car = Carrello(qta=qta_int)
        s.add(car)
        s.commit()

        car_id = car.id_carrello_entry
        s.add(ProdottiCarrelli(id_prodotto=id,id_carrello_entry=car_id))
        s.add(CarrelloUtenti(id_carrello_entry=car_id,
                             user=current_user.id))

        s.commit()

    return render_template('added.html')

@user_manager_bp.route('/Payed')
@login_required
def payed():
    try:
        # Ottenere l'ID dell'utente loggato
        actualUser = current_user.id

        # Alias per le tabelle coinvolte
        c = aliased(Carrello)
        p = aliased(Prodotti)
        pc = aliased(ProdottiCarrelli)
        cu = aliased(CarrelloUtenti)

        with Session(engine) as s:
            carrelloutente = (
                s.query(c, p)
                .join(cu, c.id_carrello_entry == cu.id_carrello_entry)
                .join(pc, c.id_carrello_entry == pc.id_carrello_entry)
                .join(p, pc.id_prodotto == p.id_prodotto)
                .filter(cu.user == actualUser)
                .all()
            )

            # Verifichiamo la disponibilità dei prodotti nel carrello
            insufficient_stock = []

            for carrello, prodotto in carrelloutente:
                if carrello.qta <= prodotto.disponibilita:
                    stmt = (
                        update(Prodotti)
                        .where(Prodotti.id_prodotto == prodotto.id_prodotto)
                        .values(disponibilita=Prodotti.disponibilita - carrello.qta)
                    )
                    s.execute(stmt)
                else:
                    insufficient_stock.append(prodotto.Titolo)

            if insufficient_stock:
                s.rollback()
                # Costruiamo una stringa con i titoli dei prodotti con disponibilità insufficiente
                stringa = ', '.join(insufficient_stock)
                return f"I prodotti [{stringa}] nel tuo carrello superano la quantità disponibile in magazzino"

            for carrello, prodotto in carrelloutente:
                try:
                    #print("prodotto attuale: ",prodotto.Titolo, ", id: ", prodotto.id_prodotto, ", riga 290")
                    # Aggiungo i prodotti comprati allo storico.
                    st = Storico(
                        Data=datetime.utcnow().date(),
                        Nome=prodotto.Titolo,
                        user=current_user.id
                    )
                    #print(st.__dict__)
                    s.add(st)
                    s.flush() # Flush per ottenere l'id_storico_entry senza commit
                    new_id = st.id_storico_entry
                    #print("new_id = ", new_id)
                    #print("prodotto attuale: ",prodotto.Titolo, ", id: ", prodotto.id_prodotto, ", riga 300")

                    # Aggiungo anche alla tabella intermedia ProdottiStorici per l'integrità referenziale.
                    id_da_aggiungere = prodotto.id_prodotto
                    #print("id_da_aggiungere = ", id_da_aggiungere)
                    ris_ = s.query(Prodotti).where(Prodotti.id_prodotto == id_da_aggiungere).first()
                    #print("ris_ = ", ris_)
                    ps = ProdottiStorici(
                        id_storico_entry=new_id,
                        id_prodotto= id_da_aggiungere if ris_ is not None else None
                    )
                    #print("ps = ", ps.__dict__)
                    s.add(ps)
                    #print("prodotto attuale: ",prodotto.Titolo, ", id: ", prodotto.id_prodotto, ", riga 310")

                    # Elimino dal carrello
                    ris = s.query(Carrello).filter_by(id_carrello_entry=carrello.id_carrello_entry).one()
                    s.delete(ris)
                    #print("prodotto attuale: ",prodotto.Titolo, ", id: ", prodotto.id_prodotto, ", riga 315")

                    # Elimino le immagini
                    folderpath = os.path.join(UPLOAD_FOLDER, str(prodotto.autore), str(prodotto.id_prodotto))
                    delete_images_dir(folderpath)
                    #print("prodotto attuale: ",prodotto.Titolo, ", id: ", prodotto.id_prodotto, ", riga 320")


                    # Commit unico alla fine di tutte le operazioni
                    s.commit()
                except Exception as e:
                    #prodotto con disp e hai nel carrello più di un prodotto.
                    print("exception occurred ",e)
                    pass

    except SQLAlchemyError as e:
        s.rollback()
        error_message = f"Errore durante il pagamento: {str(e)}"
        return error_message

    except Exception as e:
        s.rollback()
        error_message = f"Errore imprevisto durante il pagamento: {str(e)}"
        return error_message

    return render_template("payed.html")


@user_manager_bp.route('/Rimosso')
@login_required
def remove():
    if len(request.args) == 0 or 'id' not in request.args:
        return "IMPOSSIBILE RIMUOVERE DAL CARRELLO"

    try:
        actual_id = int(request.args["id"])
    except ValueError:
        return "Inserisci un valore numerico valido per l'ID"

    actual_user = current_user.id

    with Session(engine) as s:
        try:
            ris = s.query(CarrelloUtenti).filter_by(id_carrello_entry=actual_id).one()


            if ris.user != actual_user:
                return "Non hai i permessi necessari per rimuovere questo articolo"

            ris = s.query(Carrello).filter_by(id_carrello_entry=actual_id).one()

            s.delete(ris)
            s.commit()
        except NoResultFound:
            return "L'elemento specificato non esiste nel carrello"
        except Exception as e:
            s.rollback()
            return f"Si è verificato un errore durante la rimozione: {str(e)}"

    return render_template('Removed.html')

@user_manager_bp.route('/My_sales')
@login_required
def sales(): #lista degli annunci appartenenti all'utente.

    with Session(engine) as s:
        prodotti = s.query(Prodotti).where(Prodotti.autore == current_user.id).all()

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

@user_manager_bp.route("/Change_Mail",methods=["GET","POST"])
@login_required
def cambiamail():
    usr = current_user.id
    with Session(engine) as s:
        vecchia_mail = s.query(Utenti.contatto_mail).filter(Utenti.user == usr).one()[0]
        s.close()
    if request.method == "POST":
        mail1 = request.form['mail1']
        mail2 = request.form['mail2']

        if mail1 != mail2:
            flash("Le email non combaciano")
            return render_template('Change_mail.html', vecchia_mail=vecchia_mail)
        with Session(engine) as s:
            stmt = (
                update(Utenti)
                .where(Utenti.user == usr)
                .values(contatto_mail = mail1)
            )
            s.execute(stmt)
            s.commit()
        return render_template("success.html")

    else:
        return render_template('Change_mail.html', vecchia_mail=vecchia_mail)

@user_manager_bp.route("/Change_Phone",methods=["GET","POST"])
@login_required
def cambiatel():
    usr = current_user.id
    with Session(engine) as s:
        vecchio_numero = s.query(Utenti.contatto_tel).filter(Utenti.user == usr).one()[0]

    if request.method == "POST":
        tel1 = request.form['tel1']
        tel2 = request.form['tel2']

        if tel1 != tel2:
            flash("I numeri non combaciano")
            return render_template('Change_tel.html', vecchio_numero=vecchio_numero)
        with Session(engine) as s:
            stmt = (
                update(Utenti)
                .where(Utenti.user == usr)
                .values(contatto_tel = tel1)
            )
            s.execute(stmt)
            s.commit()
        return render_template("success.html")

    else:
        return render_template('Change_phone.html', vecchio_numero=vecchio_numero)


@user_manager_bp.route('/storico',methods=['GET'])
@login_required
def storico():
    with Session(engine) as s:
        ps = aliased(ProdottiStorici)
        st = aliased(Storico)
        ris = s.query(st, ps).join(ps, st.id_storico_entry == ps.id_storico_entry).filter(st.user == current_user.id).all()

    return render_template('storico.html', ris=ris)