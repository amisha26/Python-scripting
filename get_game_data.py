# ======= Lib imports =========
import os
import json
import shutil 
from subprocess import PIPE, run
import sys 


GAME_DIR_PATTERN = "game"


def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)



# Fetches name from the path
def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names


# Creates directory at a given path
def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)


# Copy source to destination and if directory exists overwrite it
def copy_and_overwrite(source, destination):
    if os.path.exists(destination):
        # recursive copy
        shutil.rmtree(destination)
    shutil.copytree(source, destination)



# Find all the game path in the data directory
def find_all_game_paths(source):
    game_paths = []
    for root, dirs, files in os.walk(source):

        # Give names of all directories and not their paths
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break
    return game_paths


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    print(new_game_dirs)
    create_directory(target_path)

    # zip matches elements in the two arrays and combine them into a tuple
    # [1, 2, 3]
    # ["a", "b", "c"]
    # output: (1, "a") (2, "b") (3, "c")
    for src, dest in  zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
    
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)


if __name__ == '__main__':
    args = sys.argv
    if (len(args) != 3):
        raise Exception("You must pass a source and target directory only")
    source, target = args[1:]
    main(source, target)