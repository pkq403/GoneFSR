def fibo(n):
    if n < 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

import dis

if __name__=="__main__":
    # dis.dis(fibo)
    print(fibo(18))
