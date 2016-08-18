from . import get_db
import random
import string


def gen_filename(length=5, source=string.ascii_letters+string.digits):
    ''' Generate random string to use as filename/url
        and check if it already exists

        length -- length of string to generate
        source -- characters to use in random string
    '''
    db = get_db()
    while True:
        filename = ''.join(random.choice(source) for __ in range(length))
        cur = db.execute('select * from Pictures where filename=?', (filename,))
        if not cur.fetchone():
            break
    return filename


def get_extension(filename):
    ''' Return the file extension from filename
        filename -- filename from which to return the extension
    '''
    return filename.rsplit('.', 1)[1]


def fetch_file(filename):
    db = get_db()
    cur = db.execute('select * from Pictures where filename=?', (filename,))
    return cur.fetchone()
