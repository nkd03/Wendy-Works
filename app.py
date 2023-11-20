from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from datetime import datetime
from werkzeug.utils import secure_filename
import bcrypt
import pyqueries
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi

# import cs304dbi_sqlite3 as dbi

import random
import helper

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

            #might change this once figure sessions out ==> think its okay to leave
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
        result = pyqueries.login_user(conn, uname, in_pw)
        print("Result", result)
        try: 
            #if the user is in the database
            if result >=1:
                timestamp = datetime.now() #not sure if we need this
                ip = str(request.remote_addr) #not sure if we need this
                session['uid'] = result #we do need this
                pyqueries.setsession(conn,result, timestamp, ip)
                flash('Welcome!')
                return redirect(url_for('profile', uid = result))
            #if no user 
            elif result is False:
                flash('Sorry, your password is incorrect, try again')
                return redirect(url_for('login'))
        except Exception as e: 
            print("Exception occurred:", e)
            flash('Sorry, no username found, create an account')
            return(redirect(url_for('join')))
            
      
@app.route('/search/')
def search():
    conn = dbi.connect() 
    u_input = request.args['query']
    u_kind = request.args['kind']
    if u_kind == 'provision':
        key_phrase = u_input
        helper.find_service(conn, key_phrase)
        return render_template('search_results.html', key_phrase=key_phrase)
    if u_kind == 'request':
        helper.find_provider(conn, key_phrase)
        return render_template('search_results.html', key_phrase=key_phrase)

@app.route('/insert/', methods=["GET", "POST"])
def insert_post():
    '''
    This function is for a user to create a post
    '''
    conn = dbi.connect()
    
    if request.method == 'GET':
        return render_template('post.html')
    else:
        # Collect relevant form information into variables
        title = request.form.get('title')
        body = request.form.get('body')
        categories = request.form.getlist('categories')
        type = request.form.get('type')
        # Flash messages accordingly for missing inputs
        if not body:
            flash('missing input: no body text')
        if not title:
            flash('missing input: no title')
        if not categories:
            flash('missing input: no category selected')
        # If any one of the inputs or combination of inputs is missing, 
        # redirect them to fill out the form again.
        if not body or not title or not categories or str(title).isnumeric():
            return redirect(url_for('insert'))
        helper.insert_post(conn, title, body, categories, type)

        flash('Your post was inserted successfully')
        return redirect(url_for('post', pid=pid)) #how do we get the pid??
        
# @app.route('/post/<int:pid>')
# def post(pid):
#     conn = dbi.connect() 
#     post_info = helper.get_post(pid)
    
#     return render_template("post.html", pid=pid)

@app.route('/profile/<int:uid>')
def profile(uid):
    conn = dbi.connect() 
    information = pyqueries.get_account_info(conn, uid)
    skills = pyqueries.get_skills(conn, uid) #not sure if this is the most efficient way but its a start
    print("Skills", skills)
    fname = information['f_name']
    usernm = information['username']
    mail = information['email']
    return render_template("account_page.html", name = fname,
                            username = usernm, email = mail, all_skills = skills)

@app.route('/posts')
def posts():
    return render_template("create.html") #just a tester for the sessions, we can workshop this when there's a new template

@app.route('/logout/')
def logout():
    session.pop('uid', None)
    flash("You've logged out, please visit again soon!")
    #end the session here 
    return redirect(url_for('index'))

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
