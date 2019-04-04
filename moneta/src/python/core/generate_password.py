"""Module to generate a new password."""
import random
import string

def random_string(stringlength=10):
    """Generate a random string of fixed length."""
    password = string.ascii_lowercase
    return ''.join(random.choice(password) for i in range(stringlength))