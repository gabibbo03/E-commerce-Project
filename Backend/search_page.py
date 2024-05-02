from flask import Blueprint, render_template,request

search_page_bp = Blueprint('search', __name__)

@search_page_bp.route('/search',methods= ['GET','POST'])
def search_page():
     

    if request.method == 'POST':
        
        query = request.form['search_query']
        print(query)
   
        return """
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
    else:
        return render_template("list_of_products_page_template.html")
