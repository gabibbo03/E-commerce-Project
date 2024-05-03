from flask import Blueprint, render_template,redirect,url_for,request,session

login_page_bp = Blueprint('login', __name__)
logout_page_bp = Blueprint('logout',__name__)
sign_in_page_bp = Blueprint('Sign_in' , __name__)
dashboard_bp = Blueprint('dashboard',__name__)


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


@login_page_bp.route('/login',methods=['GET','POST'])
def login_page():
     
    if request.method == 'POST':
        
        user = request.form['username']
        pwd = request.form['password']
        
        session['user'] = user


        print(f' quello che ricevo da metodo post : {user} , {pwd}')
        print(session['user'])

        return redirect(url_for('dashboard.dashboard'))
    else:
        return render_template('Login_Page_Template.html')

@logout_page_bp.route('/logout')
def logout():
    
    if 'user' in session.keys():
        if session['user']:
            session.pop('user',default=None)
        
    return redirect(url_for('root.root'))

@sign_in_page_bp.route('/sign_in', methods= ['GET','POST'])
def sign_in():
    
    if request.method == 'POST':
        user = request.form['username']

        pwd1 = request.form['password1']

        pwd2 = request.form['password2']
        
        print(user,pwd1,pwd2)

        return render_template('Success_Sign_In.html')
    else:
        return render_template('Create_Account_Page.html')

@dashboard_bp.route('/dashboard')
def dashboard():

    if 'user' in session.keys():
        if session['user']:
            return render_template('dashboard.html',user = session['user'])