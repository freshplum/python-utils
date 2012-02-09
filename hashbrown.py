from hashlib import md5 as hashlib_md5

def md5(key):
    """
    Create md5 hash
    """
    m = hashlib_md5()
    m.update(str(key))
    return m.hexdigest()
