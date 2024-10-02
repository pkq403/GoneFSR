from collections import deque
from itertools import islice
from binary_op import XOR, AND, NOT
#import pdb

class ESOP: # Exclusive Sum of Products
    '''
    Class to represent polynomials with binary coefficients.The exclusive-sum of products 
    is actually very well known.
    '''
    def __init__(self, valor):
        self.m = 0
        self.independent = 1 if valor else 0
        self.coefficients = []

    def discrepancy(self, s, n):
        values = deque(islice(s,n-self.m,n+1))
        result = values.pop()
        return XOR(result,self.evaluate(values)) # si el result no coincide con el h(result)
                                                 # se produce una discrepancia y se sumara un minterm
                                                 # aunque no tiene, porque aumentar la complejidad ya
                                                 # que esto dependera de la condicion del salto
                                                 # k <= 0
    def evaluate(self, values): # usar esta funcion para descomprimir a partir de los minterms/coefs
        '''
        the length of values must be m.
        '''
        result = self.independent
        for coef in self.coefficients:
            result = XOR(result, all([XOR(values[-i-1],v) for i,v in coef])) # El por que de esto?
        return result

    def add(self, s, n0, m):
        n = n0 + 1
        #print("\n[*] poly antes: ", self.__str__())
        #print("[*] h + f (add minterm): ")
        #print("[*] n: ", n)
        #print("[*] m (actual nlc): ", m)
        values = deque(islice(s,n-m,n))
        values.reverse() # les da la vuelta, para que le cuadren despues las posiciones de x0, x1...
        self.coefficients.append([(i,NOT(v)) for i,v in enumerate(values)])
        self.m = m
        #print("polinomio ahora: ", self.__str__(), "\n")

    def get_initial_term(self):
        return self.independent

    def get_binary_terms_poly(self):
        binaries_terms = []
        for coef in self.coefficients:
            bin_term = ''
            for i, j in coef: bin_term += '1' if j else '0' # 0 for neg literal, 1 for no neg literal
            binaries_terms.append(bin_term)
        return binaries_terms

    def __str__(self):
        result = '1' if self.independent else '0'
        for coef in self.coefficients:
            result += '+'+'*'.join(['(x%s+1)'%(i) if j else 'x%s'%i for i,j in coef])
        return result 
