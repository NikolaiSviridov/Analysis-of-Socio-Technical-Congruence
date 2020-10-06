from src.congruence_calculations.FilesCongruence import FilesCongruence
from src.git_parse.FilesGetter import FilesGetter
from src.visualize.Graph import FileGraph


def main():
    token = str(input())
    file_getter = FilesGetter(token)
    file_getter.run(n=50, save_json=True)
    print(f"Calculating matrix")
    files_congruence = FilesCongruence(user_to_id=file_getter.user_to_id
                                       , user_files_ids=file_getter.user_files_ids
                                       , file_to_id=file_getter.file_to_id)
    print(f"Preparing graph")
    graph = FileGraph(files_congruence)
    graph.show()


if __name__ == '__main__':
    main()

