import wworks_db as dbi


def insert_post(conn, title, body, categories, type):
    '''
    Helper function to insert a created post into the database
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 INSERT INTO post(title, body, categories, type)
                 VALUES (%s, %s, %s, %s)
                 ''', [title, body, categories, type])
    conn.commit()

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

def find_service(conn, key_phrase):
    '''
    Helper function to find posts including the relevant keyword 
    for a service 
    '''
    curs = dbi.dict_cursor(conn)
    key_phrase = '%' + key_phrase + '%'
    curs.execute('''
                 select *
                 from post
                 where body like %s and type = 'request'
                 ''', [key_phrase])
    results = curs.fetchall()
    return results


def find_provider(conn, key_phrase):
    '''
    Helper function to find users who can provide a service
    based on the categories that the "provider" has linked to
    their account
    '''
    curs = dbi.dict_cursor(conn)
    key_phrase = '%' + key_phrase + '%'
    curs.execute('''
                 select *
                 from post
                 where body like %s and type = 'provision'
                 ''', [key_phrase])
    results = curs.fetchall()
    return results

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

