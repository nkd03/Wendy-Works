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
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 

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
    """ This is our main page it contains a login form or new users can create an account"""
    if request.method == 'GET': 
        return render_template('login.html', header ='Welcome to Wendy Works!', logo='wendyworks.png')
    else:
        action = request.form.get("action")
        if action == 'Login':
            pw = request.form.get("passw")
            user = request.form.get("username")
            if not pw or not user:
                return render_template('login.html', header ='Welcome to Wendy Works!', message='Fields username and password are required', logo='wendyworks.png')
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
    """This function serves to log users in if they exists ensuring 
    that their credentials are correct or directs users to create an account """
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
            return redirect(url_for('home'))
        #if incorrect password
        elif result is False:
            flash('Sorry, your password is incorrect, try again')
            return redirect(url_for('index'))
    #if that username is not in the db
    except Exception as e: 
        if user != None: 
            flash(f'Sorry, no account with username: {user} found. Create an account')
        return(redirect(url_for('index')))
 
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Function serves to get uploaded file"""
    return send_from_directory(app.config['UPLOADS'], filename)


@app.route('/photo/', methods = ['GET', 'POST'])
def profile_photo(): 
    '''
     the user's profile photo is saved in db 
     or the photo upload page is shown 
    '''
    user = session.get('uid')
    print("user", user)
    if request.method == 'GET':
        return render_template('photo_upload.html', current_us=user,logo='wendyworks.png')
    else:
        conn = dbi.connect() 
        p = request.files["pic"]
        user_filename = p.filename
        ext = user_filename.split('.')[-1]
        print("EXT", ext)
        if ext == 'jpeg' or ext =='jpg':
            filename = secure_filename('{}.{}'.format(user, ext))
            # Check and delete old photo
            old_photo_path = os.path.join(app.config['UPLOADS'], f"{user}.{ext}")
            if os.path.isfile(old_photo_path):
                os.remove(old_photo_path)
            # save new 
            pathname = os.path.join(app.config['UPLOADS'], filename)
            p.save(pathname)
            # Store photo info in db
            pyqueries.insert_photo(conn, user, filename)
            flash("Photo Upload Successful!")
        else:
            flash("Please upload a JPEG or PNG.")

        # Redirect to the user's profile
        return redirect(url_for('profile', uid=user))
    
    
@app.route('/home/')
def home():
    '''
    Used for home page feed, gets 10 most 
    recent post entries user non-inclusive
    ''' 
    conn = dbi.connect()
    uid = session.get('uid')
    recent_posts = pyqueries.most_recent(conn, uid)
    return render_template("home.html", posts = recent_posts, logo = 'wendyworks.png')
    


@app.route('/join/', methods=["GET", "POST"])
def join():
    """This route is used when users are creating a new account, the form takes 
    user skills, and contact information to insert them into the database"""
    conn = dbi.connect()
    if request.method == 'GET':
        return render_template('create.html', header ='Create an Account', logo = 'wendyworks.png')
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
       
       #if usernam does not exist, continue inserting 
        #inserting into database
            print("I got here to line 172", username)
            pyqueries.insert_new_user(conn,username,email,f_name,l_name,stored)
        #getting last uid
            row = pyqueries.get_uid(conn)
            #print("I got here to line 176", row)
            uid = row.get("last_insert_id()")
            
            
        #inserting skills 
            pyqueries.insert_skills(conn,uid,skills)

            if len(other_skills) > 0:
                pyqueries.insert_other_skills(conn, uid, other_skills)
            flash('Account created, welcome!')

            
            flash('Account created, welcome!')
            #automatically log-in
            session['uid'] = uid
            return redirect(url_for("profile", uid = uid))
        except Exception as err:
            #print("Error",err)
            flash('form submission error'+ str(err))
            return redirect( url_for('index') )
      


@app.route('/search/', methods = ["GET", "POST"])
def search():
    """This route gets information from search form 
    to find and display prodvider or requestor posts
    Return: renders search form or search result page
     """

    conn = dbi.connect() 
    print(request.method)
    if request.method == 'GET':
        return render_template('search.html', header ='Search for a post',logo='wendyworks.png')
    else: #method should be post 
        u_input = request.form.get('query')
        u_kind = request.form.get('kind')
        print(u_input)
        print(u_kind)
        if u_kind == 'provision':
            providers = helper.providers(conn, u_input)
            return render_template('providers.html', key_phrase=u_input, providers = providers, logo='wendyworks.png')
        if u_kind == 'request':
            requests = helper.find_requests(conn, u_input)
            print('LINE 202', requests)
            return render_template('requests.html', key_phrase=u_input, requests = requests, logo='wendyworks.png')


@app.route('/insert/', methods=["GET", "POST"])
def insert_post():
    '''
    This function is for a user to create a post 
    in which they indicate whether a post is requesting or 
    providing and the skills they need or give give
    Redirects to profile page 
    '''
    conn = dbi.connect()
    
    if request.method == 'GET':
        return render_template('insert_post.html', logo='wendyworks.png')
    else:
        # Collect relevant form information into variables
        uid = session.get('uid')
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
      
     
        flash('Your post was inserted successfully')
        return redirect(url_for('profile', uid=uid))




@app.route('/profile/<int:uid>', methods = ["GET", "POST"])
def profile(uid):
    """
    This function is used for the profile page, getting all
    of the user's information to be displayed
    Return: renders account page 
    """
    if session.get('uid') == uid: 
        conn = dbi.connect() 
        information = pyqueries.get_account_info(conn, uid)
        skills = pyqueries.get_skills(conn, uid) 
        u_posts = helper.user_posts(conn, uid)
        #useid = information['uid')
        if request.method == 'GET': 
            user_photo = pyqueries.get_photo(conn, uid)
            #print("PHOTO", user_photo)
            if user_photo == None:
                return render_template("account_page.html", userdata = information, all_skills = skills, usid = uid, posts = u_posts, logo='wendyworks.png')
            else:
                p_user = user_photo['filename']
                photo_url = url_for('uploaded_file', filename=p_user)
                print("PHOTO_URL", photo_url)
                #photo = send_from_directory(app.config['UPLOADS'],p_user)
                return render_template("account_page.html", userdata = information, all_skills = skills, usid = uid, picture = photo_url, posts = u_posts, logo='wendyworks.png') 
        else:
            
            return redirect(url_for('update', user = uid))
    else: 
        flash("Sorry, you cannot access this page.")
        user = session.get('uid')
        return(redirect(url_for('profile', uid= user)))
  

@app.route('/update/<int:user>', methods = ["GET","POST"])
def update(user):
    """
    Any changes the user makes to their information 
    runs through this function
    updates the database or displays update form
    Returns: redirects to profile 
    """
    conn = dbi.connect() 
    if request.method == "POST": 
        firstnm = request.form.get('fname')
        lastnm = request.form.get('lname')
        mail = request.form.get('email')
        username = request.form.get('username')
        skills_input = request.form.get('skills')
        pyqueries.delSkills(conn, user)
        updated_skills = [skill.strip() for skill in skills_input.split(',')]
        pyqueries.insert_other_skills(conn, user, updated_skills)
        #userid stays the same so this is just updating additional info
        pyqueries.updateUser(conn, user, firstnm, lastnm, mail, username)
        return redirect(url_for('profile', uid = user))
    else: #method is get
        action = request.args.get('action')
        if action == 'UploadPhoto':
            return redirect(url_for('profile_photo'))
        elif action == 'Delete':
            uid = session.get('uid')
            pyqueries.deleteUser(conn, uid)
            session.pop('uid', None)
            flash("We're sorry to see you go! Account successfully deleted")
            return redirect(url_for('index'))
        else:
            info = pyqueries.get_account_info(conn, user)
            uskills = pyqueries.get_skills(conn, user)
            print("Skills ", uskills)
            return render_template("update_profile.html", account = info, skills = uskills, user = user, logo='wendyworks.png')


@app.route('/update_post/<int:pid>', methods = ["GET","POST"])
def update_post(pid):
    """
    Allows for user to update post details
    """
    conn = dbi.connect() 
    # Retrieve the post from the database using post_id
    user = session.get('uid')
    print(request.method)
    if request.method == 'GET':
        post = helper.get_post(conn, pid)
        print('LINE 332', post)
        #user = session.get('uid')
        
        return render_template('update_post.html', post = post, pid=post.get('pid'), logo='wendyworks.png')
    else:
        # Update post details based on the form submission
        
        action = request.form.get('action')
        print("Action",action)
        if action == "UpdatePost":
            #user = session.get('uid')
            print('line 329', user)
            updated_post = request.form
            helper.update_post(conn, updated_post, pid)
        else:
            helper.delete_post(conn, pid)
            flash("Post deleted successfully")
        return redirect(url_for('profile', uid=user))


@app.route('/interest/<int:pid>', methods = ["GET", "POST"])
def insert_interest(pid):
    conn = dbi.connect()
    if request.method == "GET":
        uid = session.get("uid")
        #insert into interest 
        pyqueries.insert_interest(conn, pid, uid)
        #get number of interest for pid
        interest_count = len(pyqueries.get_interest_count(conn,pid))
        #update interest count in the posts table 
        pyqueries.update_posts_interest_count(conn,interest_count,pid)
        flash("Your information has been sent")
        return redirect(url_for('search'))









@app.route('/post/<int:pid>')
def view_post(pid):
    # Fetch the post from the database based on pid
    conn = dbi.connect() 
    post = helper.get_post(conn, pid)
    all_interested = pyqueries.get_interested(conn,pid)

    if post:
        return render_template('post.html', post=post, all_interested = all_interested ,logo='wendyworks.png')
    else:
        # Handle case where post is not found
        return redirect(url_for('index'))








@app.route('/logout/')
def logout():
    """
    Logs the user out and ends the session
    """
    session.pop('uid', None)
    flash("You've logged out, please visit again soon!")
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
