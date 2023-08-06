import random as re
from math import sqrt
max = 10000000


def gcd(a, b):
    '''for finding the Greatest Common Divisor or Highest Common Factor between two numbers.
    It's purpose for this program is to check whether e and phi_of_n are co-prime or not,
    which is possible iff their gcd is 1.
    '''
    while b != 0:
        a, b = b, a % b
    return a


def mm_inverse(a,b):
    '''to calculate the modular multiplicative inverse of a mod b using Extended Euclidean
    Algorithm,iff a and b are co-prime.Its primary purpose is to find the same for e & phi.
    '''
    m=b
    a,b=b,a
    q,r=a//b,a%b
    t1,t2=0,1
    t=t1-q*t2
    while(b!=0):
        a,b=b,a%b
        t1,t2=t2,t
        if b!=0:
            q,r=a//b,a%b
            t=t1-q*t2
    if t1<0:
        t1+=m
    return t1


def isPrime(num):
    '''to check whether a number is prime or not.
    Its purpose is to check whether the numbers, p,q and e are prime.
    '''
    if num == 2 or num==3:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(sqrt(num)) + 2, 2):
        if num % n == 0:
            return False
    return True


def random_Prime():
    '''to generate two random prime numbers, primarily p and q.'''
    while 1:
        ranPrime = re.randint(53, max)  # generate large prime numbers for greater security
        if isPrime(ranPrime):
            return ranPrime


def key_Pairs():
    '''to generate the p and q, and
    the public and private key value pairs for the RSA Algorithm.
    '''
    p = random_Prime()
    q = random_Prime()
    n = p * q
    '''phi(n) is known as Euler's Totient Function. Here, phi(n)=phi(p)*phi(q), since,
    p and q are co-prime. Since, p and q are prime numbers, hence, phi(p)=p-1 and
    phi(q)=q-1, since, except themselves, they have no other factors (excluding 1).'''
    phi = (p - 1) * (q - 1)
    e = re.randint(2, phi-1)  # since 1<e<phi(n)
    g = gcd(e, phi)
    while g != 1:
        e = re.randint(2, phi-1)
        g = gcd(e, phi)
    d = mm_inverse(e, phi)
    return (e, n), (d, n)


def encrypt_data(plain_text, public_key):
    '''to encrypt the plain_text into a list of some numbers.'''
    key, n = public_key
    '''pow(a,b,m) is an in-built function which takes 3 arguments, converts them to float,
    and then computes {(a to the power of b) modulus of m}.'''
    ctext = [pow(ord(char), key, n) for char in plain_text]
    return ctext


def decrypt_data(ctext, private_key):
    '''to decrypt the cipher text into the original text'''
    try:
        key, n = private_key
        text = [chr(pow(char, key, n)) for char in ctext]
        return "".join(text)
    except TypeError as e:
        print(e)