"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 5 - Springbreak
Python version of Springbreak
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" Subroutine code for the SubsetSum algorithm w/out infinite coins """
def CoinsCount(coins_list, M):
    # coins_list is a list of tuple (value, qty) of coins
    # initialize lookup table that contains whether this value can be done
    table = [1] + [0] * M
    # iterate over all coins
    for value, qty in coins_list:
        # tmp_table we use to get all the qty points
        tmp_table = table[:]
        for i in range(value, M + 1):
            tmp_table[i] += tmp_table[i - value]
            # constant time processing (sort of)
            if i < value * (qty + 1):
                table[i] += tmp_table[i - value]
            else:
                table[i] += tmp_table[i - value] - tmp_table[i - value * (qty + 1)]
    # get whether or not this value can be represented and return count
    # starting at -1 to adjust for M = 0
    count = -1
    for value in table:
        if value:
            count += 1
    return count

""" Subroutine code for the Springbreak Algorithm """
def springbreak():
    # read number of cases T
    T = int(raw_input())
    # list that contains the number of denom and max payment for all test cases
    d_list, M_list = [], []
    # arrays that contains list of each coin values and their qty for each test
    coins_values = [[] for x in range(T)]
    coins_qty = [[] for x in range(T)]
    # read test cases one at a time and store them
    for test_case in range(T):
        # get number of denominations and the max payment for this test
        d, M = map(int, raw_input().split())
        # store them
        d_list.append(d)
        M_list.append(M)
        # append list of all coin_values for this test to our list, dito for qty
        coins_values[test_case] += list(map(int, raw_input().split()))
        coins_qty[test_case] += list(map(int, raw_input().split()))
    ### All inputs read --- Now processing all tests ###
    # deal with test cases one at a time
    for test_case in range(T):
        # get d, M, coins values and qty for the current test
        d = d_list[test_case]
        M = M_list[test_case]
        values = coins_values[test_case]
        qty = coins_qty[test_case]
        # zip lists into a list of tuples
        coins_set = zip(values, qty)
        # output number of ways to get change
        print(CoinsCount(coins_set, M))

""" Function call for testing """
springbreak()
