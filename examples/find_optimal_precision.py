#!/usr/bin/env python3
# encoding: utf-8
# pylint: disable=C0103
'''
    __  __ _____  _      ______ _____ _______
   |  \/  |  __ \| |    |  ____|_   _|__   __|
   | \  / | |  | | |    | |__    | |    | |
   | |\/| | |  | | |    |  __|   | |    | |
   | |  | | |__| | |____| |     _| |_   | |
   |_|  |_|_____/|______|_|    |_____|  |_|

 music encodind using minimum description length


Compute optimal precision value for a given model and dataset

'''


import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import mdlfit as mf

def fit_all_precisions(dataset_string, model_name, signature='4/4', beat_subdivisions=2,
                       data_folder='../data/encoded/', min_val=1, max_val=8):
    """Fit a model for the given dataset, searching for optimal precision.

    Parameters
    ----------
    dataset_string : str
        the name of the dataset as used in the encoding, for instance, as defined in music21
        (e.g. 'airdsAirs', 'oneills1850', 'EssenFolksong')
    model_name : str
        name of the model to use
        (options: 'Bernoulli', 'Position', 'RefinedPosition','Hierarchical', 'RefinedHierarchical')
    signature : str
        string denoting the time signature (e.g. 4/4, 2/4).
        Only pieces with that time signature (exclusively) will be encoded.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.
    data_folder : str
        Name of the folder containing the data, i.e. the pickle files
    min_val : int
    	Sets minimum value of the precision grid as 2**min_val.
    max_val : int
    	Sets maximum value of the precision grid as 2**max_val.

    """

    # strings for the signature and beat_subdivision
    signature_subdivisions = signature.replace('/', '') + "_" + str(beat_subdivisions)
    # dataset filename
    dataset_filename = dataset_string + "_" + signature_subdivisions + ".pkl"

    # load encoded the dataset
    dataset = mf.dataio.load_encoded_dataset(data_folder + dataset_filename)

    ## resulting model (parameters may vary) for the given precisions
    models = []

    # precision grid of values
    precision_grid = [2**k for k in range(min_val, max_val+1)]

    for precision in precision_grid:
        # create model
        model = mf.models.createModel(model_name, dataset, signature, beat_subdivisions,
                                      d=precision)
        # save model
        models.append(model)

    # description lenght for each model
    description_lengths = np.array([model.dl for model in models])
    # find index of the model with the minunim description length
    argmin = np.argmin(description_lengths)
    # optimal precision value
    optimal_precision = precision_grid[argmin]
    # minumum description length
    mdl = np.min(description_lengths)

    # column width
    colwidth = 100
    print('='*colwidth)
    print("Selection of optimal precision value".center(colwidth))
    print()

    fmt_s = '{:<8}{:<12}{}'
    fmt = '{:10d}{:21.6f}'
    print(fmt_s.format('', 'Precision', 'Description length').rjust(colwidth))
    print()
    for (d, dl) in zip(precision_grid, description_lengths):
        print((fmt.format(d, dl)).rjust(colwidth))

    print()
    print('Optimal precision: '.ljust(colwidth - len("{:d}".format(optimal_precision))) +
          "{:d}".format(optimal_precision))
    print('Minimum description length: '.ljust(colwidth - len("{:4.6f}".format(mdl))) +
          "{:4.6f}".format(mdl))
    print()
    models[argmin].show(colwidth=colwidth)
    print('='*colwidth)


    plt.figure()
    grid_exp = range(min_val, max_val+1)
    plt.plot(grid_exp, description_lengths, '-*')
    plt.plot(grid_exp[argmin], description_lengths[argmin], '*r', label='optimal value')
    plt.legend()
    plt.xlabel("$\\log_2(d)$")
    plt.ylabel("description length (bits)")
    plt.title(model_name + " model fitting " + dataset_string + " dataset")

    plt.show()


def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_string',
                        action='store',
                        help='the name of the dataset as used in the encoding, for instance, as'\
                        ' defined in music21 (e.g. airdsAirs, oneills1850, EssenFolksong)')
    parser.add_argument('model_name',
                        action='store',
                        help='name of the model to use'\
                        '(options: Bernoulli, Position, RefinedPosition, Hierarchical,'\
                        'RefinedHierarchical)')
    parser.add_argument('-s', '--signature',
                        help='string denoting the time signature (e.g. 4/4, 2/4)',
                        default='4/4', type=str, action='store')
    parser.add_argument('-b', '--beat_subdivisions',
                        help='number of (equal) subdivisions of each beat',
                        default='2', type=int, action='store')
    parser.add_argument('-d', '--data_folder',
                        help='name of the folder containing the data, i.e. the pickle files',
                        default='../data/encoded/', action='store')
    parser.add_argument('-m', '--min_val',
                        help='sets minimum value of the precision grid as 2**min_val',
                        default=1, type=int, action='store')
    parser.add_argument('-M', '--max_val',
                        help='sets maximum value of the precision grid as 2**max_val',
                        default=8, type=int, action='store')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])

    # fit the model for the given dataset for all values in precision grid
    fit_all_precisions(parameters['dataset_string'],
                       parameters['model_name'],
                       parameters['signature'],
                       parameters['beat_subdivisions'],
                       parameters['data_folder'],
                       parameters['min_val'],
                       parameters['max_val'])
