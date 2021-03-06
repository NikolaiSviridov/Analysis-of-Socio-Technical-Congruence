from collections import defaultdict
import pygit2
from github import Github
import os
import src.utils as utils
import progressbar


class FilesGetter:
    """
    Class for getting all changed files by N top contributors.
    Workflow:
    1. Init remote and local repositories
    2. Get top N users and theirs commits from remote repository
    3. Iterate over users and theirs commits while getting SHA of each commit. Each SHA is used to get changed files
       by using local repository.
    As the result we got multiple maps:
    file_to_id - changed filename and id
    user_to_id - user login and id
    id_to_user - id and user login
    user_files_ids - user files and set of changed files ids
    """

    EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

    def __init__(self
                 , token
                 , local_repo_path=utils.LOCAL_REPO_DIR
                 , remote_repo_name='facebook/react'
                 , remote_repo_https='https://github.com/facebook/react.git'):
        self.__init_local_repo(local_repo_path, remote_repo_https)
        self.__init_remote_repo(token, remote_repo_name)
        self.file_to_id = dict()
        self.user_to_id = dict()
        self.id_to_user = dict()
        self.user_files_ids = defaultdict(set)

    def __init_local_repo(self, local_repo_path, remote_repo_https):
        """
        Init local repository by using pygit2 lib. If a folder empty it'll clone repository to it, otherwise
        continue with existing folder as repository. If a folder doesn't exists raise exception.

        :param local_repo_path: path of local repository
        :param remote_repo_https: https of remote repository
        """
        if os.path.exists(local_repo_path) and os.path.isdir(local_repo_path):
            if not os.listdir(local_repo_path):
                print(f"Cloning {remote_repo_https} into {local_repo_path}")
                self.local_repo = pygit2.clone_repository(remote_repo_https, local_repo_path)
                print(f"Finished cloning")
            else:
                print(f"Dir {local_repo_path} is not empty. Using as repo.")
                self.local_repo = pygit2.Repository(local_repo_path)
        else:
            raise OSError(f"{os.path.abspath(local_repo_path)} doesn't exist or not a directory")

    def __init_remote_repo(self, token, remote_repo_name):
        """
        Init remote repository by using PyGithub lib.

        :param token: Github token for working with API
        :param remote_repo_name: remote repository name must be in 'facebook/react' format
        """
        self.token = token
        g = Github(token)
        self.remote_repo = g.get_repo(remote_repo_name)

    def __get_first_n_top_contributors(self, n=50):
        return self.remote_repo.get_stats_contributors()[-n:]

    def run(self, n=50, save_json=False):
        """
        Get all changed files by N top contributors.
        Results stored in:
        file_to_id
        user_to_id
        id_to_user
        user_files_ids

        :param n: number of top contributors
        :param save_json: boolean flag if you need to save results in json format
        """
        file_id = 0
        user_id = 0

        contributors = self.__get_first_n_top_contributors(n)

        print(f"Getting files from users commits")
        bar = progressbar.ProgressBar(max_value=len(contributors))
        for contributor in contributors:
            user_login = contributor.author.login
            self.user_to_id[user_login] = user_id
            self.id_to_user[user_id] = user_login

            commits = self.remote_repo.get_commits(author=contributor.author)
            for commit in commits:
                try:
                    local_commit = self.local_repo.revparse_single(commit.sha)
                except KeyError:
                    # Local and remote repos differ. Need to update local repo.
                    continue

                if not local_commit.parents:
                    diffs = self.local_repo.diff(FilesGetter.EMPTY_TREE_SHA, local_commit)
                else:
                    diffs = self.local_repo.diff(local_commit.parents[0], local_commit)

                for diff in diffs:
                    file_name = diff.delta.old_file.path
                    if file_name not in self.file_to_id:
                        self.file_to_id[file_name] = file_id
                        file_id += 1
                    self.user_files_ids[user_login].add(self.file_to_id[file_name])
            user_id += 1
            bar.update(user_id)

        if save_json:
            self._save_to_json()

        # New line after progressbar
        print()

    def _save_to_json(self):
        dict_of_lists = defaultdict(list, ((k, list(v)) for k, v in self.user_files_ids.items()))
        utils.save_to_json(dict_of_lists, "user_files_ids")
        utils.save_to_json(self.file_to_id, "file_to_id")
        utils.save_to_json(self.user_to_id, "user_to_id")
        utils.save_to_json(self.id_to_user, "id_to_user")


if __name__ == '__main__':
    token = str(input())
    file_getter = FilesGetter(token)
    file_getter.run(n=50, save_json=True)
