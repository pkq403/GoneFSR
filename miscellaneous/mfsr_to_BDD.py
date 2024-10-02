from BDD_node import BDDnode
from utils import logic_poly_executer
# Author: Pedro Castro
def msfr_to_BDD(msfr_poly, n):
    '''
    Constructs a BDD (Binary Decision Diagram) from
    an string representing the msfr polynomio of a sequence
    Space complexity -> O(2^n) n -> being the number of parameters (x1, ..., xn)
    Parameters
    ----------
    - msfr polynomio : string
    - n : int -> number of variables
    Returns
    -------
    a node which is the root of the BDD 
    '''
    n2 = 2**n
    root = BDDnode(name="x0")

    for i in range(n2):
        params = bin(i)[2:].zfill(n)
        cur = root
        values = []
        for j in range(n):
            param_val = int(params[j])
            values.append(param_val)
            if j == n - 1:
                side = param_val
                break
            if param_val: # xn'
                if cur.left is None:
                    cur.left = BDDnode(name=f"x{j+1}")
                cur = cur.left
            else: # xn
                if cur.right is None:
                    cur.right = BDDnode(name=f"x{j+1}")
                cur = cur.right
        res = logic_poly_executer(poly, values)
        if side:
            cur.left = BDDnode(name="res", val=res)
        else:
            cur.right = BDDnode(name="res", val=res)
        return root



