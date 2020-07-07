import os
from shutil import copyfile, rmtree
from os.path import isfile, join

def clear_dir(folder):
    rmtree(folder)

def make_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def get_dirname(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

def make_dirname(*dirnames):
    dirnames = list(dirnames)
    complete_dir = dirnames.pop(0)
    for dirname in dirnames:
        complete_dir = os.path.join(complete_dir, dirname)

    return complete_dir
