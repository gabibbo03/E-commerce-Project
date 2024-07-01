from flask import app
from flask_login import LoginManager
import os
from numpy import finfo,float64
from dateutil import parser
from datetime import  datetime
"""
   extention.py serve solo a collegare login_manager di 
   app.py in cui viene inizializzato ogni volta che viene tirato su il server
   e user_management.py in cui viene ogni volta vengono eseguite le procedure 
   adibite all'identificazione di un utente.
"""

login_manager = LoginManager()

"""
  questo pezzo di codice fa in modo che ogni volta che
  si vuole accedere ad una parte in cui è necessario l'accesso 
  si viene indirizzati alla pagina di login
"""
login_manager.login_view = 'user_manager.login_page'

# Base directory of the project
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Directory where uploaded files will be stored
UPLOAD_FOLDER = os.path.join('static\\uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_PATH = 16 * 1024 * 1024 # Maximum file size: 16MB

placeholder = os.path.join(UPLOAD_FOLDER,"product-placeholder.png")

#controlla che la estensione dei file siano corretti
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#valori massimi per il valore dei prezzi.
DOUBLEMAX = finfo(float64).max
DOUBLEMIN = 0.0

start_date = datetime(2024, 12, 1).date()

# controlla che la data sia valida e nel range giusto
def check_date_validity(date_str):
    try:
        # Data di inizio: 1 dicembre 2024
        start_date = datetime(2024, 12, 1).date()

        # Data di fine: data attuale
        end_date = datetime.now().date()

        # Parsa la data fornita nel formato "dd/mm/yy"
        date = parser.parse(date_str, dayfirst=True).date()

        # Controlla che la data sia compresa tra start_date e end_date
        return start_date <= date <= end_date

    except ValueError:
        # Se c'è un errore nel parsing della data, restituisci False
        return False