import cs304dbi as dbi


def insert_post(conn, uid, title, body, categories, type, date):
    '''
    Helper function to insert a created post into the database
    '''
    curs = dbi.dict_cursor(conn)
    # how would we get the username?
    curs.execute('''
                 INSERT INTO post(uid, title, body, categories, type, post_date)
                 VALUES (%s, %s, %s, %s, %s, %s)
                 ''', [uid, title, body, categories, type, date])
    conn.commit()


# pid INT AUTO_INCREMENT PRIMARY KEY,
#   `uid` INT NOT NULL, 
#   title VARCHAR(40) NOT NULL, 
#   body TEXT NOT NULL, 
#   post_date DATE NOT NULL,
#   categories SET('clothing', 'fitness', 'beauty', 'crafts', 'transportation', 'photography', 'other') NOT NULL,
#   `type` ENUM('request', 'provision'), 
#   `status` ENUM('open', 'closed', 'in progress') NOT NULL, 

def get_user(conn, username):
    '''
    Helper function to insert a created post into the database
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT uid 
                 from user
                 where username = %s
                 ''', [username])
    return curs.fetchone()

def get_post(conn, pid):
    '''
    Helper function to get a post given its pid
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT * from post 
                 WHERE pid = %s
                 ''', [pid])
    return curs.fetchone()

def get_pid(conn):
    """A quick helper function to get uid using last-insert"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''select last_insert_id()''')
    return curs.fetchone()

def find_requests(conn, key_phrase):
    '''
    Helper function to find posts including the relevant keyword 
    for a request
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 select *
                 from post
                 where body like (%s) and type = 'request'
                 ''', ['%' + key_phrase + '%'])

    return curs.fetchall()


def providers(conn, key_phrase):
    '''
    Helper function to find users who can provide a service
    based on the categories that the "provider" has linked to
    their account
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 select *
                 from post
                 where body like (%s) and type = 'provision'
                 ''', ['%' + key_phrase + '%'])
    return curs.fetchall()

def find_service_by_cat(conn, cat):
    '''
    Helper function to find posts that belong to a certain category
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 select *
                 from post
                 where categories = %s
                 ''', [cat])
    results = curs.fetchall()
    return results

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
    conn = dbi.connect()
    uid_test = get_user(conn, 'test1')
    print(uid_test)
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)