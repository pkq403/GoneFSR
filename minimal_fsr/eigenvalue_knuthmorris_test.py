from knuthMorrisPratt import KnuthMorrisPratt
from eigenvalue import eigenvalue
a = [1,0,0, 0, 0, 1]
n = 3
print(eigenvalue(a,n))
text = [0,0,0,0]
patt = [1,0,0,0,0]

print(KnuthMorrisPratt(text, patt))
