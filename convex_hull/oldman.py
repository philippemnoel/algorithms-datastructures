"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 4 Extra Credit - Oldman
Python version of Oldman
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" Subroutine code for vectors crossproduct with same origin """
def v_cp(o, x, y):
    # returns positive if OXY proceeds counterclockwise, else negative for
    # clockwise and zero if they are collinear
    return (x[0] - o[0]) * (y[1] - o[1]) - (x[1] - o[1]) * (y[0] - o[0])

""" Subroutine code for Andrew's Monotone Chain Algorithm """
def ConvexHull(points):
    # base case
    if len(points) <= 1:
        return points
    # sort lexicographically
    contracts = sorted(points)
    # initialize lower hull and upper hull
    lowhull, uphull = [], []
    # iteratively build the lower hull
    for point in contracts:
        while len(lowhull) > 1 and v_cp(lowhull[-2], lowhull[-1], point) < 0:
            lowhull.pop()
        lowhull.append(point)
    # iteratively build the upper hull
    for point in reversed(contracts):
        while len(uphull) > 1 and v_cp(uphull[-2], uphull[-1], point) < 0:
            uphull.pop()
        uphull.append(point)
    # concatenate lower and upper hull to get full convex hull
    return lowhull[:-1] + uphull[:-1]

""" Subroutine code for Oldman algorithm """
def oldman():
    # read m (sell contracts) and n (buy contracts)
    m, n = map(int, raw_input().split())
    # value that will be outputted
    profits = 0
    # contracts dicitonaries, we only save the cheapest or most expensive
    # value for each date if many similar dates
    buys, sells = dict(), dict()
    # initialize lowest sell price variable and most exp buy price variable
    lowest_sell, most_exp_buy = None, None
    # initialize earliest sell and latest buy
    earliest_sell, latest_buy = None, None
    # fill sell dictionary
    for i in range(m):
        # (price, starting date)
        p_i, d_i = map(int, raw_input().split())
        # get lowest sell
        if lowest_sell == None or p_i < lowest_sell:
            lowest_sell = p_i
        # get earliest sell
        if earliest_sell == None or d_i < earliest_sell:
            earliest_sell = d_i
        # no value at this date or higher cost
        if sells.get(d_i) == None or sells.get(d_i) > p_i:
            sells[d_i] = p_i
    # fill buy dicitonary
    for j in range(n):
        # (price, end_date)
        q_j, e_j = map(int, raw_input().split())
        # get most exp buy
        if most_exp_buy == None or q_j > most_exp_buy:
            most_exp_buy = q_j
        # get latest buy
        if latest_buy == None or e_j > latest_buy:
            latest_buy = e_j
        # if no value at this date or current price is higher than the previously
        # stored price we update (we want the highest buy price). If the price is
        # lower or equal than the lowest sell price, we don't take it or if the
        # date is earlier than earliest sell we don't take it
        if buys.get(e_j) == None:
            buys[e_j] = q_j
        elif buys.get(e_j) < q_j and q_j > lowest_sell and e_j > earliest_sell:
            buys[e_j] = q_j
    # convert all to arrays after removing similar dates (date, price)
    extreme_buys, extreme_sells = [], []
    # buys case (value = date / buys.get(value) = price)
    for value in buys:
        extreme_buys.append((value, buys.get(value)))
    # sells case
    # we also trim values here according to our buy
    for value in sells:
        # price, date = value
        price = sells.get(value)
        # if sell price is greater or equal to our most expensive buy, then we
        # definitely don't want it, or if the date starts on or after our
        # latest buy, then we definitely don't want it
        if price < most_exp_buy and value < latest_buy:
            extreme_sells.append((value, price))

    # divide and conquer part
    sell_contracts = extreme_sells
    buy_contracts = extreme_buys

    # brute-force case for n,m <= 3000
    # convex hull needs at least 3 points
    if n <= 3000 and m <= 3000 or n < 3 or m < 3:
        for buy in buy_contracts:
            for sell in sell_contracts:
                if buy[1] > sell[1]:
                    contract = (buy[0] - sell[0]) * (buy[1] - sell[1])
                    if contract > profits:
                        profits = contract
    # convex hull method
    else:
        # get the convex hulls points of our first layer
        extreme_sells = ConvexHull(sell_contracts)
        extreme_buys = ConvexHull(buy_contracts)

    # calculate all extreme profits in a brute-force manner and pick highest
    for buy in extreme_buys:
        for sell in extreme_sells:
            if buy[0] > sell[0]:
                contract = (buy[0] - sell[0]) * (buy[1] - sell[1])
                if contract > profits:
                    profits = contract
    # render success
    print(profits)

""" Function call for testing """
oldman()
