from flask import Blueprint, render_template

product_page_bp = Blueprint('product', __name__)

@product_page_bp.route('/<product_id>')
def product_page():
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
    return f'@TODO: product_page '