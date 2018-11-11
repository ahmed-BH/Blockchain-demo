class Blockchain:
    __slots__ = ["head", "nb_blocks"]

    def __init__(self):
        self.head      = None
        self.nb_blocks = 0

    def add_block(self, block):
        block.prev = self.head
        if self.head is not None:
            block.previous_hash = self.head.hash

        self.head  = block
        self.nb_blocks += 1
        self.head.mine()

    def get_weight(self):
        weight   = 0
        tmp_head = self.head

        while tmp_head is not None:
            weight  += tmp_head.difficulty
            tmp_head = tmp_head.prev

        return weight  


    def show_blocks(self):
        tmp_head = self.head
        i = 1
        while tmp_head is not None:
            print("[Block {}] {}".format(i, tmp_head))
            tmp_head = tmp_head.prev
            i       += 1
    