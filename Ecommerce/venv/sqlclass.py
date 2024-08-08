from sqlalchemy import URL,create_engine,func,and_,select
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
Recensioni = Base.classes['Recensioni']
ProdottiRecensioni = Base.classes['ProdottiRecensioni']
ProdottiCarrelli = Base.classes['ProdottiCarrelli']
CarrelloUtenti = Base.classes['CarrelloUtenti']
ProdottiStorici = Base.classes['ProdottiStorici']
Storico = Base.classes['Storico']
print(Storico.__table__.columns.keys())


