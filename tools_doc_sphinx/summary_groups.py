# -*- coding: utf-8 -*-
#
# Copyright Universit√© Rennes 1 / INSERM
# Contributor: Raphael Weber
#
# Under CeCILL license
# http://www.cecill.info

"""
Module for the creation of groups of methods in the API documentation of
classes, based on
https://autodocsumm.readthedocs.io/en/latest/examples.html?highlight=example_grouper#including-a-table-of-contents
"""

import numpy as np
from linecache import getline
from importlib import import_module


# global variable
try:
    from pkg_name import PACKAGE_NAME

except Exception:
    #: (*str*) Name of the package to document with methods groups, imported
    #: from a file named **pkg.py**
    PACKAGE_NAME = ''


def group_parser(module_path):
    """
    Gets the set of methods defined in a module along with their respective
    group

    :param module_path: path to the source code file of the module
    :type module_path: str

    :returns: structured as follows:

        - Key is class name, value is a dictionary structured as follows:

            - Key is group name, value is the list of methods contained in the
              group
    :rtype: dict
    """

    # define role identifiers
    start_group_exp = "    # Group: "
    end_group_exp = "    # End group"
    deco_group = "    # *********"
    meth_exp = "    def "
    class_exp = "class "

    l_exp = max(len(start_group_exp), len(end_group_exp), len(deco_group),
                len(meth_exp), len(class_exp))

    # load file content
    with open(module_path, 'r') as f:
        trunc_array = np.array([line[:l_exp] for line in f.readlines()])

    # get index of lines with class definition
    class_inds = np.where(
        np.array(
            [trunc[:len(class_exp)] for trunc in trunc_array]
        ) == class_exp
    )[0]

    # get list of classes name
    class_name_list = []
    for ind in class_inds:
        class_name = getline(
            module_path, ind + 1
        )[len(class_exp):].split('(')[0]
        class_name_list.append(class_name)

    # get index of lines where the groups start and end
    group_start_inds_tmp = np.where(
        np.array(
            [trunc[:len(start_group_exp)] for trunc in trunc_array]
        ) == start_group_exp
    )[0]

    group_end_inds_tmp = np.where(trunc_array == end_group_exp)[0]

    # initialize list of range of line indexes of groups
    group_inds_list = []

    # initialize list of groups name
    group_name_list = []

    # initialize dictionary with the methods included in each group
    group_dict = {name: {} for name in class_name_list}

    # initialize counters
    i, j = 0, 0

    # loop on groups indexes
    while i < group_start_inds_tmp.shape[0] and j < group_end_inds_tmp.shape[0]:
        # get group start and end indexes
        start_ind = group_start_inds_tmp[i]
        end_ind = group_end_inds_tmp[j]

        # check if group start index is legit
        start_ok = trunc_array[start_ind - 1] == deco_group and \
            trunc_array[start_ind + 1] == deco_group

        # check if group end index is legit
        end_ok = trunc_array[end_ind - 1] == deco_group and \
            trunc_array[end_ind + 1] == deco_group

        # check if group is legit
        if start_ok and end_ok:
            # increment counters
            i += 1
            j += 1

            # get class containing the group
            class_ind = np.where(class_inds < start_ind)[0][-1]
            class_name = class_name_list[class_ind]

            # update group lists and dictionary
            group_inds_list.append((start_ind, end_ind))
            group_name = getline(
                module_path, start_ind + 1
            )[len(start_group_exp):-1]
            group_name_list.append(group_name)
            group_dict[class_name][group_name] = []

        else:
            # update counters
            if not start_ok:
                i += 1

            if not end_ok:
                j += 1

    # get line indexes of the methods
    meth_inds = np.where(
        np.array(
            [trunc[:len(meth_exp)] for trunc in trunc_array]
        ) == meth_exp
    )[0]

    # loop on methods
    for ind in meth_inds:
        # get class containing the method
        class_ind = np.where(class_inds < ind)[0][-1]
        class_name = class_name_list[class_ind]

        # get group containing the method and update group dictionary
        for group_inds, group_name in zip(group_inds_list, group_name_list):
            if ind >= group_inds[0] and ind <= group_inds[1]:
                method_name = getline(
                    module_path, ind + 1
                )[len(meth_exp):].split('(')[0]
                group_dict[class_name][group_name].append(method_name)

    return group_dict


def launch_group_parser(package_name):
    """
    Recursive function for launching :func:`.group_parser` inside a package

    :param package_name: name of the package
    :type package_name: str

    :returns: see output of :func:`.group_parser`
    """

    # import package
    package = import_module(package_name)

    # initialize output
    group_dict = {}

    # check if package indeed
    if hasattr(package, "__all__"):
        # loop on modules and sub-packages
        for member_name in package.__all__:
            # recursive call
            group_dict.update(
                launch_group_parser("%s.%s" % (package_name, member_name))
            )

    # module imported
    else:
        # parse module and update global variable
        group_dict.update(group_parser(package.__file__))

    return group_dict


def example_grouper(app, what, name, obj, section, parent):
    """
    See
    https://autodocsumm.readthedocs.io/en/latest/examples.html?highlight=example_grouper#including-a-table-of-contents
    """

    group_dict = launch_group_parser(PACKAGE_NAME)
    for class_name, group_dict_sub in group_dict.items():
        for group_name, meth_list in group_dict_sub.items():
            if name in meth_list and class_name == parent.__name__:
                return group_name


def setup(app):
    """
    See
    https://autodocsumm.readthedocs.io/en/latest/examples.html?highlight=example_grouper#including-a-table-of-contents
    """
    
    app.connect('autodocsumm-grouper', example_grouper)
