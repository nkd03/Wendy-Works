from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import bcrypt
import pyqueries
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi

# import cs304dbi_sqlite3 as dbi

import random

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html', header ='Welcome to Wendy Works')

# You will probably not need the routes below, but they are here
# just in case. Please delete them if you are not using them

@app.route('/join/', methods=["GET", "POST"])
def join():
    conn = dbi.connect()
    if request.method == 'GET':
        return render_template('create.html', header ='Create an Account')
    else: #request method is POST
       
        try: #getting account information first 
            username = request.form.get("username") 
            pass1=request.form.get("pswrd") 
            pass2=request.form.get("pswrd-repeat")
        #getting contact information
            email=request.form.get("email")
            f_name=request.form.get("f_name")
            l_name=request.form.get("l_name")
        #getting checked skills as a list 
            skills=request.form.getlist("skills")
        #getting other skills, changing into a list 
            other_skills = request.form.get("other_skills").split(",")

            print(other_skills)

        #checking if passwords match before creating account 
        #or inserting anything 
            if pass1 != pass2:
                flash('passwords do not match')
                return redirect( url_for('index'))
            
            hashed = bcrypt.hashpw(pass1.encode('utf-8'),
                        bcrypt.gensalt())
            stored = hashed.decode('utf-8')

            #potentially add a check to ensure a user with that username is not 
            #already in the db? 

        #inserting into database
            pyqueries.insert_new_user(conn,username,email,f_name,l_name,stored)
        #getting last uid
            row = pyqueries.get_uid(conn)
            uid = row.get("last_insert_id()")
            
            
        #inserting skills 
            pyqueries.insert_skills(conn,uid,skills)

            if len(other_skills) > 0:
                pyqueries.insert_other_skills(conn, uid, other_skills)

            #might change this once figure sessions out
            flash('Account created! Please log in')
            return redirect(url_for("login"))

        except Exception as err:
            flash('form submission error'+ str(err))
            return redirect( url_for('index') )


@app.route('/login/', methods = ["GET", "POST"])
def login(): 
    if request.method == 'GET': 
        return render_template('login.html', header = 'Login to Wendy Works')
    else: 
        uname = request.form.get('username')
        in_pw = request.form.get('passw')
        conn = dbi.connect()
        #sessvalue = request.cookies.get('session') working on this more
        #user_info = ...
        result = pyqueries.login_user(conn, uname, in_pw)
        print("Result", result)
        if result >=1:
            flash('Welcome!')
            return redirect(url_for('profile', uid = result))
        elif result is False:
            flash('Sorry, your password is incorrect, try again')
            return redirect(url_for('login'))
        elif result is None: 
             flash('Sorry, no username found, create an account')
             return redirect(url_for('join'))
            
      
       


@app.route('/profile/<int:uid>')
def profile(uid):
    conn = dbi.connect() 
    information = pyqueries.get_account_info(conn, uid)
    skills = pyqueries.get_skills(conn, uid) #not sure if this is the most efficient way but its a start
    print("Skills", skills)
    fname = information['f_name']
    usernm = information['username']
    mail = information['email']
    return render_template("account_page.html", name = fname, username = usernm, email = mail, all_skills = skills)


@app.route('/logout/')
def after_logout():
    flash("you've successfully logged out!")
    #end the session here 
    return redirect( url_for('index') )

# @app.route('/formecho/', methods=['GET','POST'])
# def formecho():
#     if request.method == 'GET':
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data=request.args)
#     elif request.method == 'POST':
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data=request.form)
#     else:
#         # maybe PUT?
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data={})

# @app.route('/testform/')
# def testform():
#     # these forms go to the formecho route
#     return render_template('testform.html')



if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    db_to_use = 'wworks_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
