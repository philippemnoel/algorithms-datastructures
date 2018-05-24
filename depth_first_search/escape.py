"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 2 - Escape
Python version of Escape
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# global visited set to keep track over all DFS for a single test case
visited = set()

""" Subroutine code for the iterative implementation of DFS """
def iterative_DFS(graph, vertex):
    global visited
    # initialize the stack and the set of visited vertices
    stack = []
    stack.append(vertex)
    # will count the number of visited nodes in this DFS
    visited_len = 0
    # as long as the stack is not empty, keep searching
    while stack != []:
        vertex = stack.pop()
        # if this vertex has not been visited, add it to visited and visit
        # its neighbors
        if vertex not in visited:
            visited.add(vertex)
            visited_len += 1
            # add the new edges to the stack
            for edge in graph[vertex[0]][vertex[1]]:
                stack.append(edge)
    # return number of visited nods in this DFS
    return visited_len


""" Subroutine code for easily breaking out of nested loop running DFS """
def DFS_call(graph, n):
    global visited
    # reinitialize the visited set for the new test case
    visited = set()
    total_visited = 0
    # run DFS on all the diagonal states, checking that they reached al
    for i in range(n):
        total_visited += iterative_DFS(graph, (i,i))
    if total_visited == n ** 2:
        return "YES"
    else:
        return "NO"


""" Subroutine code for the Escape algorithm """
def escape():
    # read number of cases T
    T = int(raw_input())
    # initialize the arrays that will store each value of each test case
    n_list = []
    keys_list = [[] for x in range(T)]
    # deal with test cases one at a time
    for test_case in range(T):
        # get number of states and keys
        n, k = map(int, raw_input().split())
        # add to test lists
        n_list.append(n)
        # fill in the keys_list with all the key edges linking the states
        for key in range(k):
            # get the key
            curr_key = list(map(int, raw_input().split()))
            # add key to list of keys for the test case
            keys_list[test_case].append(curr_key)

    # deal with test cases one at a time
    for case in range(T):
        # get values for this current test
        n = n_list[case]
        keys = keys_list[case]
        # initialize graph as matrix of lists of nxn pair of states
        # each index (i,j) represents a state pair
        # each pair of states contains a list that will contain all the edges
        # it maps to
        graph = [[[] for x in range(n)] for y in range(n)]
        # fill in the graph with all the key edges linking the states
        # deal key by key for this test case
        for key in keys:
            # initialize the set that will contain the mappings
            mapping = []
            # fill in the graph
            for i in range(n):
                for j in range(n):
                    # reverse mapping for inverse DFS
                    # saves a linear time loop
                    if i == 0:
                        mapping.append((key[j] - 1, j))
                    # initialize two vertices used to insert
                    v1 = mapping[i]
                    v2 = mapping[j]
                    graph[v1[0]][v2[0]].append((v1[1], v2[1]))
        # call DFS testing function and DFS function and return output
        print(DFS_call(graph, n))


""" Function call for testing """
escape()
