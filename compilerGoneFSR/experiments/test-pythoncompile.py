def hello(a, b):
    print(f"{a}, can u hear {b}?")
if __name__=='__main__':
    code_object = compile('x = 5; x += 1', '<string>', 'exec')
    print(code_object.co_code)
