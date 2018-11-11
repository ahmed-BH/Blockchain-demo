# -------- My Modules ---------
import utils
# -----------------------------

class Transaction:
    __slots__ = ["sender", "receiver", "assets", "fee", "signature"] 

    def __init__(self, **kargs):
        assert list(kargs.keys()) == ["sender", "receiver", "assets"], 'Keys must be "sender", "receiver", "assets" '
        
        self.sender    = kargs.get("sender", None)
        self.receiver  = kargs.get("receiver", None)
        self.assets    = kargs.get("assets", None)
        self.fee       = "3"
        
        assert self.sender   is not None, '"sender" value should be specified'
        assert self.receiver is not None, '"receiver" value should be specified'
        assert self.assets   is not None, '"assets" value should be specified'
        
        self.signature = ""

    def sign(self, sender_priv_key):
        data_to_sign   = utils.encryption.get_public_pem(self.sender) + utils.encryption.get_public_pem(self.receiver) \
        + self.assets.encode() + self.fee.encode()

        self.signature = utils.encryption.sign(data_to_sign, sender_priv_key)

    def is_valid(self):
        data_to_valid = utils.encryption.get_public_pem(self.sender) + utils.encryption.get_public_pem(self.receiver) \
        + self.assets.encode() + self.fee.encode()
        
        return utils.encryption.valid_signature(data_to_valid, self.sender, self.signature)

    def to_bytes(self):
        return utils.encryption.get_public_pem(self.sender) + utils.encryption.get_public_pem(self.receiver) \
        + self.assets.encode() + self.fee.encode() + self.signature
    


