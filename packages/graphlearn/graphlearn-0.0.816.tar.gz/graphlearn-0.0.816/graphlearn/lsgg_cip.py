import eden.graph as eg
from networkx.algorithms import isomorphism as iso
import networkx as nx
import logging

# nx 2.2 has this:
from networkx.algorithms.shortest_paths.unweighted import _single_shortest_path_length as short_paths
logger = logging.getLogger(__name__)


def _add_hlabel(graph):
    eg._label_preprocessing(graph)


def _edge_to_vertex(graph):
    return eg._edge_to_vertex_transform(graph)


class CoreInterfacePair:
    """
    this is referred to throughout the code as cip
    it contains the cip-graph and several pieces of information about it.
    """

    def __init__(self,
                 interface_hash=0,
                 core_hash=0,
                 graph=None,
                 radius=0,
                 thickness=0,
                 core_nodes_count=0,
                 count=0,
                 root=None,
                 core_nodes=[],
                 interface_nodes=[],
                 interface_graph=None):
        self.interface_hash = interface_hash
        self.core_hash = core_hash
        self.graph = graph
        self.radius = radius
        self.thickness = thickness
        self.core_nodes_count = core_nodes_count
        # count is used to count how often we see this during grammar creation
        self.count = count
        self.root = root
        self.interface_nodes = interface_nodes
        self.core_nodes = core_nodes
        # reference to the graph thing
        self.interface_graph = interface_graph



    def __str__(self):
        return 'cip: int:%d, cor:%d, rad:%d, thi:%d, rot:%d' % \
               (self.interface_hash, self.core_hash, self.radius, self.thickness, self.root)


################
#  decompose
###############

def graph_hash(graph, node_name_label=lambda id, node: node['hlabel']):
    """
        so we calculate a hash of a graph
    """
    node_names = {n: calc_node_name(graph, n,  node_name_label) for n in graph.nodes()}
    #tmp_fast_hash = lambda a, b: fast_hash([(a ^ b) + (a + b), min(a, b), max(a, b)])
    tmp_hash = lambda a, b: hash((min(a,b), max(a,b)))
    l = [tmp_hash(node_names[a], node_names[b]) for (a, b) in graph.edges()] # was tmp fast hash before
    l.sort()
    # isolates are isolated nodes
    isolates = [n for (n, d) in graph.degree if d == 0]
    z = [node_name_label(node_id, graph.node[node_id]) for node_id in isolates]
    z.sort()
    return hash(tuple(l + z))


def calc_node_name(interfacegraph, node, node_name_label=lambda id, node: node['hlabel']):
    '''
     part of generating the hash for a graph is calculating the hash of a node in the graph
     # the case that n has no neighbors is currently untested...
    '''
    d = nx.single_source_shortest_path_length(interfacegraph, node, 20)
    l = [node_name_label(nid, interfacegraph.node[nid]) + dis for nid, dis in d.items()]
    l.sort()
    return hash(tuple(l))


def graph_hash_core(graph, node_name_label=lambda id, node: node['hlabel']):
    return graph_hash(graph,  node_name_label)


def extract_core_and_interface(root_node=None,
                               graph=None,
                               radius=None,
                               thickness=None):
    '''

    Parameters
    ----------
    root_node
    graph
    radius
    thickness
    hash_bitmask

    Returns
    -------
        makes a cip oO
    '''
    # preprocessing
    graph = _edge_to_vertex(graph)
    _add_hlabel(graph)
    # this was used before, but it assumes that root_node is a single node...
    #dist = nx.single_source_shortest_path_length(graph, root_node, radius + thickness)
    dist = {a:b for (a,b) in short_paths(graph,
                                         root_node if isinstance(root_node,list) else [root_node],
                                         thickness+radius)}

    # find interesting nodes:
    core_nodes = [id for id, dst in dist.items() if dst <= radius]
    interface_nodes = [id for id, dst in dist.items()
                       if radius < dst <= radius + thickness]
    return _finalize_cip(root_node,graph,radius,thickness,dist,core_nodes,interface_nodes)

