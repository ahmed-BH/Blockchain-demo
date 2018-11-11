from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

# --------- My Modules ----------
import utils.settings as settings
# -------------------------------

def generate_encryption_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    public_key = private_key.public_key()
    
    return {"public_key": public_key, "private_key": private_key}

def save_fs(keys):
    pem = keys["private_key"].private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(settings.PRIV_KEY_PATH, 'wb') as pem_out:
        pem_out.write(pem)

    pem = keys["public_key"].public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(settings.PUB_KEY_PATH, 'wb') as f:
        f.write(pem)

def get_private_pem(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

def get_public_pem(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def load_encryption_keys(priv=settings.PRIV_KEY_PATH, pub=settings.PUB_KEY_PATH):
    with open(priv, 'rb') as pem_in:
        private_key = load_pem_private_key(pem_in.read(), None, default_backend())
    
    with open(pub, 'rb') as pem_in:
        public_key = load_pem_public_key(pem_in.read(), default_backend())

    return {"public_key": public_key, "private_key": private_key}

def encrypt(key, data):
    return key.encrypt(
    data.encode(),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

def decrypt(key, encrypted):
    plaintext = key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )

    return plaintext.decode("utf8")

def sign(message, private_key):
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
     hashes.SHA256()
    )

def valid_signature(message, public_key, signature):
    try:    
        sig = public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature as e:
        return False


