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
    return


def get_user(conn, username):
    '''
    Helper function find user by username 
    Returns user
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
    returns post 
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
    returns lists of posts by uid 
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                select pid, title, body, type, status, categories
                 from post where uid=%s
                 ''',[uid])
    return curs.fetchall()


def get_pid(conn):
    """A quick helper function to get uid using
      last-insert
      Using until we fix transactions"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''select last_insert_id()''')
    return curs.fetchone()

def find_requests(conn, key_phrase):
    '''
    Helper function to find posts including the relevant keyword 
    for a request
    returns lists of posts labeled as request by phrase 
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
    returns lists of posts labeled as provision by phrase
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 select *
                 from post,user
                 where body like (%s) and type = 'provision' and post.uid = user.uid
                 ''', ['%' + key_phrase + '%'])
    return curs.fetchall()

def update_post(conn, post_obj, pid):
    '''
    Helper function to find users who can provide a service
    based on the categories that the "provider" has linked to
    their account
    returns lists of posts labeled as provision by phrase
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE post
                 SET title = %s, body = %s, status = %s
                 where pid = %s
                 ''', [post_obj.get('title'), post_obj.get('body'), 
                       post_obj.get('status'), pid])
    conn.commit()
    return curs.fetchall()

def delete_post(conn, pid):
    '''
    Used to delete a specified post 
    from the db
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                DELETE from post where pid=%s
                 ''', [pid])
    conn.commit() 


def add_comment(conn, pid, uid, body):
    '''
    Helper function to insert a created post into the database
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 INSERT INTO replies(pid, uid, body)
                 VALUES (%s, %s, %s)
                 ''', [pid, uid, body])
    conn.commit()

def get_comment(conn, pid):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                SELECT * 
                FROM replies
                WHERE pid = %s
                ''', [pid])
    return curs.fetchall()
