from email.utils import formatdate
from time import time
from datetime import tzinfo


def get_current_local_time():
    return formatdate(time(), tzinfo())