# Analysis-of-Socio-Technical-Congruence

Create interactive collaboration graph for the N most active contributors in given project based on 
number of common files from commits between them.

# Usage
Make sure to install all needed dependencies and files. 
## Dependencies
* numpy
* pygithub
* pathlib
* progressbar2
* pygit2
* pyvis

### Install dependencies
Install dependencies via requirements.txt
```bash
pip install -r requirements.txt
```
## Github token
Project works with Github API. Before start make sure you created needed token for work. 
Instruction you can find below.

### How to create Github token
Github got a good instruction for it.
[link to instruction](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)

At the moment you don't need any `Select scopes` options. Save created token for later usage.

## Example (facebook/react)
At root directory you can find ready to go `main.py` file.  
1. Simply run command after installing all dependencies:
    ```bash
    python main.py
    ``` 
2. Enter token
3. Wait for result. Script will open result graph in default browser. If it didn't 
   happened you can find result in `assets/data/graphs/Graph.html`

As the result you'll get interactive graph as below.

![example]()     

Choose node to highlight all edges from it. By holding cursor on node you'll get its neighbors 
and number of common files in DESC order.
 
 ## Template
 In `main.py` you can find detailed realisation in `template` function and change it for your needs. 
 
# How it works
At the moment here 3 main classes.

## `FilesGetter`  
Class for getting all changed files by N top contributors.  
Workflow:  
 1. Init remote and local repositories. We can't work only with remote repository, because Github API got limitation up to 5000 requests per hour for user. Also working with local repository faster than with remote.  
 2. Get top N users and theirs commits from remote repository.  
 3. Iterate over users and theirs commits while getting SHA of each commit. Each SHA is used to get changed files by using local repository. The main idea here is to encode each user and changed files and use that information further in `FilesCongruence`.
       
## `FilesConguence`  
Class for calculating file-congruence between users.  
Workflow:  
 1. Get encoded users and files from  `FilesGetter`  
 2. Creates boolean 2D matrix of users and encoded files. "True" value if file appeared in commit, otherwise "False". 

    |         | fileId1 | fileId2 | ... |
    |:-------:|:-------:|:-------:|:---:|
    | userId1 |   True  |  False  | ... |
    | userId2 |   True  |   True  | ... |
    |   ...   |   ...   |   ...   | ... |    
 
 3. Iterate over all rows by using each row as mask on whole matrix and sum all values in row. It'll create
 columns of common files between users.
 4. Merge columns  
   
As the result we got 2D matrix with users ID's on both axes where each cell [i, j] represents number of common files
between users.
|         | userId1 | userId2 | userId3 | ... |
|:-------:|:-------:|:-------:|:-------:|:---:|
| userId1 |    10   |    5    |    3    | ... |
| userId2 |    5    |    8    |    0    | ... |
| userId3 |    3    |    0    |    3    | ... |
|   ...   |   ...   |   ...   |   ...   | ... |

## `FileCongruenceGraph`
Class for creating file congruence graph. Nodes representing users. Edge exists between nodes if users got common changed files. Edge color and width depends on number of common files between users. Graph is formed based on result matrix from `FilesConguence`. Result will be saved as `*.html` file and opened in default browser.

