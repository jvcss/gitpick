
# baixo o repositorio

# listar as branches remotas

# listar arquivos para ignorar

# listar nome de arquivos contendo diferencas a..b

# listar as diferencas entre a..b por arquivo e salvar em patch

# salvo no banco o path de cada arquivo com nome sendo seu hash, identificando o par a..b correspondente

# table patcher
#
# |  file_name_hash |   repo_url |   par_a_b  |     patch    |   apply_at   |  compare_at  |
# | --------------- | -----------| ---------- | ------------ | ------------ | ------------ |
# |     '23bbd'     | 'https://' |'main_cead' | 'diff --git' | 13:02 28/23  | 12:01 28/23  |

# permito apagar alguma linha de patch criada

class GitManager:
    """
        Permite criar um banco de patches para aplicar em branches
    """
    files: list

    def __init__(self, a: str, b: str, ignore: list):
        self.a = a
        self.b = b
        self.ignore = ignore

    def get_repo(self):
        print('git clone https://github.com/user/repo.git')

    def get_branches(self):
        print('git branch -r')

    def get_file_diffs(self):
        print('git diff origin/a..origin/b -- this/file.txt')

    def get_files_diff(self):
        print("git diff origin/a..origin/b --name-only")

    def apply_patch(self):
        print("git checkout a")
        print("git apply the/filehashname.patch")

    def save_patch(self):
        print('''INSERT INTO 
                        patcher(file_name_hash,par_a_b,patch,apply_at,compare_at) 
                    VALUES ('23bbd', 'main_cead', 'diff --git', 13:02 28/23, 12:01 28/23);
              ''')

    def delete_patch(self):
        print("DELETE FROM patcher WHERE file_name_hash = '23bbd';")

    def update_patch(self):
        print('UPDATE patcher SET file_name_hash = "a8s56", patch = "diff --git..";')
