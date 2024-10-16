import networkx as nx

from glob import glob
from os.path import join
from json import load
from copy import deepcopy
from math import floor
from json import dump

from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn


class MakeGraph:
    def __init__(self, sdp_result:dict) -> None:
        self.__sdp_result = \
            [list(zip(tok, sdp)) for tok, sdp in zip(sdp_result['tok/fine'], sdp_result['sdp'])]

    def __get_subarray(self, 
                       arr, 
                       size:int, 
                       *,
                       is_soft:bool=False, 
                       proportion:float=1):
        '''
        `is_soft`: wether trailing chunk (it may not contain enough items, and thus
        cannot be returned as a subarray) is truncated according to the `proportion`
        argument.
        `proportion`: an argument which determines wether the last chunk will be 
        discarded. It must be a float < 1. If the size of the last chunk greater 
        then `proportion` * `size`, and the chunk will be retained; otherwise, 
        discarded.
        '''      
        if is_soft:
            proportion = proportion
        else:
            proportion = 1
             
        if len(arr) % size == 0:
            split_pos = [i*size for i in range(1, int(len(arr)/size)+1)]
        else:
            split_pos = [i*size for i in range(1, floor(len(arr)/size)+1)] + [len(arr)]
        
        subarrays = []
        start_pos = 0
        for end_pos in split_pos:
            subarrays.append(arr[start_pos:end_pos])
            start_pos = end_pos
         
        if len(subarrays[-1]) < proportion * size:
            subarrays.pop()
        
        return subarrays
    
    def run(self, size:int, *, is_soft:bool=True, proportion:float=1) -> list[nx.Graph]:
        text_column = TextColumn("Generating graphs from SDP...")
        bar_column = BarColumn(bar_width=20)
        progress = Progress(text_column, bar_column)
        
        subarries = self.__get_subarray(self.__sdp_result,
                                        size,
                                        is_soft=is_soft,
                                        proportion=proportion)
        
        graphs = []
        with progress:
            for sub in progress.track(subarries):
                G = nx.DiGraph()
                for node_semrel_lst in sub:
                    nodes = [node_semrel[0] for node_semrel in node_semrel_lst]
                    G.add_nodes_from(nodes)
                
                    id_node_dict = dict(enumerate(node_semrel_lst, 1))
                
                    edges = []
                    for node, sem_rels in node_semrel_lst:
                        for rel in sem_rels:
                            head_id = rel[0]
                            if head_id != 0:
                                edges.append((id_node_dict[rel[0]][0], node, {'relation': rel[1]}))
                        
                    G.add_edges_from(edges)
                
                graphs.append(G)
        
        return graphs


class GraphStats:
    def __init__(self, graphs:list[nx.Graph]) -> None:
        self.graphs = graphs

        self.graph_stats = []

    def __run_through_graphs(param_name:str):
        def inner(func):

            def wrapper(self):
                print(f'{param_name} is being computed...')

                results = []
                for graph in self.graphs:
                    results.append(func(self, graph))

                self.graph_stats.append({param_name: results})
                
                return results
            
            return wrapper
            
        return inner

    @__run_through_graphs('out_degree_centrality')
    def __out_centrality(self, g):
        return nx.out_degree_centrality(g)
    
    @__run_through_graphs('in_degree_centrality')
    def __in_centrality(self, g):
        return nx.in_degree_centrality(g)

    @__run_through_graphs('shortest_path_length')
    def __shortest_path_len(self, g):
        shortest_path_len = nx.shortest_path_length(g)
        if isinstance(shortest_path_len, int):
            return shortest_path_len
        else:
            return list(shortest_path_len)
    
    @__run_through_graphs('average_shortest_path_length')
    def __average_shortest_path_length(self, g):
        return list(nx.all_pairs_shortest_path_length(g))
    
    @__run_through_graphs('clustering_coef')
    def __clustering_coef(self, g):
        return nx.cluster.clustering(g)
    
    @__run_through_graphs('n_of_nodes')
    def __n_of_nodes(self, g):
        return g.number_of_nodes()
    
    @__run_through_graphs('n_of_edges')
    def __n_of_edges(self, g):
        return g.number_of_edges()
    
    @__run_through_graphs('in_degree')
    def __in_degree(self, g):
        return dict(g.in_degree())
    
    @__run_through_graphs('out_degree')
    def __out_degree(self, g):
        return dict(g.out_degree())
    
    def get_stats(self):
        self.__in_centrality()
        self.__out_centrality()
        self.__shortest_path_len()
        self.__average_shortest_path_length()
        self.__clustering_coef()
        # self.__n_of_nodes()
        # self.__n_of_edges()
        self.__in_degree()
        self.__out_degree()


# if __name__ == '__main__':
#     with open('data_for_exp_5\\gi_net\\0.1_捕风的异乡人.json', 'r', encoding='utf-8') as f:
#         nlp_results = load(f)
    
#     mg = MakeGraph(nlp_results)
#     g = mg.run(1)

#     gs = GraphStats(g)
#     gs.get_stats()

#     with open('1.json', 'w', encoding='utf-8') as f:
#         dump(gs.graph_stats, f, ensure_ascii=False, indent=2)
