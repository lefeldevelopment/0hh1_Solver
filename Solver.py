class Solver:
    """
    Solves A 0h h1 game.
    
    None = Empty field
    0 = Red
    1 = Blue
    """
    def __init__(self, field) -> None:
        self.field = field
        self.size = len(field)
    
    # 0->1, 1->0
    def _other(self,num):
        return int(not num)
    
    def _rotate(self):
        self.field = list(map(list,zip(*self.field)))
    
    @property
    def solved(self):
        for row in self.field:
            if None in row:
                return False
        else:
            return True
    
    # only 2 same color
    def solve_max(self):
        for row in self.field:
            # next 2 each other
            for slot_idx in range(self.size-1):
                if row[slot_idx] == row[slot_idx+1] and row[slot_idx] != None:
                    for replacer in [slot_idx-1,slot_idx+2]:
                        if replacer in range(self.size):
                            row[replacer] = self._other(row[slot_idx])
            # as hole
            for slot_idx in range(self.size-2):
                if row[slot_idx] == row[slot_idx+2] and row[slot_idx] != None:
                    row[slot_idx+1] = self._other(row[slot_idx])
    
    # same amount in a row
    def solve_amount(self):
        for row in self.field:
            zero = row.count(0)
            one = row.count(1)
            if zero*2 == self.size:
                obj = 0
            elif one*2 == self.size:
                obj = 1
            else:
                continue
            for slot_idx in range(self.size):
                if row[slot_idx] == None:
                    row[slot_idx] = self._other(obj)
    
    # row only 1x
    def solve_doubbles(self):
        check_a = []
        check_b = []
        for v in self.field:
            if v.count(None) == 2:
                check_b.append(v)
            elif not v.count(None):
                check_a.append(v)

        for a in check_a:
            for b in check_b:
                if all(x == y for x, y in zip(a, b) if y != None):
                    for i in range(self.size):
                        if b[i] == None:
                            b[i] = int(not a[i])
        
    def run_one_time(self):
        for _ in range(2):
            self.solve_max()
            self.solve_amount()
            self.solve_doubbles()
            self._rotate()
    
    def mainloop(self):
        old = []
        while not self.solved:
            self.run_one_time()
            if self.field == old:
                break
            old = self.field.copy()
            

    def output(self):
        print(self)
        
    def __repr__(self):
        out = []
        for row in self.field:
            row = map(lambda slot: str(slot) if slot != None else "_", row)
            out.append(" ".join(row))
        return "\n".join(out)


# test
if __name__ == "__main__":
    f = [
        [None,None,1,None,None,None],
        [None,None,None,None,None,None],
        [0,None,None,0,1,None],
        [None,None,None,0,None,None],
        [None,None,None,None,1,None],
        [0,0,None,1,None,None]
        ]

    s = Solver(f)

    s.mainloop()
    s.output()
