import wworks_db as dbi




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
                 where body like %s
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
                 where body like %s
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

