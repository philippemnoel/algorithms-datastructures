##
 # sieve_of_eratosthenes.py
 #
 # Language: Python 2
 #
 # Program to print all primes smaller than or equal to a given number n using
 # Sieve of Eratosthenes.
 ##

from __future__ import print_function

def sieve_of_eratosthenes(n):
    # initialize boolean array with all entries as true
    # entries in primes will be false if not a prime, else true
    primes = [True for i in range(n + 1)]

    # iterate over the array, checking for primes
    p = 2
    while (p * p <= n):
        # if primes[p] is true, then it is a prime
        if primes[p]:
            # update all multiples of p as not primes
            for i in range(p * 2, n + 1, p):
                primes[i] = False
        p += 1

    # print all prime numbers for visual confirmation
    for p in range(2, n):
        if primes[p]:
            print(p, " ", end='')
    print()

    # render success
    return 0

if __name__=='__main__':
    # prompt user for an integer >= 2
    print("Enter a valid integer above 1: ", end='')
    while True:
        try:
            n = input()
        except ValueError:
            print("Invalid input, please try again: ", end='')
            continue
        if n < 2:
            print("Invalid input, please try again: ", end='')
            continue
        else:
            break

    # output primes
    print("Following are the prime numbers smaller than ", end='')
    print("or equal to {}:".format(n))
    sieve_of_eratosthenes(n)