def _finalize_cip(root_node,graph,radius,thickness,dist,core_nodes,interface_nodes):
    # this is relevant when  1. edges are root  OR 2. interface sizes are non standard
    # the problem-case is this: an interface-edge-node is connected to cores, so using it for interface
    # isomorphismchecks is nonse.
    test = lambda idd: 2==sum([ neigh in core_nodes for neigh in graph.neighbors(idd) ])
    mv_to_core = {idd:0 for idd in interface_nodes if "edge" in graph.node[idd] and test(idd)}
    if mv_to_core:
        core_nodes+= list(mv_to_core.keys())
        interface_nodes = [i for i in interface_nodes if i not in mv_to_core ]


    # calculate hashes
    core_hash = graph_hash_core(graph.subgraph(core_nodes))
    node_name_label = lambda id, node: node['hlabel'] + dist[id] - radius
    interface_hash = graph_hash(graph.subgraph(interface_nodes),
                                node_name_label=node_name_label)

    # copy cip and mark core/interface
    cip_graph = graph.subgraph(core_nodes + interface_nodes).copy()
    ddl = 'distance_dependent_label'
    for no in interface_nodes:
        cip_graph.node[no][ddl] = cip_graph.node[no]['hlabel'] + dist[no] - (radius + 1)

    interface_graph = nx.subgraph(cip_graph, interface_nodes)

    return CoreInterfacePair(interface_hash,
                             core_hash,
                             cip_graph,
                             radius,
                             thickness,
                             len(core_nodes),
                             root=root_node,
                             core_nodes=core_nodes,
                             interface_nodes=interface_nodes,
                             interface_graph=interface_graph)


######
# compose
######


def merge(graph, node_orig_interface, node_cip_interface):
    '''
    so i merge the nodes in the interface,  keeping the node in the cip
    '''
    for n in graph.neighbors(node_orig_interface):
        graph.add_edge(node_cip_interface, n)
    if isinstance(graph, nx.DiGraph):
        for n in graph.predecessors(node_orig_interface):
            graph.add_edge(n, node_cip_interface)
    graph.remove_node(node_orig_interface)


def find_all_isomorphisms(home, other):
    if iso.faster_could_be_isomorphic(home, other):
        ddl = 'distance_dependent_label'
        label_matcher = lambda x, y: x[ddl] == y[ddl] and \
                                     x.get('shard', 1) == y.get('shard', 1)

        graph_label_matcher = iso.GraphMatcher(home, other, node_match=label_matcher)
        for index, mapping in enumerate(graph_label_matcher.isomorphisms_iter()):
            if index == 5:
                logger.debug('lsgg_compose_util i checked more than 5 isomorphisms')
            yield mapping
    else:
        logger.log(5, 'lsgg_compose_util faster iso check failed')
        yield {} # iso.graphmatcher returns empty dict when nothing is found. i do the same :) 


def core_substitution(graph, orig_cip, new_cip):
    """
    graph is the whole graph..
    subgraph is the interface region in that we will transplant
    new_cip_graph which is the interface and the new core
    """

    # preprocess
    graph = _edge_to_vertex(graph)
    assert (
    set(orig_cip.graph.nodes()) - set(graph.nodes()) == set([])), 'lsgg_compose_util orig_cip_graph not in graph'

    # get isomorphism
    iso = next(find_all_isomorphisms(orig_cip.interface_graph, new_cip.interface_graph))
    #iso = next(find_all_isomorphisms(orig_cip.interface_graph, new_cip.interface_graph)) 
    if len(iso) != len(orig_cip.interface_graph):
        logger.log(5, "lsgg_compose_util grammar hash collision, discovered in 'core_substution' ")
        return None

    # make graph union (the old graph and the new cip are now floating side by side)
    graph = nx.union(graph, new_cip.graph, rename=('', '-'))

    graph.remove_nodes_from(map(str, orig_cip.core_nodes))

    # merge interface nodes
    for k, v in iso.items():
        merge(graph, str(k), '-' + str(v))
    
    graph = eg._revert_edge_to_vertex_transform(graph)
    re = nx.convert_node_labels_to_integers(graph)
    return re
