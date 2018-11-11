import os.path as path
from os import mkdir

PATH = path.join(path.dirname(__file__),"keys")
if not path.exists(PATH):
    mkdir(PATH)

PRIV_KEY_PATH = path.join(PATH, "priv_key.pem") 
PUB_KEY_PATH  = path.join(PATH, "pub_key.pem") 

