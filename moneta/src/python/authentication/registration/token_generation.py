" Module for generating JWT token for registration "
import jwt

TEMPORARY_SECRET = '''ATTENTION THIS IS TEMPOARARY SECRET,
                      it should be stored in local settings or another hidden file'''


def generate_token(email):
    '''
    take user email as string, and return JWT token in str format
    encryption algorithm HS256
    '''

    encoded_jwt = jwt.encode({'email': email}, TEMPORARY_SECRET, algorithm='HS256')
    token_as_str = encoded_jwt.decode('utf-8')
    return token_as_str
