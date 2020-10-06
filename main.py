from src.congruence_calculations.FilesCongruence import FilesCongruence
from src.git_parse.FilesGetter import FilesGetter
from src.visualize.FileCongruenceGraph import FileCongruenceGraph
import src.utils as utils


def main():
    print("Please enter the Github token : ")
    token = str(input())

    file_getter = FilesGetter(token)
    file_getter.run(n=50, save_json=True)

    print(f"Calculating matrix")
    files_congruence = FilesCongruence(user_to_id=file_getter.user_to_id
                                       , user_files_ids=file_getter.user_files_ids
                                       , file_to_id=file_getter.file_to_id)

    print(f"Preparing graph")
    graph = FileCongruenceGraph(files_congruence)
    graph.show()


def template():
    print("Please enter the Github token : ")
    token = str(input())
    # token = ''
    local_repo_path = utils.LOCAL_REPO_DIR
    remote_repo_name = 'facebook/react'
    remote_repo_https = 'https://github.com/facebook/react.git'

    file_getter = FilesGetter(token
                              , local_repo_path=local_repo_path
                              , remote_repo_name=remote_repo_name
                              , remote_repo_https=remote_repo_https)
    n = 50
    save_json = True

    file_getter.run(n=n, save_json=save_json)

    load = False
    print(f"Calculating matrix")
    files_congruence = FilesCongruence(user_to_id=file_getter.user_to_id
                                       , user_files_ids=file_getter.user_files_ids
                                       , file_to_id=file_getter.file_to_id
                                       , load=load)

    heading = "Graph"
    print(f"Preparing graph")
    graph = FileCongruenceGraph(files_congruence, heading=heading)
    graph.show()


if __name__ == '__main__':
    main()
    # template()
