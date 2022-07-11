# -*- coding: utf-8 -*-
#
# Copyright Université Rennes 1 / INSERM
# Contributor: Raphael Weber
#
# Under CeCILL license
# http://www.cecill.info

"""
Script for extracting the tree view of source code, it automatically handles
the gitignore file at the root directory
"""

from os.path import isfile, isdir, basename, abspath
from os import listdir, remove
from argparse import ArgumentParser
from glob import glob


def get_ignored_items(dir_root, ignore_list):
    """
    Gets list of items to ignore in the tree view

    :param dir_root: root directory for the tree view
    :type dir_root: str
    :param ignore_list: patterns/items to look for
    :type ignore_list: list

    :returns: list of items to ignore in the tree view
    :rtype: list
    """

    ignored_item_list = []
    exception_list = []
    for ignore in ignore_list:
        if ignore[0] != '!':
            ignored_item_list += glob(
                "%s/%s" % (dir_root, ignore), recursive=True
            )

        else:
            exception_list.append(ignore[1:])

    for exception in exception_list:
        exception_item_list = glob(
            "%s/%s" % (dir_root, exception), recursive=True
        )
        
        for exception_item in exception_item_list:
            if exception_item in ignored_item_list:
                ignored_item_list.remove(exception_item)

    return ignored_item_list


def write_tree_view_recursive(
    dir_root_path, output_path, dir_root_name=None, ignored_item_list=[],
    level=0
):
    """
    Recursive function for writing tree view in a TXT file

    :param dir_root_path: path to the root directory for the tree view
    :type dir_root_path: str
    :param output_path: path to output file where to write the tree view
    :type output_path: str
    :param dir_root_name: name to use as root directory inside the tree view,
        by default it is the basename of ``dir_root_path``
    :type dir_root_name: str
    :param ignored_item_list: items to ignore in the tree view
    :type ignored_item_list: list
    :param level: nesting level inside the package structure
    :type level: int
    """

    if dir_root_name is None:
        dir_root_name = basename(dir_root_path)

    if dir_root_name != '':
        dir_root_name += '/'

    listing = listdir(dir_root_path)
    listing_dir = [i for i in listing if isdir("%s/%s" % (dir_root_path, i))]
    listing_file = [i for i in listing if isfile("%s/%s" % (dir_root_path, i))]
    listing = listing_dir + listing_file

    for item in listing:
        item_path = "%s/%s" % (dir_root_path, item)
        item_path_relative = "%s%s" % (dir_root_name, item)
        if item_path not in ignored_item_list:
            if item in listing_dir:
                with open(output_path, 'a') as f:
                    f.write(' ' * 4 * level)
                    f.write("|__ %s%s\n" % (dir_root_name, item))

                write_tree_view_recursive(
                    item_path, output_path,
                    dir_root_name=item_path_relative,
                    ignored_item_list=ignored_item_list, level=level + 1
                )

            else:
                with open(output_path, 'a') as f:
                    f.write(' ' * 4 * level)
                    f.write("|__ %s\n" % item)


if __name__ == '__main__':
    #############
    # arguments #
    #############
    parser = ArgumentParser()

    parser.add_argument(
        "dir_root",
        type=str,
        help="root directory where to start the tree view"
    )

    parser.add_argument(
        "-i",
        "--ignore_list",
        nargs='+',
        type=str,
        help="list of files/directories to ignore in the tree view (similar "
        "to gitignore)",
        default=[]
    )

    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="output path where is written the tree view",
        default="tree_view.txt"
    )

    args, _ = parser.parse_known_args()
    dir_root = abspath(args.dir_root)
    ignore_list = args.ignore_list
    output_path = args.output_path

    ######################
    # script starts here #
    ######################

    # check if gitignore file in root directory
    gitignore_path = "%s/.gitignore" % dir_root
    if isfile(gitignore_path):
        # load gitignore
        with open(gitignore_path, 'r') as f:
            gitignore_list = [
                s.replace('\n', '') for s in f.readlines()
                if s != '\n' and s[0] != '#'
            ]

        # fuse with input ignore list
        ignore_list = list(set(ignore_list + gitignore_list))

        # add git folder to ignore list
        ignore_list += [".git"]

    ignored_item_list = get_ignored_items(dir_root, ignore_list)

    if isfile(output_path):
        remove(output_path)

    write_tree_view_recursive(
        dir_root, output_path, dir_root_name='',
        ignored_item_list=ignored_item_list
    )
