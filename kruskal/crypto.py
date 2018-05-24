"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 3 - Crypto
Python version of Crypto
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from collections import defaultdict, deque
# global dictionnaries to contain all of our sets
# parent is like the parents set, in some sense
# it contains the parent of each node and that's it
parent = dict()
rank = dict()
# this array will contain the bandwiths for each query from 1 to t
bandwiths = []
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" Subroutine code for merge subroutine of MergeSort algorithm """
def merge(lst1, lst2):
    # save lengths of lists for runtime
    lst1_len = len(lst1)
    lst2_len = len(lst2)
    # initialize output list and iteration indices
    oupt_lst = []
    index1, index2 = 0, 0
    # merging loop for non-empty lists
    while index1 != lst1_len and index2 != lst2_len:
        if lst1[index1] > lst2[index2]:
            oupt_lst.append(lst1[index1])
            index1 += 1
        else:
            oupt_lst.append(lst2[index2])
            index2 += 1
    # subcase if one list is now empty
    if index1 == lst1_len:
        oupt_lst += lst2[index2:]
    else:
        oupt_lst += lst1[index1:]
    return oupt_lst
""" Subroutine code for MergeSort algorithm """
def MergeSort(lst):
    # save length of list for runtime
    lst_len = len(lst)
    # base case
    if lst_len == 0 or lst_len == 1:
        return lst
    else:
        # recursive call
        mid = int(lst_len / 2)
        first_half = MergeSort(lst[:mid])
        second_half = MergeSort(lst[mid:])
        return merge(first_half, second_half)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" Subroutine code for Kruskal's makeset """
def makeset(vertex):
    # add our new vertex as a singleton value inside our set
    # and set its rank to 0
    parent[vertex] = vertex
    rank[vertex] = 0
""" Subroutine code for Kruskal's set find """
def find(vertex):
    # if our vertex is not the parent, recurse down the subtree
    if parent[vertex] != vertex:
        parent[vertex] = find(parent[vertex])
    # return p(x)
    return parent[vertex]
""" Subroutine code for Kruskal's set union """
def union(vertex1, vertex2, servers, users):
    # vertex1 and vertex2 are required to be roots
    root1 = find(vertex1)
    root2 = find(vertex2)
    # if rank of root1 > rank of root 2, we swap the two roots
    # since root2 has higher rank, so we should attach the smallest
    # tree to it
    if rank[root1] > rank[root2]:
        # switch the roots
        tmp = root2
        root2 = root1
        root1 = tmp
        # switch the users count
        tmp1 = users[root2]
        users[root2] = users[root1]
        users[root1] = tmp1
        # switch the servers count
        tmp2 = servers[root2]
        servers[root2] = servers[root1]
        servers[root1] = tmp2
    # if the rank are the same, make them as one root and increment rank
    if rank[root1] == rank[root2]:
        rank[root2] += 1
    # update the tree
    parent[root1] = root2
    # update users
    users[root2] += users[root1]
    # update servers
    servers[root2] += servers[root1]
    # return the root of the new connected component
    return root2
""" Subroutine code for Kruskal's algorithm """
def Kruskal(graph, weights, servers, users):
    # making all the sets is done when reading input
    # each weight in the weights list represent one edge
    # they are already sorted in decreasing order
    for w in weights:
        # get the current edge we are looking at
        edge = graph[w].popleft()
        # if not single node, add edge to our tree and merge the sets
        if find(edge[0]) != find(edge[1]):
            # pass along servers and users as when we will merge elements,
            # we check if they can provide an allocation and if so allocate
            # pass in weight since it will be the bandwith
            connected_comp_root = union(edge[0], edge[1], servers, users)
            # get number of servers and users in this new connected comp
            num_servers = servers[connected_comp_root]
            num_users = users[connected_comp_root]
            # iterate over all the users in the component
            for user in range(num_users):
                # if there is still space in servers
                if num_servers > 0:
                    # append a new bottleneck bandwith
                    bandwiths.append(w)
                    # decrease capacity available by 1
                    num_servers -= 1
                    # remove the user just assigned
                    users[connected_comp_root] -= 1
            # once done looping over the users, set the number of servers
            # in the component to the remaining number of servers for when
            # we will merge the components
            servers[connected_comp_root] = num_servers
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" Subroutine code for Crypto algorithm """
def crypto():
    # global var for more easily keeping track of bandwith cuz lazy
    global bandwiths
    # read n (vertices) and m (edges)
    n, m = map(int, input().split())
    # weights list -- will contain duplicate, should be ok
    weights = []
    # initialize the graph as an adjacency list, though about making adjacency
    # matrix, but it will be very inefficient since most of it would be empty
    # weights as keys and edges list as value
    graph = defaultdict(deque)
    # get all the edges and their weights
    for edge in range(m):
        # get the edge and its weight
        u, v, w = map(int, input().split())
        # add weight to our weight array that will be sorted
        weights.append(w)
        # fill in the vertices V_sets
        # this is the MAKESET operation from Kruskal
        # we do it here to save a linear loop later
        makeset(u)
        makeset(v)
        # add edge and its weight to our graph
        graph[w].append((u, v))
    # get k (servers) and t (users)
    k, t = map(int, input().split()) # these are kinda useless since Python
    # get the arrays that contain the servers locations, their capacities,
    # and the users locations
    servs_locations = list(map(int, input().split()))
    servs_capacities = list(map(int, input().split()))
    users_locations = list(map(int, input().split()))
    # generate a dictionary that contains the number of spots available in
    # each connected component (key is the root of the component)
    servers = dict()
    for index in range(k):
        servers[servs_locations[index]] = servs_capacities[index]
    # generate a dictionary that contains the number of users in each
    # connected component (key is the root of the component)
    users = dict()
    for index in range(t):
        users[users_locations[index]] = 1
    # fill the rest of both dictionnaries with 0 values since no user nor serv
    for index in range(n):
        if servers.get(index + 1) == None:
            servers[index + 1] = 0
        if users.get(index + 1) == None:
            users[index + 1] = 0
    # get Q (number of queries) and the Q queries
    Q = int(input()) # useless value since we're using Python
    queries = list(map(int, input().split()))
    # sort the weights in decreasing order (we are building a Max Span Tree)
    # this is an inverted MergeSort algorithm
    sorted_weights = MergeSort(weights)
    # Modified Kruskal algorithm that builds a maximum spanning tree while
    # assigning users to servers and storing it in the bandwiths array
    Kruskal(graph, sorted_weights, servers, users)
    # iterate over all the queries and take the bandwith computed
    # previously and return it. We take - 1 since array is indexed 0
    for query in queries:
        print(bandwiths[query - 1])

""" Function call for testing """
crypto()
