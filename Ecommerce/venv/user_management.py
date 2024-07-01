import hashlib
import os
from flask import flash
from flask import Blueprint, render_template, redirect, url_for, request
from hashlib import sha256
import extention
from flask_login import UserMixin,login_user,logout_user,current_user,login_required
from sqlclass import Utente, engine, select, and_
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


@extention.login_manager.user_loader
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
            stmt = select(Utente).where(and_(Utente.contatto_mail == email, Utente.user != user))
            stmt2 = select(Utente).where(Utente.user == user)
            emailres = s.execute(stmt).all()
            useres = s.execute(stmt2).one()

        if useres or emailres:
            if useres:
                flash("Nome utente già utilizzato da un altro utente")

            if emailres:
                flash("email già utilizzata")
            return redirect(url_for("user_manager.sign_in"))


        if pwd1 == pwd2:
            hashed_pwd = hash_password(pwd1)
            with Session(engine) as s:
                s.add(Utente(user= user,password=hashed_pwd,contatto_mail=email))
                s.commit()
                return render_template("Success_Sign_In.html")
        else:
            flash("le password immesse devono essere uguali")
            return redirect(url_for('user_manager.sign_in'))

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
                           email=u.contatto_mail,telefono=u.contatto_tel,
                           media_recensioni=u.media_recensioni_ricevute)
