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


Fit all the models for the given dataset.

'''

import sys
import argparse
import mdlfit as mf

def fit_all_models(dataset_string, signature='4/4', beat_subdivisions=2,
                   data_folder='../data/encoded/', precision=None):
    """Fit all models for the given dataset.

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
        name of the folder containing the data, i.e. the pickle files
    precision: float
        precision value used for coding (default sqrt(n)
        with n total number of beat positions)

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

    # models
    models = []

    for name in model_names:
        # create model
        model = mf.models.createModel(name, dataset, signature, beat_subdivisions, d=precision)
        # save model
        models.append(model)

    for model in models:
        colwidth = 80
        print('='*colwidth)
        # show model
        # model.show()
        model.show(colwidth=colwidth)

    print('='*colwidth)

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
    parser.add_argument('-p', '--precision',
                        help='precision value used for coding (default sqrt(n) with n total number'\
                        ' of beat positions)',
                        default=None, type=int, action='store')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])

    # fit all the models for the given dataset
    fit_all_models(parameters['dataset_string'],
                   parameters['signature'],
                   parameters['beat_subdivisions'],
                   parameters['data_folder'],
                   parameters['precision'])
