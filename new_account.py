
import cs304dbi as dbi
import bcrypt
# import cs304dbi_sqlite3 as dbi

def insert_new_user(conn,username,email,f_name,l_name,hashed):
    '''
    Takes user account information and inserts in to the user table database 
    '''
    curs = dbi.dict_cursor(conn)
    try:
        curs.execute('''
                 INSERT INTO user(username,email,f_name,l_name,`password`) 
                 VALUES (%s,%s,%s,%s)
                 ''',
                 [username,email,f_name,l_name,hashed])
        conn.commit()
        return  
    except Exception as err:
        flash('That username is taken: {}'.format(repr(err)))
    


def get_uid(conn):
    """A quick helper function to get uid using last-insert"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''select last_insert_id()''')
    row = curs.fetchone()
    uid = row[0]
    return uid 


def insert_skills():
    """This function intends to insert any skills users have checked
    or have added in as other"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 INSERT INTO movie(tt,title,`release`,addedby) 
                 VALUES (%s,%s,%s,%s)
                 ''',
                 [])
    conn.commit()
    return 


def login_user(conn, username, pw): 
    curs = dbi.dict_cursor(conn)
    hashed = bcrypt.hashpw(pw.encode('utf-8'),
                        bcrypt.gensalt())
    


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
