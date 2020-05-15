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

Fit all the models for the given dataset after computing optimal precision.

'''


import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import mdlfit as mf

def fit_all_models_and_precisions(dataset_string, signature='4/4', beat_subdivisions=2,
                                  data_folder='../data/encoded/', min_val=1, max_val=8):
    """Fit all models for the given dataset, searching for optimal precision.

    Parameters
    ----------
    dataset_string : str
        the name of the dataset as used in the encoding, for instance, as defined in music21
        (e.g. 'airdsAirs', 'oneills1850', 'EssenFolksong')
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

    # model names
    model_names = ['Bernoulli', 'Position', 'RefinedPosition',
                   'Hierarchical', 'RefinedHierarchical']

    # optimal models
    optimal_models = []

    # precision grid of values
    precision_grid = [2**k for k in range(min_val, max_val+1)]

    # for each model
    for model_name in model_names:
        ## resulting model (parameters may vary) for the given precisions
        models = []

        # for each precision
        for precision in precision_grid:
            # create model
            model = mf.models.createModel(model_name, dataset, signature, beat_subdivisions,
                                          d=precision)
            # save model
            models.append(model)

        # description length for each model
        dls = np.array([model.dl for model in models])

        # create dictionary corresponding to current piece
        dict_models = {"model": model_name, "description lengths": dls}

        optimal_models.append(dict_models)


    # plot the results
    plt.figure()
    grid_exp = range(min_val, max_val+1)
    for ind, model_name in enumerate(model_names):

        # description lengths for model
        description_lengths = optimal_models[ind]['description lengths']
        # find index of the model with the minunim description length
        argmin = np.argmin(description_lengths)

        plt.plot(grid_exp, description_lengths, '-*', label=model_name)
        plt.plot(grid_exp[argmin], description_lengths[argmin], 'ok', markersize=12, alpha=0.2)

    plt.legend(loc='upper right')
    plt.xlabel("$\\log_2(d)$")
    plt.ylabel("description length (bits)")
    plt.title("fitting " + dataset_string + " dataset with all models")

    plt.show()


def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_string',
                        action='store',
                        help='the name of the dataset as used in the encoding, for instance, as'\
                        ' defined in music21 (e.g. airdsAirs, oneills1850, EssenFolksong)')
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
                        default=12, type=int, action='store')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])

    # fit the model for the given dataset for all values in precision grid
    fit_all_models_and_precisions(parameters['dataset_string'],
                                  parameters['signature'],
                                  parameters['beat_subdivisions'],
                                  parameters['data_folder'],
                                  parameters['min_val'],
                                  parameters['max_val'])
