from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import bcrypt
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
     if request.method == 'GET':
         return render_template('create.html', header='Create an Account')
     if request.method == 'POST': 
         if request.form.get('email') and request.form.get('username') not in ...:
             ...
             
       
         #return redirect(url_for('profile', uid = ))
        # if username not in the database: 
            #reroute to the profile page 
    #  else:
    #      try:
    #         #getting account information first 
    #          username = request.form.get("username") 
    #          pass1=request.form.get("pswrd") 
    #          pass2=request.form.get("pswrd-repeat")
    #         #getting contact information
    #          email=request.form.get("email")


    #          if pass1 != pass2:
    #             flash('passwords do not match')
    #             return redirect( url_for('index'))
#             flash('form submission successful')
#             return render_template('greet.html',
#                                    title='Welcome '+username,
#                                    name=username)

        #  except Exception as err:
        #      flash('form submission error'+str(err))
        #      return redirect( url_for('index') )

@app.route('/login/', methods = ["GET", "POST"])
def login(): 
    if request.method == 'GET': 
        return render_template('login.html', title = 'Login to Wendy Works!')
    else: 
        #sessvalue = request.cookies.get('session') working on this more
        user = ...

        return redirect(url_for('profile', uid = user))
    
@app.route('/profile/<int:uid>')
def profile(uid):
    ...


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
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'wworks_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
