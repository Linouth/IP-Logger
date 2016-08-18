from .database import db_session
from .models import Picture
import random
import string


def gen_filename(length=5, source=string.ascii_letters+string.digits):
    ''' Generate random string to use as filename/url
        and check if it already exists

        length -- length of string to generate
        source -- characters to use in random string
    '''
    while True:
        filename = ''.join(random.choice(source) for __ in range(length))
        pic = Picture.query.filter(Picture.filename == filename).first()
        print(pic)
        if not pic:
            break
    return filename


def get_extension(filename):
    ''' Return the file extension from filename
        filename -- filename from which to return the extension
    '''
    return filename.rsplit('.', 1)[1]
