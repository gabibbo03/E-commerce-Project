from flask import Flask, render_template, request

app = Flask(__name__)

# pagina della lista prodotti
@app.route('/')
def root ():
    """
    viene qualcosa del tipo
    lista_articoli = recupera_da_database
    return render_template(list_of_products_page_template, products = lista_articoli)
    così facendo viene una lista troppo lunga. si può fare
    che la lista viene spezzata in blocchi da 10, e si fanno n pagine da 10 prodotti.
    
    nel template a fondo pagina si mette un bottone "next" che manda una request del tipo "?page=2"
    cos' si capisce quale dei n blocchi da 10 inviare al render del template.
    in pratica, qui si fa un for da 0 a n con salti di 10. nel template c'è già
    il for_each element (quindi da 0 a 10).
    """
    pass

@app.route('/login')
def login ():
    """
    gestione del metodo post
    """
    pass

@app.route('/<item_id>')
def dashboard ():
    """
    item_id è la chiave primaria dell'articolo dentro al database
    articolo = get_article_from_db(item_id)
    return render_template(
        product_page,
        product_name = articolo.name, o articolo[name], o quel che è
            a seconda del tipo di dato in cui è salavtp
        prduct_description = articolo.descrizione

        etc
        
        )
    """
    pass