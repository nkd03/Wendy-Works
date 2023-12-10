
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
                 VALUES (%s,%s,%s,%s,%s)
                 ''',
                 [username,email,f_name,l_name,hashed])
        conn.commit() 
    except Exception as err:
        return ('Error: {}'.format(repr(err)))
 



def get_uid(conn):
    """A quick helper function to get uid using last-insert"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''select last_insert_id()''')
    return curs.fetchone()




def insert_skills(conn, uid,skills):
    """This function intends to insert any skills users have checked
    or have added in as other"""
    curs = dbi.dict_cursor(conn)
    for skill in skills:
        curs.execute('''
                    INSERT INTO skills(uid,skill) 
                    VALUES (%s,%s)
                    ''',
                    [uid,skill])
        conn.commit()
    
def get_photo(conn, uid): 
    '''
    gets the user's profile photo from
    the db
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select filename from picfile where 
                 uid=%s''', [uid]
                 )
    return curs.fetchone() 

def insert_photo(conn, uid, filename):
    '''
    Inserts a new photo into the database or updates the existing one if the uid already exists.
    '''
    curs = dbi.dict_cursor(conn)

    # check if the uid is already in the database
    curs.execute('''SELECT * FROM picfile WHERE uid = %s''', [uid])
    if curs.fetchone():
        # If uid exists, update 
        curs.execute('''UPDATE picfile SET filename = %s WHERE uid = %s''', [filename, uid])
    else:
        # If uid does not exist, insert 
        curs.execute('''INSERT INTO picfile(uid, filename) VALUES (%s, %s)''', [uid, filename])

    conn.commit()


def insert_other_skills(conn, uid, other_skills):
    """This function intends to insert any skills users have checked
    or have added in as other"""
    curs = dbi.dict_cursor(conn)
    for skill in other_skills:
        if skill!= '':
            curs.execute('''
                    INSERT INTO skills(uid,skill) 
                    VALUES (%s,%s)
                    ''',
                    [uid,skill])
            conn.commit()
    


def get_skills(conn, uid): 
    """
    This function gets all skills
    that the user has in the database
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                select * from skills where uid= (%s)
                 ''', [uid]) 
    return curs.fetchall()


def get_account_info(conn,uid):
    """This function returns users information using uid """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                    select * from user where uid= (%s)
                    ''',
                    [uid])
    return curs.fetchone()

    

def login_user(conn, username, pass1):
    """
    This function checks if the input and hashed
    passwords are the same and returns the uid, false, 
    or, if not found, None

    """ 
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 select f_name, `uid`, `password` from user 
                 where username= (%s)
                 ''', [username])
    element = curs.fetchone() 
    if element is not None: 
        passw = element['password']
        hashed2 = bcrypt.hashpw(pass1.encode('utf-8'), passw.encode('utf-8'))
        hashed2_str = hashed2.decode('utf-8')
        if hashed2_str == passw:
            return element['uid']
        else: 
            return False

def updateUser(conn, user, firstnm, lastnm, mail, username):
    """
    Updates the user's information in the database
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                    update user set username = %s, email = %s, f_name = %s, l_name = %s
                    where `uid`=(%s)
                 ''', [username, mail, firstnm, lastnm, user])   
    conn.commit() 
    

def delSkills(conn, user): 
    """
    Removes skills in the database
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                delete from skills where uid =(%s)
                 ''', [user])
    conn.commit() 

def setsession(conn, result, timestamp, uip): 
    """
    sets session information for the database
    will be utilized in next version of project
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
    INSERT INTO session (`uid`, st, ip) 
    VALUES (%s, %s, %s)
     ''', [result,timestamp, uip])
    conn.commit() 



