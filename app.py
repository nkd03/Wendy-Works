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

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET': 
        return render_template('login.html', header ='Welcome to Wendy Works!')
    else:
        action = request.form.get("action")
        if action == 'Login':
            pw = request.form.get("passw")
            user = request.form.get("username")
            if not pw or not user:
                return render_template('login.html', header ='Welcome to Wendy Works!', message='Fields username and password are required')
            else:
                 #will use this in login route
                session['temporary_username'] = user
                session['temporary_password'] = pw
                return redirect(url_for('login'))
        else:
            if action == 'Create Account':
                return redirect(url_for('join'))
        
@app.route('/login/')
def login(): 
    print("METHOD",request.method)
    #removes temp data from session
    user = session.pop('temporary_username', None)
    pw = session.pop('temporary_password', None)
    
    print("USER", user)
    conn = dbi.connect()
    result = pyqueries.login_user(conn, user, pw)
    print("Result", result)
    try: 
        #if the user is in the database
        if result >=1:
            #timestamp = datetime.now() #not sure if we need this
            #ip = str(request.remote_addr) #not sure if we need this
            session['uid'] = result 
            # pyqueries.setsession(conn,result, timestamp, ip)
            return redirect(url_for('profile', uid = result))
        #if incorrect password
        elif result is False:
            flash('Sorry, your password is incorrect, try again')
            return redirect(url_for('login'))
    #if that username is not in the db
    except Exception as e: 
        print("Exception occurred:", e)
        flash('Sorry, no username found, create an account')
        return(redirect(url_for('join')))
 
@app.route('/photo/', methods = ['GET', 'POST'])
def profile_photo(): 
    user = session.get('uid')
    if request.method == 'GET':
        return render_template('photo_upload.html', current_us = user)
    else:
        request.form.get("pic")
        return render_template('photo_upload.html')
     

    

 

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
            print("Skills", skills)
        #getting other skills, changing into a list 
            other_skills = request.form.get("other_skills").split(",")


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
          
            #if pyqueries.check_usern(conn,username) != None:
               #flash("Username is taken. Please enter a unique username")
                #return render_template('create.html', header ='Create an Account')
       
       #if usernam does not exist, continue inserting 
        #inserting into database
            pyqueries.insert_new_user(conn,username,email,f_name,l_name,stored)
        #getting last uid
            row = pyqueries.get_uid(conn)
            uid = row.get("last_insert_id()")
            
            
        #inserting skills 
            pyqueries.insert_skills(conn,uid,skills)

            if len(other_skills) > 0:
                pyqueries.insert_other_skills(conn, uid, other_skills)

            
            flash('Account created! Please log in')
            return redirect(url_for("index"))

        except Exception as err:
            flash('form submission error'+ str(err))
            return redirect( url_for('index') )

           
      
@app.route('/search/', methods = ["GET", "POST"])
def search():
    conn = dbi.connect() 
    print(request.method)
    if request.method == 'GET':
        return render_template('search.html', header ='Search for a post')
    else: #method should be post 
        u_input = request.form.get('query')
        u_kind = request.form.get('kind')
        print(u_input)
        print(u_kind)
        if u_kind == 'provision':
            print("Entering Provision")
            providers = helper.providers(conn, u_input)
            print(providers)
            print(type(providers))
            return render_template('providers.html', key_phrase=u_input, providers = providers)
        if u_kind == 'request':
            print("Entering request")
            requests = helper.find_requests(conn, u_input)

            return render_template('requests.html', key_phrase=u_input, requests = requests)



@app.route('/insert/', methods=["GET", "POST"])
def insert_post():
    '''
    This function is for a user to create a post
    '''
    conn = dbi.connect()
    
    if request.method == 'GET':
        return render_template('insert_post.html')
    else:
        # Collect relevant form information into variables
        print(request.form)
        username = request.form.get('u_name')
        user_id = helper.get_user(conn, username)
        uid = user_id['uid']
        date = datetime.now()
        print(uid)
        title = request.form.get('title')
        body = request.form.get('body')
        categories = request.form.getlist('category')
        print(categories)
        type = request.form.get('type')
        # Flash messages accordingly for missing inputs
        if not body:
            flash('missing input: no body text')
        if not type:
            flash('missing input: no type')
        if not title:
            flash('missing input: no title')
        if not categories:
            flash('missing input: no category selected')
        # If any one of the inputs or combination of inputs is missing, 
        # redirect them to fill out the form again.
        if not body or not title or not categories or not type or str(title).isnumeric():
            return redirect(url_for('insert_post'))
        
        helper.insert_post(conn, uid, title, body, categories, type, date)
        post_id = helper.get_pid(conn)
        
        print(post_id)
        pid = post_id['last_insert_id()']
        print(pid)
       
        flash('Your post was inserted successfully')
        return redirect(url_for('post', pid=pid)) #how do we get the pid??



@app.route('/post/<int:pid>')
def post(pid):
    """
    this funciton displays the specified post
    """
    conn = dbi.connect() 
    #getting post information
    post_info = helper.get_post(conn, pid)
    #getting poster information
    account_info= pyqueries.get_account_info(conn,post_info.get('uid'))
    
    return render_template("display_post.html", post_info=post_info, account_info=account_info)


@app.route('/profile/<int:uid>', methods = ["GET", "POST"])
def profile(uid):
    """
    This function is used for the profile page, getting all
    of the user's information to be displayed
    """
    if session.get('uid') == uid: 
        conn = dbi.connect() 
        information = pyqueries.get_account_info(conn, uid)
        skills = pyqueries.get_skills(conn, uid) 
        fname = information['f_name']
        lname = information['l_name']
        usernm = information['username']
        mail = information['email']
        useid = information['uid']
        if request.method == 'GET': 
            return render_template("account_page.html", fnm = fname, lnm = lname,
                                username = usernm, email = mail, all_skills = skills, usid = useid)
        else:  
            return redirect(url_for('update', user = uid))
    else: 
        flash('Sorry, you cannot access this page')
        return(redirect(url_for('login')))
  

@app.route('/update/<int:user>', methods = ["GET","POST"])
def update(user):
    """
    Any changes the user makes to their information 
    runs through this function
    updates the database or displays update form
    """
    conn = dbi.connect() 
    if request.method == "POST": 
        firstnm = request.form.get('fname')
        lastnm = request.form.get('lname')
        mail = request.form.get('email')
        username = request.form.get('username')
        skills_input = request.form.get('skills')
        #remove old skills from the db
        pyqueries.delSkills(conn, user)
        updated_skills = [skill.strip() for skill in skills_input.split(',')]
        #add new skills to the db
        pyqueries.insert_other_skills(conn, user, updated_skills)
        #userid stays the same so this is just updating additional info
        pyqueries.updateUser(conn, user, firstnm, lastnm, mail, username)
        return redirect(url_for('profile', uid = user))
    else: #method is get
        action = request.args.get('action')
        if action == 'UploadPhoto':
            return redirect(url_for('profile_photo'))
        else:
            info = pyqueries.get_account_info(conn, user)
            uskills = pyqueries.get_skills(conn, user)
            print("Skills ", uskills)
            return render_template("update_profile.html", account = info, skills = uskills, user = user)


@app.route('/logout/')
def logout():
    """
    Logs the user out and ends the session
    """
    session.pop('uid', None)
    flash("You've logged out, please visit again soon!")
    #end the session here 
    return redirect(url_for('index'))


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
