
import pynetbox

def netbox_connect(url, token):
    ''''''
    # add exception handling
    nb = pynetbox.api(url, token)
    return nb
