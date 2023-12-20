import cs304dbi as dbi


def insert_post(conn, uid, title, body, categories, type, date):
    '''
    Helper function to insert a post into the database.
    Returns the post id. 
    '''
    curs = dbi.cursor(conn)
    curs.execute('''
                 INSERT INTO post(uid, title, body, categories, type, post_date)
                 VALUES (%s, %s, %s, %s, %s, %s)
                 ''', [uid, title, body, categories, type, date])
    conn.commit()
    curs.execute('''select last_insert_id()''')
    pid = curs.fetchone()
    return pid[0]


def get_user(conn, username):
    '''
    Helper function find user by username.
    Returns user.
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
    Helper function to get a post given its pid.
    Returns post.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT pid, uid, title, body, post_date, categories, type, status, interest_count from post 
                 WHERE pid = %s
                 ''', [pid])
    return curs.fetchone()

def user_posts(conn, uid):
    '''
    Helper function that gets all posts from a 
    specific user.
    Returns lists of posts sorted by date.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                select pid, title, body, type, status, categories,
                 interest_count
                 from post where uid=%s
                 ORDER BY post_date DESC
                 ''',[uid])
    return curs.fetchall()



def find_requests(conn, key_phrase):
    '''
    Helper function to find posts including the relevant keyword 
    for a request.
    Returns list of posts labeled as request.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 select pid, title, body, categories, status, post_date, 
                 email, username, f_name, l_name
                 from post, user
                 where body like (%s) and type = 'request' and post.uid = user.uid
                 ORDER BY post_date DESC
                 ''', ['%' + key_phrase + '%'])

    return curs.fetchall()


def providers(conn, key_phrase):
    '''
    Helper function to find posts including the relevant keyword
    for a provision.
    Returns list of posts labeled as provision.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 select *
                 from post,user
                 where body like (%s) and type = 'provision' and post.uid = user.uid
                 ORDER BY post_date DESC
                 ''', ['%' + key_phrase + '%'])
    return curs.fetchall()

def update_post(conn, post_obj, pid):
    '''
    Helper function to update the post in a table.
    Returns the updated post. 
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
                DELETE from interest where pid=%s
                    ''',[pid])
    conn.commit()
    curs.execute('''
                DELETE from replies where pid=%s
                 ''',[pid])
    conn.commit()
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
    '''
    Helper function to get a user's comment under a specified post
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                SELECT replies.uid, user.f_name, replies.body FROM 
                 replies inner join user on user.uid = replies.uid
                WHERE pid = %s
                ''', [pid])
    return curs.fetchall()
