"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 6 - Countproducts
Python version of Countproducts
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" Subroutine code for Coundproducts algorithm """
def countproducts():
    # get number of numbers
    n = int(raw_input())
    # list of potential primes to be used for the randomized algorithm
    # taken from https://primes.utm.edu/lists/small/millions/
    primes = [11717,20123,53051,95287,383321,15485863]
    # result counter
    count = 0
    # identity we use to speed up calculations
    # (a * b) % p = ((a % p) * (b % p)) % p
    # set of all distinct numbers and list of numbers
    nums = []
    nums_set = set()
    for num in range(n):
        curr_num = int(raw_input())
        # we try multiple size primes since we have a randomized alg
        nums.append(curr_num)
        nums_set.add(curr_num % primes[3])
        nums_set.add(curr_num % primes[4])
        nums_set.add(curr_num % primes[5])
    # loop and brute-force all comparisons using the identity above
    i = 0
    while i < n:
        for j in range(i + 1, n):
            curr1 = ((nums[i] % primes[3]) * (nums[j] % primes[3])) % primes[3]
            curr2 = ((nums[i] % primes[4]) * (nums[j] % primes[4])) % primes[4]
            curr3 = ((nums[i] % primes[5]) * (nums[j] % primes[5])) % primes[5]
            # make sure all of them work
            if curr1 in nums_set and curr2 in nums_set and curr3 in nums_set:
                count += 1
        i += 1
    # output result
    print(count)

""" Function call for testing """
countproducts()
