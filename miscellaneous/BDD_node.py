'''
BDD node Class
Written by Pedro Castro
'''
class BDDnode:
    def __init__(self, name="not named", left=None, right=None, val=None):
        self.name = name
        self.left = left
        self.right = right
        self.value = val

    def __str__(self):
        if self.value is None:
            return self.name + '\t left: (' + self.left.__str__() + ')\t right: (' + self.right.__str__() + ')\n'
        return str(self.value)
