from itertools import islice
from esop import ESOP
from eigenvalue import eigenvalue

def non_linear_complexity(s,l): 
    # Calculates the nonlinear complexity of the whole sequence
    k = 0 # jump
    m = 0 # complexity
    y = islice(s,0,l)
    h = ESOP(next(y)) # feedback

    for n0, yn in enumerate(y):
        n = n0 + 1 # The index starts in 1, porque haces un next al principio para cargar el ESOP
        d = h.discrepancy(s,n) # discrepancy h(x)
        #print("")
        #print("[*] iteracion")
        #print("processing: ", s[:n+1])
        #print("salto k: ", k)
        #print("nlc m: ", m)
        if d:
            #print("[!] Discrepancia!!")
            if not m:
                #print("Inicializa discrepancia")
                k = n
                m = n
            elif k <= 0:
                t = eigenvalue(s,n) # eigenvalue = period + preperiod
                if t < n + 1 - m:
                    #print("[!!!] Actualiza NLC")
                    # se produce un salto en la complejidad no lineal
                    #print("m salto en: ", n)
                    #print("eigenvalue: ", t)
                    #print("antigua m: ", m)
                    k = n + 1 - t - m # c(y^n) - c(y^n-1)
                    m = n + 1 -t # n - k(y^n) = c(y^n)
                    #print("nueva m: ", m)
            h.add(s, n0, m)
        k -= 1
        #print("")
    return h
