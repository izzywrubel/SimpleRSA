# Isabel Wrubel
# Blockchain COMP412 Homework 1

import math
from random import randrange, getrandbits

# Source:
# Assisted with finding and generating large prime numbers
# https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb

def my_gcd(x,y):
    mx = max(x,y)
    my = min(x,y)
    if my ==0:
        return mx
    else:
        return my_gcd(my,mx%my)

def linear_comb(x,y):
    a, lastA = 0, 1
    b, lastB = 1, 0
    while (y != 0):
        q = x // y
        x, y = y, x % y
        a, lastA = lastA - q * a, a
        b, lastB = lastB - q * b, b
    return (lastA, lastB)

def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    for _ in range(128):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number():
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(8)
    return p

def keys(p,q):
    # calculate n
    n = p*q

    # calculate totient
    tn = (p-1)*(q-1)

    # calculate e
    e = int(math.sqrt(tn+1)//2)
    while ((tn+1)%e != 0):
        e +=1

    #cacluate d
    d = (tn+1)//e

    # final keys (not in tuple form for ease of testing)
    publickey = e
    privatekey = d
    return (publickey, privatekey)

def fastModExp(x,y,p):
    res = 1
    x = x % p

    while (y > 0):
        if ((y % 2) == 1):
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

def encrypt(message,publickey,n):
    cipher = fastModExp(message,publickey,n)
    return cipher

def decrypt(cypher,privatekey,n):
    return fastModExp(cypher,privatekey,n)

# TESTS — RUN FILE TO SEE ENCRYPTION AND DECRYPTION PROCESSES
print("GENERATING PRIMES...")
p = generate_prime_number()
q = generate_prime_number()
print(p,q)
print("GENERATING KEYS...")
print("Public Key: " + str(keys(p,q)[0]))
print("Private Key: " + str(keys(p,q)[1]))
print("ENCRYPTING MESSAGE...")
publickey = keys(p,q)[0]
n = p*q
print(encrypt(20,publickey,n))
cipher = encrypt(20,publickey,n)
print("DECRYPTING MESSAGE...")
privatekey = keys(p,q)[1]
print(decrypt(cipher,privatekey,n))
