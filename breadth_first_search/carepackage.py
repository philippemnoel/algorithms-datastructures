"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 7 - Carepackage
Python version of Carepackage
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from collections import defaultdict, deque, Counter

""" Subroutine code for BFS path-finding algorithm """
def BFS(flights, source, sink):
    # dict to keep track of the nodes we have visited so far
    visited = defaultdict(bool)
    # initialize our queue
    queue = deque()
    queue.append(source)
    # parents dict to reconstruct the path later
    parents = dict()
    # repeat as long as there are non-considered vertices
    while(queue):
        # get the next vertex
        u = queue.popleft()
        # if u has not been visited, we visit it and perform BFS iteration
        if not visited[u]: # if true
            visited[u] = True
            # if u is the sink, then we are done with our path
            if u == sink:
                break
            # look at all the flights departing from u
            for v in flights[u]:
                # if they haven't been visited and have remaining capacity we
                # want to consider them eventually
                if not visited[v] and flights[u][v] > 0:
                    # add neighbor vertex to queue to consider them
                    queue.append(v)
                    # define their parents as the current departure city
                    parents[v] = u
    # construct the path that we will use to compute the bottleneck flow
    path = []
    # if we have not visited the sink, then there was no path
    if not visited[sink]:
        return None
    # else, we go over our list of parents and reconstruct the path as a list
    v = sink
    while v != source:
        u = parents[v]
        path.append((u,v))
        v = u
    # return our path to Ford-Fulkerson subroutine
    return path


""" Subroutine code for Ford-Fulkerson's MaxFlow Algorithm """
def Ford_Fulkerson(flights, source, sink):
    # maxflow variable to be outputted, initialized at 0
    maxflow = 0
    # get the first path with DFS
    curr_path = BFS(flights, source, sink)
    # while there is a path between source and sink
    while curr_path != None:
        # initial dummy bottleneck flow
        bottleneck_flow = float("Inf")
        # iterate over our path and find the bottleneck flow
        for u, v in curr_path:
            bottleneck_flow = min(flights[u][v], bottleneck_flow)
        # increase our maximum flow to reflect this new flow
        maxflow += bottleneck_flow
        # update our capacities and our reverse edges with our new flow
        for u, v in curr_path:
            flights[u][v] -= bottleneck_flow
            flights[v][u] += bottleneck_flow
        # run a new DFS (repeating until there is no path between s and t)
        curr_path = BFS(flights, source, sink)
    # render success
    return maxflow


""" Subroutine code for Carepackage algorithm """
def carepackage():
    # read n (cities) and m (cargo flights)
    n, m = map(int, raw_input().split())
    # temporary flights dict to process the time and build the actual graph of
    # flights we will be using
    tmp_flights = defaultdict(list)
    # actual flights graph we will be using after times have been processed
    flights = defaultdict(Counter)
    # reading the flights into a list for simplicity and coordinate compression
    # (if needed for faster runtime)
    raw_flights = []
    for flight in range(m):
        a, b, s, t, c = map(int, raw_input().split())
        raw_flights.append((a, b, s, t, c))
    # build our tmp_flight dict as a list of all the flights from each city
    for a, b, s, t, c in raw_flights:
        tmp_flights[a].append((a, b, s, t, c))
    # iterate over all of our departure cities
    for u in tmp_flights:
        # if it's not the sink, then we look for an outgoing flight
        if u != n:
            # look at all flights leaving this departure city
            for a, b, s, t, c in tmp_flights[u]:
                # add their capacity to the capacity edge in our final graph
                flights[(a, s)][(b, t)] += c
                # if the outgoing city is not the sink, then we might need to
                # add a dummy flight for the time to check out between cities
                if b != n:
                    # look at all outgoing flights from the arrival city
                    for A, B, S, T, C in tmp_flights[b]:
                        # if the time match, we add a dummy flight to connect
                        # them
                        if S >= t:
                            flights[(b, t)][(b, S)] += float("Inf")
                # if the arrival city is the sink, then we can just add a
                # dummy flight to specify that our path is complete
                else:
                    flights[(n, t)][(n, -1)] += float("Inf")
    # make the beginning dummy flights as starting points
    # tmp_flights[1] is all points starting from the source
    for a, b, s, t, c in tmp_flights[1]:
        flights[(1, -1)][(1, s)] += float("Inf")
    # source = Albany, labelled 1, sink = Cambridge, labelled n
    source, sink = (1, -1), (n, -1)
    # use Ford-Fulkerson's Maximum Flow Algorithm to get the maximum number of
    # packages that could have been sent
    max_packages = Ford_Fulkerson(flights, source, sink)
    # render success
    print(max_packages)


""" Function call for testing """
carepackage()
