# Cambiamenti : 
Ho apportato questi cambiamenti a causa di un conflitto con una libreria python : flask-login 6.3.0.

- server-side
- client-side
- implementazioni


# Server-side.
Ho quindi usato il modulo : user_management per implementare il meccanismo di

- login
- logout
- sign_in  
- dashboard.

il problema principale è stato quello di gestire le variabili che dovrebbero essere viste da più moduli.
Tra cui l'oggetto login_manager che deve essere inizializzato in 'app.py' e usato in 'user_management'.py .

Ho quindi deciso di introdurre un nuovo modulo python chiamato 'extention.py' in cui ho dichiarato l'oggetto necessario 
per il login.(guarda #implementazioni)

Altra modifica sta nel DB in cui ho sistemato alcuni attributi della relazione utente in modo che funzionasse il meccanismo 
di hashing del login.

1. nome VARCHAR(20) -> VARCHAR(256) , l'ho fatto un po per pigrizia, non avevo voglia di controllare l'input dell'utente lol
2. password  VARCHAR(20) -> BYTEA , questo è il cambiamento più importante , perchè hashando non salvo caratteri ma byte ( entrava in conflitto quando facevo la 
  query per il login)
3. email VARCHAR(20) -> VARCHAR(256) , stesso motivo del punto 1.

# Client-side.

altri cambiamenti li ho apportati alla struttura del file 'header.html' per gestire le sessioni e i messaggi che di flask.
I messaggi come 'utente o password errata' vengono messi sul file html con una funzione di flask chiamata 'flash' che li printa in modo da migliorare la visibilità
nel sito.

Ho provato ad aggiungere qualcosa del file dashboard,mettendo le informazioni dell'utente.

# Implementazioni :

L'implementazione delle operazioni di base che un utente può fare nel sito hanno bisogno di due cose : 

1. Un oggetto di tipo Login_manager
2. Un oggetto di tipo User.

Il Login_manager si occupa di gestire il meccanismo delle sessioni in modo che utente rimanga autenticato (con i cookies) nel momento in cui fa login
ed esce dalla sua area personale/esce dal suo account nel momento in cui fa logout.

l'oggetto User invece serve per rappresentare l'utente in ogni operazione.
La cosa più importante da ricordare per questa classe è che l'attributo 'id' corrisponde alla chiave primaria di 'Utente' in sqlalchemy.
é necessario un metodo UserLoader per funzionalità interne delle funzioni di login e logout.
Questo metodo esegue una semplice query del tipo : 

SELECT UTENTI.user,UTENTI.password,UTENTI......
FROM  UTENTI
WHERE Utenti.user = id.

dove carica dal db le informazioni per l'utente.

# funzioni spiegate in Breve : 

1. Login : 

    all'inizio di tutto è presente un if che vede se sto facendo un richiesta post o get.
    se ho una richiesta post prendo in input ciò che lo username e la password dell'utente.
    Apro una Sessione sul DB.
    successivamente faccio un try - except 
    il try principalmente cerca di eseguire una query per trovare il primo utente con quelle credenziali
    se la query non trova quei dati, lancia un'eccezione che viene raccolta da except.
    Dopo la query prendo la password hashata e mi salvo sia il sale che la password presa dal db.
    Il sale lo uso per hasharlo con la password e poi confrontarla con quella salvata nel db.

    se le due password sono uguali faccio
       login_user(User(id=user,bla,bla,bla))
       redirect('user_management.dashboard')

2. logout :
    
    Semplicemente toglie dalla sessione lo user 
    tramite logout_user()

    poi fa redirect alla root.

3. Sign_in :
    Il funzionamento è simile a login solo che in questo caso viene salvato l'utente
    con User,password_hashata e email.

    altri controlli che faccio è vedere se l'utente che ha inserito l'email non ne sta
    usando una già presente.
    (dovrei farlo anche per user).

4. dashboard : 

    da qui carico tutte le informazioni di base per l'utente
    e vorrei che l'utente potesse cambiare queste informazioni da qui
    almeno : nome utente,password,numero di telefono,email...etc.

    