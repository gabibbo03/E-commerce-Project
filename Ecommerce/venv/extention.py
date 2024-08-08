from flask import app
from flask_login import LoginManager
import os
import shutil
from numpy import finfo,float64
from datetime import  datetime
from sqlalchemy.orm import aliased

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


def delete_images_dir(path_cartella):
    # Verifica se il percorso della cartella esiste
    if os.path.exists(path_cartella):
        # Elimina tutti i file nella cartella
        for nome_file in os.listdir(path_cartella):
            percorso_completo = os.path.join(path_cartella, nome_file)
            try:
                if os.path.isfile(percorso_completo):
                    os.remove(percorso_completo)
                elif os.path.isdir(percorso_completo):
                    shutil.rmtree(percorso_completo)  # Elimina anche le sotto-cartelle ricorsivamente
            except Exception as e:
                print(f"Errore durante l'eliminazione di {percorso_completo}: {e}")
                raise e

        # Elimina la cartella stessa
        try:
            os.rmdir(path_cartella)
            print(f"Cartella {path_cartella} eliminata con successo.")
        except Exception as e:
            print(f"Errore durante l'eliminazione della cartella {path_cartella}: {e}")
            raise e
    else:
        print(f"Il percorso {path_cartella} non esiste.")

def get_images_for_products(_prodotti, p, img_src) -> None:
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