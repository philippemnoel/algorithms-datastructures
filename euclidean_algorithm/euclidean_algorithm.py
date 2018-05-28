"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Euclidean Algorithm - Finding Greatest Common Divisor -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def gcd(a, b):
    """ Finds greatest common divisor of a and b """
    # sanity check
    if a < 1 or b < 1:
        return "Need a & b greater or equal to 1"
    # algorithm
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    # render success
    return a
