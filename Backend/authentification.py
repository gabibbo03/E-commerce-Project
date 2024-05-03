from flask import Blueprint, render_template,redirect,request

login_page_bp = Blueprint('login', __name__)
sign_in_page_bp = Blueprint('Sign_in' , __name__)


@login_page_bp.route('/login',methods=['GET','POST'])
def login_page():
     
    if request.method == 'POST':
        
        user = request.form['username']
        pwd = request.form['password']
        
        print(f' quello che ricevo da metodo post : {user} , {pwd}')
        return user
    else:
        return render_template('Login_Page_Template.html')


@sign_in_page_bp.route('/sign_in', methods= ['GET','POST'])
def sign_in():
    
    if request.method == 'POST':
        user = request.form['username']

        pwd1 = request.form['password1']

        pwd2 = request.form['password2']
        
        print(user,pwd1,pwd2)

        return render_template('Success_Sign_In.html')
    else:
        return render_template('Create_Account_Page.html')
