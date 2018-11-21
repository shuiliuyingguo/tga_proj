#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
rawdata_proc.py
    - Read the TGA csv file
    - Calculate the weight loss at 100 and 770 degree
    - Plot TGA result from data and print the weight loss

Handles the primary functions
"""

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

SUCCESS = 0
INVALID_DATA = 1
IO_ERROR = 2

DEFAULT_DATA_FILE_NAME = 'data.csv'

def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def data_analysis(data_array):
    """
    data_array : numpy array of time, temperature, weight and weight percent of the sample with units in min, celsius degree, milligram and percent
    Returns
    -------
    data_stats : numpy array of temperature and weight percent of the sample with units in celsius degree and percent
    """
    print(type(data_array))
    print(data_array)
    data_stats=data_array[:,[1,3]]
    return data_stats

def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input_rates", help="The location of the input rates file",
    #                     default=DEF_IRATE_FILE, type=read_input_rates)
    parser.add_argument("-c", "--csv_data_file", help="The location (directory and file name) of the csv file with "
                                                  "data to analyze",
                    default=DEFAULT_DATA_FILE_NAME)
    args = None
    try:
        args = parser.parse_args(argv)
        args.csv_data = np.loadtxt(fname=args.csv_data_file, delimiter=',')
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, IO_ERROR
    return args, SUCCESS

def plot_analysis(base_f_name, data_stats):
    """
    Makes a plot of weight percentage against temperature--TGA test curve and annotate two interesting points
    :param base_f_name: string of base output name (without extension)
    :param data_stats: numpy array of weight percentage and temperature
    :return: saves a png file
    """
    tga_curve = plt.figure()
    ax = tga_curve.add_subplot(111)
    x_axis = data_stats[:,0]
    y_axis = data_stats[:,1]

    # calculate the weight percent loss
    W_p_loss1 = 100-data_stats[1662][1]
    W_p_loss2 = data_stats[1662][1] - data_stats[5697][1]

    line, = ax.plot(x_axis, y_axis,'b-', lw=1.1)
    plt.title('TGA test for PAA/PDADMA/KCl')
    plt.xlabel('Temperature')
    plt.ylabel('Weight Percentage')
    ax.annotate('Temperature: {} \xb0C \nWeight Percent Loss: {:2.4f}%'.format(100.004, W_p_loss1),xy=(100.004,96.3208),
                xytext=(10,63), arrowprops=dict(facecolor='black', shrink=0.05),)
    ax.annotate('Temperature: {} \xb0C \nWeight Percent Loss: {:2.4f}%'.format(770.098, W_p_loss2),xy=(770.098,26.3771),
            xytext=(455,53), arrowprops=dict(facecolor='black', shrink=0.05),)
    out_name = base_f_name + ".png"
    plt.savefig(out_name)
    print('At temperature: {} \xb0C, the weight percent loss is: {:2.4f}%'.format(100.004, W_p_loss1))
    print('At temperature: {} \xb0C, the weight percent loss is: {:2.4f}%'.format(770.098, W_p_loss2))
    print("Wrote file: {}".format(out_name))

def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != SUCCESS:
        return ret
    data_stats = data_analysis(args.csv_data)
    base_out_fname = os.path.basename(args.csv_data_file)
    base_out_fname = os.path.splitext(base_out_fname)[0] + '_analysis'
    out_fname = base_out_fname + '.csv'
    np.savetxt(out_fname, data_stats, delimiter=',')
    print("Wrote file:{}".format(out_fname))

    plot_analysis(base_out_fname, data_stats)
    return SUCCESS  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
