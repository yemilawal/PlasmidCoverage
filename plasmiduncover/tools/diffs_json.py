#!/usr/bin/env python3

"""
Last update: 29/12/2017
Author: T.F. Jesus
This script takes json files and compares them using output jsons from mashix.
Please note that it only compares two json files
"""

import argparse
import os
import json


def load_jsons(jsonfiles):
    '''
    Loads two json files to a list using json.load()
    Parameters
    ----------
    jsonfiles: list
        A list of json files

    Returns
    -------
    list_of_json: list
        A list of two dictionaries, one for each file loaded

    '''
    list_of_json = []
    for json_f in jsonfiles:
        with open(json_f, "r") as data_file:
            data = json.load(data_file)
        list_of_json.append(data)
    return list_of_json


def range_conversion(x, c, d):
    '''
    Function to convert an initial range of [-1,1] to any custom range desired
    Parameters
    ----------
    x: float
        The value to convert
    c: float
        new range min value
    d: float
        new range max value
    Returns
    -------
    y: float
        the converted x value to the new range

    '''
    a = -1
    b = 1
    y = (x - a) * float(d - c) / (b - a) + c
    y = round(y, 2)

    return y


## function that calculates the differences between the two json files provided as input
def diff_jsons(list_of_json):
    '''
    Function that creates a dictionary with the differences between the
    dictionaries of both files. This functions allows to check the
    presence/absence of accession numbers in both files and if a given
    accession is present in both json files it will retrieve the difference
    between them. This allows to know if a given accession is more likely to
    be in one read set or another (very roughly).
    Parameters
    ----------
    list_of_json: list
        A list of two dictionaries, one for each input file

    Returns
    -------
    temp_dict: dict
        This returns a dictionary with the differences between both
        dictionaries that were taken as inputs for this function with the
        list_of_json variable.

    '''
    temp_list_k = []
    temp_dict = {}
    for xcounter, json_dict in enumerate(list_of_json):
        for k, v in json_dict.items():
            # print x
            if xcounter == 0:
                if k not in temp_list_k:
                    only_1st = k + "_1st"  ## appends a tag to the key in this list to know its origin
                    temp_list_k.append(
                        only_1st)  ## however dictionary stores original keys
                    temp_dict[k] = v
            elif xcounter == 1:
                only_1st = k + "_1st"
                if only_1st not in temp_list_k:
                    only_2nd = k + "_2nd"
                    temp_list_k.append(k + "_2nd")
                    temp_dict[k] = v
                else:
                    x = float(temp_dict[k]) - float(v)  ## x is the difference
                    # between the value in the first file and the second file
                    temp_dict[k] = range_conversion(x, 0, 1)
                    temp_list_k.remove(
                        only_1st)  ## removes key from list if it is also present in second file

    for k, v in temp_dict.items():
        only_1st = k + "_1st"
        only_2nd = k + "_2nd"
        if only_1st in temp_list_k:
            temp_dict[k] = 1
        elif only_2nd in temp_list_k:
            temp_dict[k] = 0

    return temp_dict


def main():
    parser = argparse.ArgumentParser(
        description="Compares two json files with coverage percentage")
    parser.add_argument("-i", "--input_jsons", dest="inputfile", nargs=2,
                        required=True,
                        help="Provide the input json files of interest.")
    # parser.add_argument('-c','--cutoff', dest='cutoff', default=0,
    # help='Provide the cutoff value used \
    #	for the minimum coverage allowed to be outputed to json files. This
    # value should be equal in both files to compare.')

    args = parser.parse_args()

    jsonfiles = args.inputfile
    jsons = []
    ## checks if json is in same directory
    for json_f in jsonfiles:
        jsons.append(os.path.basename(json_f))

    list_of_json = load_jsons(jsonfiles)

    final_dict = diff_jsons(list_of_json)

    ## writes output file
    ## output file have the original name of input jsons in order to be parsable by other scripts
    out_file = open(jsons[0][:-5] + "_vs_" + jsons[1][:-5] + ".json", "w")
    out_file.write(json.dumps(final_dict))
    out_file.close()


if __name__ == "__main__":
    main()
