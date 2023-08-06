import sys
import subprocess
import lfs

def main():
    print("Running LFS wrapper")
    print(sys.argv)

    arguments = sys.argv[1:]
    path_to_git_lfs = "/".join(lfs.__file__.split("/")[:-1]) + "/git-lfs"

    subprocess.check_call([path_to_git_lfs, *arguments])
