import datetime
import hashlib

class Block:
    __slots__ = ["hash", "previous_hash", "nonce", "timestamp", "data", "prev", "difficulty"]

    def __init__(self, data):
        self.hash          = ""
        self.previous_hash = ""
        self.nonce         = 0
        self.timestamp     = str(datetime.datetime.utcnow())
        self.data          = data
        self.prev          = None
        self.difficulty    = 5

    def mine(self):
        if not self.data.is_valid(): raise ValueError("Invalid Transaction's Signature ! ")
        
        tmp_hash   = ""
        self.nonce = 0
        while not tmp_hash.startswith("0"*self.difficulty):
            ref = hashlib.sha256()
            ref.update(self.previous_hash.encode())
            ref.update(self.timestamp.encode())
            ref.update(self.data.to_bytes())
            ref.update(str(self.nonce).encode())
            
            tmp_hash   = ref.hexdigest()
            self.nonce += 1
        
        self.nonce -=1 
        self.hash   = tmp_hash

    def is_valid(self):
        if not self.data.is_valid():
            return False

        ref = hashlib.sha256()
        ref.update(self.previous_hash.encode())
        ref.update(self.timestamp.encode())
        ref.update(self.data.to_bytes())
        ref.update(str(self.nonce).encode())

        return self.hash == ref.hexdigest() and self.hash.startswith("0"*self.difficulty)

    def __str__(self):
        return " hash: {}\n prev_hash: {}\n nonce: {}\n timestamp: {}\n data: {}\n difficulty: {}".format(
            self.hash,self.previous_hash,self.nonce,self.timestamp,self.data,self.difficulty)