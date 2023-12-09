import cs304dbi as dbi


def insert_post(conn, uid, title, body, categories, type, date):
    '''
    Helper function to insert a created post into the database
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 INSERT INTO post(uid, title, body, categories, type, post_date)
                 VALUES (%s, %s, %s, %s, %s, %s)
                 ''', [uid, title, body, categories, type, date])
    conn.commit()


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

def user_posts(conn, uid):
    '''
    gets all posts from a specified user if
    it is not distinctly closed
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                select pid, title, body, status, categories
                 from post where uid=%s
                 ''',[uid])
    return curs.fetchall()


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
                 from post, user
                 where body like (%s) and type = 'request' and post.uid = user.uid
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
                 from post,user
                 where body like (%s) and type = 'provision' and post.uid = user.uid
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

