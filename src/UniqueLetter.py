def alphabet(x):
    if x < 26:
        return chr(x + ord('a'))
    else:
        return chr((x % 26) + ord('a')) + alphabet(x-26)

class UniqueLetter:
    def __init__(self):
        self.mapping = {}

    def __getitem__(self, key):
        if not key in self.mapping:
            self.mapping[key] = self.next()
        return self.mapping[key]
  
    def next(self):
        return alphabet(len(self.mapping))
 



