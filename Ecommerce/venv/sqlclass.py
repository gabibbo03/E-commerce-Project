from sqlalchemy import URL,create_engine,select,and_,desc,func
from sqlalchemy.ext.automap import automap_base

# Usa l'engine che hai già creato
url_code = URL.create(
    drivername="postgresql",
    username="postgres",
    password="post",
    host="localhost",
    port=5432,
    database="Ecommerce"
)

engine = create_engine(url=url_code,echo=False)

Base = automap_base()
Base.prepare(autoload_with=engine)


Utente = Base.classes['Utenti']
Prodotti = Base.classes['Prodotti']
Carrello = Base.classes['Carrello']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']
Utenti = Base.classes['Utenti']


