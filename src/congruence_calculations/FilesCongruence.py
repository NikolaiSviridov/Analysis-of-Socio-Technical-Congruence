import numpy as np
import src.utils as utils


class FilesCongruence:
    def __init__(self, user_to_id=None, user_files_ids=None, file_to_id=None, load=False):

        if load:
            self.user_to_id = utils.load_json("user_to_id")
            self.user_files_ids = utils.load_json("user_files_ids")
            self.file_to_id = utils.load_json("file_to_id")
        else:
            self.user_to_id = user_to_id
            self.user_files_ids = user_files_ids
            self.file_to_id = file_to_id

        self.__init_matrix()
        self.__calculate()

    def __init_matrix(self):
        size = (len(self.user_to_id), len(self.file_to_id))
        self.matrix = np.full(size, False, dtype=bool)
        for user_login, files_ids in self.user_files_ids.items():
            idxs = list(files_ids)
            self.matrix[self.user_to_id[user_login], idxs] = True

    def __calculate(self):
        columns = []
        for i in range(len(self.user_to_id)):
            columns.append((self.matrix * self.matrix[i]).sum(axis=1))

        self.matrix_cross = np.column_stack(columns)


