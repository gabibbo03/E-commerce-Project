from flask_login import LoginManager

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
