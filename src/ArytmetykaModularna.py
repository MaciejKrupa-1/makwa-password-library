"""
Euclidean algorithm
* Compute the greatest common divisor (GCD) of two numbers
Inputs:
* a (int) - first number
* b (int) - second number
Output:
* (int) - the greatest common divisor of a and b
"""
def nwd(a,b):
    while a > 0 and b > 0:
        temp = b
        b = a % b
        a = temp
    if a == 0:
        return b
    if b == 0:
        return a
"""
Extended Euclidean algorithm
* Compute the modular inverse of a modulo b 
Inputs:
* a (int) - the number to invert modulo b
* b (int) - the modulo
Output:
* (int) or None - modular inverse of a modulo b if it exists, otherwise None 
"""
def reverseModulo(a,b):
    if nwd(a,b) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, b
    while v3 != 0:
        q = u3 // v3
        v1,v2,v3,u1,u2,u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3),v1,v2,v3
    return u1 % b
"""
Extended Euclidean algorithm
* Solves the system of congruences using the Chinese Remainder Theorem (CRT).
Inputs:
* x_p (int) - solution modulo p
* p (int) - modulus p (should be coprime with q)
* x_q (int) - solution modulo q
* q (int) - modulus q (should be coprime with p)
Output:
* result (int) - the solution modulo p * q  
"""
def CRT(x_p, p, x_q, q):
    n = p * q
    q_inv = reverseModulo(q, p)
    p_inv = reverseModulo(p, q)
    result = (x_p * q * q_inv + x_q * p * p_inv) % n
    return result
"""
Main Makwa computation without factorization of N.
Computes x raised to the power 2^roundNumber modulo N using Python's built-in pow for fast exponentiation.
Inputs:
* x (int) - base
* N (int) - modulus
* roundNumber (int) - number of rounds (mcost in makwa algorithm)
Output:
* (int) - result of x^(2^roundNumber) mod N
"""
def normalPath(x, N, roundNumber):
    exponent = 2 ** roundNumber
    return pow(x, exponent, N)

"""
Main makwa computes with known factorisation of N
* Performs computations modulo p and q separately, which leads to faster calculation of the result.
Inputs:
* x (int) - base
* p (int) - first prime factor   of modulus
* q (int) - second prime factor of modulus
* roundNumber (int) - number of rounds (mcost in makwa algorithm)
Output:
* (int) - combined result modulo p * q
"""
def quickPath(x, p, q, roundNumber):
    e_p = pow(2, roundNumber, p-1)
    e_q = pow(2, roundNumber, q-1)

    x_p = pow(x, e_p, p)
    x_q = pow(x, e_q, q)
    return CRT(x_p, p, x_q, q)




