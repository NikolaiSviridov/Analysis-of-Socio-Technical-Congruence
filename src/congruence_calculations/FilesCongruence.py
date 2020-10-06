import numpy as np
import src.utils as utils


class FilesCongruence:
    """
    Class for calculating file-congruence between users.
    Workflow:
    1. Creates boolean 2D matrix of users and encoded files. "True" value if file appeared in commit, otherwise "False"
    2. Iterate over all rows by using each row as mask on whole matrix and sum all values in row. It'll create
       columns of common files between users.
    3. Merge columns
    As the result we got 2D matrix with users ID's on both axes where each cell [i, j] represents number of common files
    between users.
    """
    def __init__(self, user_to_id=None, user_files_ids=None, file_to_id=None, load=False):
        if load:
            self.user_to_id = utils.load_json("user_to_id")
            self.user_files_ids = utils.load_json("user_files_ids")
            self.file_to_id = utils.load_json("file_to_id")
        else:
            self.user_to_id = user_to_id
            self.user_files_ids = user_files_ids
            self.file_to_id = file_to_id

        self.__init_matrix_users_files()
        self.__calculate_matrix_common()

    def __init_matrix_users_files(self):
        """
        Create boolean 2D matrix of users and encoded files.
        """
        size = (len(self.user_to_id), len(self.file_to_id))
        self.matrix_users_files = np.full(size, False, dtype=bool)
        for user_login, files_ids in self.user_files_ids.items():
            idxs = list(files_ids)
            self.matrix_users_files[self.user_to_id[user_login], idxs] = True

    def __calculate_matrix_common(self):
        """
        Create 2D matrix with users ID's on both axes where each cell [i, j] represents number of common files
        between users
        """
        columns = []
        for i in range(len(self.user_to_id)):
            columns.append((self.matrix_users_files * self.matrix_users_files[i]).sum(axis=1))

        self.matrix_common = np.column_stack(columns)


