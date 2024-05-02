from flask import Blueprint, render_template,request

search_page_bp = Blueprint('search', __name__)

@search_page_bp.route('/search',methods= ['GET','POST'])
def search_page():
     
    if request.method == 'GET':
          query = request.args
          for k in query.keys():
               print(query[k])
    
    return render_template("list_of_products_page_template.html")
