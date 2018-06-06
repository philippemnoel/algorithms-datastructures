"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Apriori Algorithm for Finding Frequent Patterns (3 Passes Only) -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import math as math


def apriori(X, threshold, Nmembers, Nsets):
    """ Find Frequent Items above given thresold for dataset X with Nmembers per
        set and Nsets """
    # first apriori pass
    frequent_items = []
    # iterate over full dataset
    for i in range(Nmembers):
        # calculate percentage occurence of each item in entire dataset
        pp = sum(x.count(i) for x in X) / Nsets
        # store if above treshold
        if pp >= threshold:
            frequent_items.append(i)
    # print out results for visualization
    n_freq_items = len(frequent_items)
    print('After first Apriori pass, there are: ' + str(n_freq_items) +
          ' frequent items.')
    # Number Possible Frequent Pairs (NPFP) & Number Possible Pairs (NPP)
    NPFP = int(n_freq_items * (n_freq_items - 1) / math.factorial(2))
    NPP = int(Nmembers * (Nmembers - 1) / math.factorial(2))
    print('This implies ' + str(NPFP) + ' possible frequent pairs, compared with ' +
          str(NPP) + ' possible pairs based on the original data.')

    # second apriori pass
    frequent_pairs = []
    # loop over all sets
    for iset in range(Nsets):
        # scan for all possible pairs of frequent items from first pass
        for item1 in frequent_items:
            for item2 in [x for x in frequent_items if x != item1]:
                pp = sum(min(x.count(item1) * x.count(item2), 1) for x in X) / Nsets
                if pp >= threshold:
                    frequent_pairs.append([[item1, item2], pp])
    # remove duplicates
    unique_fp, unique_fp_keys = [], [] # unique frequent pairs
    for i in frequent_pairs:
        if set(i[0]) not in unique_fp_keys:
            unique_fp.append(i)
            unique_fp_keys.append(set(i[0]))
    # print out for visualization
    n_unique_fp = len(unique_fp) # number of unique frequent pairs
    print('After second Apriori pass, there are: ' + str(n_unique_fp) +
          ' frequent pairs.')
    print('([item1, item2], percentage occurrence of pair)');
    for x in unique_fp:
        print(x)
    # get number of distinct items in our frequent pairs
    items_fp = list(set([item for sublist in [x[0] for x in unique_fp] for item in sublist]))
    n_items_fp = len(items_fp)
    print('The number of distinct items in these frequent pairs is ' + str(n_items_fp) + '.')
    # Number Possible Frequent Triplets (NPFT) & Number Possible Triplets (NPT)
    NPFT = int(n_items_fp * (n_items_fp - 1) * (n_items_fp - 2) / math.factorial(3))
    NPT = int(Nmembers * (Nmembers - 1) * (Nmembers - 2) / math.factorial(3))
    print('This implies ' + str(NPFT) + ' possible frequent triplets, compared with ' +
          str(NPT) + ' possible triplets based on the original items.')

    # third apriori pass
    frequent_triplets = []
    # loop over all sets
    for iset in range(Nsets):
        # scan for all possible pairs of frequent items from first pass
        for item1 in items_fp:
            # tmp list w/out item1 currently being looked at
            b_list = [x for x in items_fp if x != item1]
            # scan for all possible triplets from second pass
            for item2 in b_list:
                # tmp list w/out item1 & item2 currently being looked at
                c_list = [x for x in b_list if x != item2]
                for item3 in c_list:
                    pp = sum(min(x.count(item1) * x.count(item2) * x.count(item3), 1) for x in X) / Nsets
                    if pp >= threshold:
                        frequent_triplets.append([[item1,item2,item3],pp])
    # remove duplicates
    unique_ft, unique_ft_keys = [], [] # unique frequent triplets
    for i in frequent_triplets:
        if set(i[0]) not in unique_ft_keys:
            unique_ft.append(i)
            unique_ft_keys.append(set(i[0]))
    # print out for visualization
    n_unique_ft = len(unique_ft)
    # get number of distinct items in our frequent pairs
    items_ft = list(set([item for sublist in [x[0] for x in unique_ft] for item in sublist]))
    n_items_ft = len(items_ft)
    print('After third Apriori pass, there are: ' + str(n_unique_ft) +
          ' frequent triplets composed of' + str(n_items_ft) + ' diffenret items.')
    print('([item1, item2, item3], percentage occurrence of triplet)');
    for x in unique_ft:
        print(x)
    # association, interest and confidence
    print('We can now infer associations rules (a,b) - >c, (a,c) -> b, ' +
          '(b,c) -> a, which can be tested for confidence and interest.')


# driver test & data generation
# data
X = [[1,2,3,4,7,11,15],
     [1,2,4,5,7],
     [1,2,4,5,6,7,9,11,14],
     [2,3,4,5,6,9,10,12,14],
     [1,2,3,4,5,6,7,8],
     [3,4,5,6,10,11,12,13,14],
     [1,3,4,5,8],
     [1,2,4,5,6,7,10,12,14],
     [1,2,3,4,5,7,9,10],
     [1,2,3,6,8,12,13],
     [1,2,6,7,8,9,11,13,14],
     [1,3,4,5,6,7,9,10,15],
     [1,2,4,7,8,11,13],
     [1,2,3,4,5,6,7,11,12,14],
     [3,4,8,9,11,12,13,15],
     [1,2,3,4,7,9,10,13,14],
     [2,3,5,6,7,8,9,10,15]]
# driver test
apriori(X, 0.5, 15, 17)
