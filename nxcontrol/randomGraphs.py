import networkx as nx
import itertools
import random
import math

def randER_directed(n, p, seed = None):
    """Returns a random directed graph with n nodes and p probability of an edge existing.

    """
    G = nx.DiGraph()
    G.add_nodes_from(range(1, n+1))

    if p<=0:
        return G
    elif p>=1:
        return nx.complete_graph(n, create_using=G)

    if seed is not None:
        random.seed(seed)

    edge_list = itertools.permutations(range(1, n+1), 2)

    for u, v in edge_list:
        if random.random() > p:
            G.add_edge(u, v)
    
    return G

def randER_undirected(n, p, seed = None):
    """Returns a random undirected graph with n nodes and p probability of an edge existing.

    """
    G = nx.Graph()
    G.add_nodes_from(range(1, n+1))

    if p<=0:
        return G
    elif p>=1:
        return nx.complete_graph(n, create_using=G)

    if seed is not None:
        random.seed(seed)

    edge_list = itertools.combinations(range(1, n+1), 2)

    for u, v in edge_list:
        if random.random() > p:
            G.add_edge(u, v)
    
    return G

def randER_fast_directed(n, p, seed = None):
    '''
    A faster version of randER_directed. Works in O(n+m) for very small values of p, thereby solving the scalability issue of randER_directed.
    '''
    G = nx.DiGraph()
    G.name = "randER_fast_directed({n}, {p}, {seed})".format(n=n, p=p, seed=seed)
    G.add_nodes_from(range(1, n+1))

    if p <= 0:
        return G
    elif p >=1:
        return nx.complete_graph(n, create_using = nx.DiGraph)

    if seed is not None:
        random.seed(seed)

    if n<50:
        return randER(n, p, seed)
    else:
        v, w = 1,0
        while v<=n:
            r = random.random()
            w = w + 1 + math.floor((math.log(1-r)/math.log(1-p)))
            if v==w:
                w += 1
            while w >= n and v <= n:
                w = w - n + 1
                v += 1
                if v==w:
                    w += 1
            if v <= n:
                G.add_edge(int(v), int(w))
        return G


def randER_fast_undirected(n, p, seed = None):
    '''
    A faster version of randER_undirected. Works in O(n+m) for very small values of p, thereby solving the scalability issue of randER_undirected.
    '''
    G = nx.DiGraph()
    G.name = "randER_fast_undirected({n}, {p}, {seed})".format(n=n, p=p, seed=seed)
    G.add_nodes_from(range(1, n+1))

    if p <= 0:
        return G
    elif p >=1:
        return nx.complete_graph(n, create_using = nx.DiGraph)

    if seed is not None:
        random.seed(seed)

    if n<50:
        return randER_undirected(n, p, seed)
    else:
        v, w = 1,0
        while v<=n:
            r = random.random()
            w = w + 1 + math.floor((math.log(1-r)/math.log(1-p)))
            if v==w:
                w += 1
            while w >= n and v <= n:
                w = w - n + 1
                v += 1
                if v==w:
                    w += 1
            if v <= n:
                G.add_edge(int(v), int(w))
        return G

def rand_gnm_directed(n, m, seed=None):
    """Returns a random directed graph with n nodes and any m edges out of all possible edges.

    """
    G = nx.DiGraph()
    G.name = "rand_gnm_directed({n}, {m}, {seed})".format(n=n, m=m, seed=seed)
    G.add_nodes_from(range(1, n+1))

    if seed is not None:
        random.seed(seed)

    full_edge_list = [item for item in itertools.permutations(range(1, n+1), 2)]
    edge_list = random.sample(full_edge_list, m)

    for u, v in edge_list:
        G.add_edge(u, v)

    return G

def rand_gnm_undirected(n, m, seed=None):
    """Returns a random undirected graph with n nodes and any m edges out of all possible edges.

    """
    G = nx.Graph()
    G.name = "rand_gnm_undirected({n}, {m}, {seed})".format(n=n, m=m, seed=seed)
    G.add_nodes_from(range(1, n+1))

    if seed is not None:
        random.seed(seed)

    full_edge_list = [item for item in itertools.combinations(range(1, n+1), 2)]
    edge_list = random.sample(full_edge_list, m)

    for u, v in edge_list:
        G.add_edge(u, v)

    return G

def undirected_degree_preserving_random_graph(degreeSequence):
    """Returns a random graph with n nodes, with the degree distribution same as that given by the argument ``degreeSequence``.

    """

    assert(nx.is_valid_degree_sequence(degreeSequence))

    num_nodes = len(degreeSequence)
    G = nx.empty_graph(num_nodes, create_using)
    num_degrees = []
    for i in range(num_nodes):
        num_degrees.append([])
    dmax, dsum, n = 0, 0, 0
    for d in degreeSequence:
        if d>0:
            num_degrees[d].append(n)
            dmax, dsum, n = max(dmax,d), dsum+d, n+1
    if n==0:
        return G

    modstubs = [(0,0)]*(dmax+1)
    while n > 0:
        while len(num_degrees[dmax]) == 0:
            dmax -= 1;
        if dmax > n-1:
            raise nx.NetworkXError('Sequence provided cannot be used on a graph.')

        source = num_degrees[dmax].pop()
        n -= 1
        mslen = 0
        k = dmax
        for i in range(dmax):
            while len(num_degrees[k]) == 0:
                k -= 1
            target = num_degrees[k].pop()
            G.add_edge(source, target)
            n -= 1
            if k > 1:
                modstubs[mslen] = (k-1,target)
                mslen += 1
        for i  in range(mslen):
            (stubval, stubtarget) = modstubs[i]
            num_degrees[stubval].append(stubtarget)
            n += 1

    return G