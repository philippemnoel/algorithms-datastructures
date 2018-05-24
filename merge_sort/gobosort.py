"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 1 - GoboSort
Python version of GoboSort
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import math
import operator

# global unsorted array to keep track of the number of unsorted pair per power
# of 2 of the arrays (global cuz lazy af)
unsorted_count_array = []
inverse_unsorted = []

# bool to trigger which array to fill
which_array = False


""" Code for the split subroutine according to GoboSort specifications """
def split_arr(array, i, q_k):
    return list(reversed(array[i * (2 ** q_k):(i + 1) * (2 ** q_k)]))


""" Code for the merge and inversion counting subroutine """
def merge_count(arr1, arr2):
    global unsorted_count_array
    global inverse_unsorted
    global which_array
    # define output array
    output_arr = []

    # save at which power index we are by computing original length of arr2 to
    # know at which power of 2 we are at and using the log base 2 to find the power
    power = int(math.log(len(arr2), 2))

    # replacing the append [0] and remove [0] everytime by an increasing index
    # since array.remove takes O(n) time and my algorithm was too frikkin' slow
    # unnecessarily
    # keep a different index for each array cuz I want to stay at 0 even if one
    # array increases
    index1 = 0
    index2 = 0

    #save lengths to save redundant computations
    len1 = len(arr1)
    len2 = len(arr2)

    # if both arrays non-empty, check which value is the smallest and append
    while index1 != len1 and index2 != len2:
        # <= since if they are equal, it is not an inversion
        if arr1[index1] <= arr2[index2]:
            output_arr.append(arr1[index1])
            index1 += 1
        else:
            # we put arr2 before arr1, so everything in arr1 is to be inverted,
            # so we add it's length of inversions to the appropriate power index
            if which_array == False:
                unsorted_count_array[power] += len1 - index1
            else:
                inverse_unsorted[power] += len1 - index1
            output_arr.append(arr2[index2])
            index2 += 1
    # if one array is empty, just add the other one
    if index1 == len1:
        output_arr += arr2[index2:]
    else:
        output_arr += arr1[index1:]
    # return the merged array and the increment unsorted counter
    return output_arr


""" Code to recursively split an array in subarrays """
def merge_split(array):
    # save lengths for speed
    len_arr = len(array)
    # empty or single value array, can't be split more
    if len_arr == 0 or len_arr == 1:
        return array
    # larger than single value array, split in 2 and re-split until base case
    else:
        # case to int to round
        mid = int(len_arr / 2)
        # recursive calls
        first_half = merge_split(array[:mid])
        second_half = merge_split(array[mid:])
        # call the merging and counting subroutine
        return merge_count(first_half, second_half)


""" Code for the GoboSort algorithm """
def gobosort():
    global unsorted_count_array
    global inverse_unsorted
    global which_array
    # read inputs (arr len, # of ops, array itself, list of ops to be done)
    n, m = map(int, raw_input().split())
    array = list(map(int, raw_input().split()))
    q_klist = list(map(int, raw_input().split()))

    # if we are given an empty array, then there are 0 unsorted elements
    arr_len = len(array)
    if arr_len == 0 or arr_len == 1:
        print(0)

    # run the merge sort and count all the inversions in powers of 2
    tmp_arr = []
    num_arrays = 2 ** (n - q_klist[0])
    for i in range(num_arrays):
        tmp_arr += split_arr(array, i, q_klist[0])

    # initialize unsortedness counting array (both ways to compute total
    # number of possible inversions)
    unsorted_count_array = [0] * n
    inverse_unsorted = [0] * n

    # inverse initially modified array
    inverse_tmp_arr = tmp_arr[::-1]

    # run the merge sort counting on normal array
    merge_split(tmp_arr)

    # switch to fill the inverse array
    which_array = True

    # run the merge sort counting on inverse array
    merge_split(inverse_tmp_arr)

    # total potential inversion array
    total_potential_inversions = list(map(operator.add, unsorted_count_array, inverse_unsorted))

    # save the first unsorted count and output it
    current_unsorted = sum(unsorted_count_array)
    print(current_unsorted)

    # runs the unsorting counting algorithm for each q_k value (m times) after
    # the first value (we only run the mergesort once)
    for i in range(m - 1):
        # q_k and number of subarrays for this iteration and their length
        q_k = q_klist[i + 1]
        n_arrays = 2 ** (n - q_k)

        # if we all have arrays of length 1, then the array does not change
        # and the unsortedness counter is the same as it previously was
        if n_arrays == arr_len:
            print(current_unsorted)
        # if the split array is the whole array, then we just do permutations
        # minus the current count
        elif n_arrays == 1:
            # substract each element, element-wise, to make the new list
            unsorted_count_array = list(map(operator.sub, total_potential_inversions, unsorted_count_array))
            # get the current unsortedness and output
            current_unsorted = sum(unsorted_count_array)
            print(current_unsorted)
        else:
            # for each of the power of two stored that are inside the smaller
            # array bloc, we reverse each of their value since this array will
            # be flipped, so they can be stored for the next computation
            for j in range(q_k):
                # update the current value in the array for future computations
                unsorted_count_array[j] = total_potential_inversions[j] - unsorted_count_array[j]
            # print the current unsortedness of this version of the array and
            # update the current count for next iteration
            current_unsorted = sum(unsorted_count_array)
            print(current_unsorted)


""" function call for testing """
gobosort()
