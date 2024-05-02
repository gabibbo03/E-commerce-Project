from flask import Blueprint, render_template,request

login_page_bp = Blueprint('login', __name__)

@login_page_bp.route('/login',methods=['GET','POST'])
def login_page():
     
    if request.method == 'POST':
        
        user = request.form['username']
        pwd = request.form['password']
        
        print(f' quello che ricevo da metodo post : {user} , {pwd}')
        return user
    else:
        return render_template('Login_Page_Template.html')