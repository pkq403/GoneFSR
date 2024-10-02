# Depende de a cual llames antes al ser interpretado no hay confusion
def a():
    print("soy a ")

a()
a = 2
print(a)

