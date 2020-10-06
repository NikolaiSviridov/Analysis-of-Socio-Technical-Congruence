from pyvis.network import Network
from src.congruence_calculations.FilesCongruence import FilesCongruence
import numpy as np
import src.utils as utils


class FileGraph:
    def __init__(self, files_congruence, heading="Graph"):
        self.user_to_id = files_congruence.user_to_id
        self.id_to_user = {v: k for k, v in self.user_to_id.items()}
        self.matrix_cross = files_congruence.matrix_cross

        self.__init_net(heading)

    def __gen_quantiles(self, cross_matrix):
        self.matrix_cross = cross_matrix
        non_null_values = cross_matrix[cross_matrix != 0]
        self.quantiles = [
            np.quantile(non_null_values, 0.25)
            , np.quantile(non_null_values, 0.5)
            , np.quantile(non_null_values, 0.75)
        ]

    def __init_net(self, heading):
        self.net = Network(heading=heading
                           , height="1080px"
                           , width="100%"
                           , bgcolor="#222222"
                           , font_color="white")

        self.__gen_quantiles(self.matrix_cross)

        self.net.barnes_hut()

        size = self.matrix_cross.shape[0]
        for i in range(size):
            for j in range(size):
                if i == j:
                    continue

                weight = int(self.matrix_cross[i, j])
                if weight == 0:
                    continue
                src = self.id_to_user[i]
                dst = self.id_to_user[j]

                self.net.add_node(src, src, title=src)
                self.net.add_node(dst, dst, title=dst)
                self.net.add_edge(src, dst, value=weight, color=self.edge_color(weight, *self.quantiles))

        neighbor_map = self.net.get_adj_list()

        for node in self.net.nodes:
            node["title"] += " Neighbors:<br>" + "<br>".join(self.__pretty_string_neighbors(node, neighbor_map))
            node["value"] = len(neighbor_map[node["id"]])

    def __get_num_of_files_with_neighbor(self, user, neighbor):
        num_of_files = self.matrix_cross[self.user_to_id[user], self.user_to_id[neighbor]]
        return neighbor, num_of_files

    def __pretty_string_neighbors(self, node, neighbor_map):
        result = map(lambda neighbor: self.__get_num_of_files_with_neighbor(node["title"], neighbor)
                     , neighbor_map[node["id"]])
        result = sorted(result, key=lambda x: x[1], reverse=True)
        result = map(lambda x: f"{x[0]} : {x[1]}", result)
        return result

    def show(self):
        self.net.show(f"{utils.GRAPHS_DIR}/{self.net.heading}.html")

    @staticmethod
    def edge_color(weight, quantile1, quantile2, quantile3):
        if weight <= quantile1:
            return '#0569E1'
        if weight <= quantile2:
            return '#C1F823'
        if weight <= quantile3:
            return '#FCAA05'
        return '#EE5503'


if __name__ == '__main__':
    files_congruence = FilesCongruence(load=True)
    graph = FileGraph(files_congruence)
    graph.show()
