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


Compute a corpus' description length for different models, searching for optimal precision d in each case

'''


import sys
import argparse
import mdlfit as mf

def fit_all_precisions(dataset_string, model_name, signature='4/4', beat_subdivisions=2,
                   data_folder='../data/encoded/', precision_range = [2**k for k in range(3,10)]):
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
    precision_range : list
    	List of integers containing the precisions to consider.

    """

    # strings for the signature and beat_subdivision
    signature_subdivisions = signature.replace('/', '') + "_" + str(beat_subdivisions)
    # dataset filename
    dataset_filename = dataset_string + "_" + signature_subdivisions + ".pkl"

    # load encoded the dataset
    dataset = mf.dataio.load_encoded_dataset(data_folder + dataset_filename)

    ## resulting model (parameters may vary) for the given precisions
    models = []

    for precision in precision_range:
    # create model
    model = mf.models.createModel(model_name, dataset, signature, beat_subdivisions, d=precision)
    # save model
    models.append(model)

    description_lengths = [model.dl for model in models]
    #find index or the minunim description length
    argmin = min(enumerate(description_lengths))[0]
    optimal_precision = precision_range[argmin]
    mdl = min(description_lengths)

    #for model in models:
    #    print('='*50)
    #    # show model
    #    model.show()

    print(model_name)
    print('='*50)
    print('Description lengths: %s. \n Optimal precision: %d.\n Minimum description length: %d', str(description_lengths), optimal_precision, mdl )


def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_string',
                        action='store',
                        help='the name of the dataset as used in the encoding, for instance, as'\
                        ' defined in music21 (e.g. airdsAirs, oneills1850, EssenFolksong)')
    parser.add_argument('model_name',
    					action = 'store',
    					help = 'name of the model to use'\
    					'(options: Bernoulli, Position, RefinedPosition, Hierarchical, RefinedHierarchical)'
    					)
    parser.add_argument('-s', '--signature',
                        help='string denoting the time signature (e.g. 4/4, 2/4)',
                        default='4/4', type=str, action='store')
    parser.add_argument('-b', '--beat_subdivisions',
                        help='number of (equal) subdivisions of each beat',
                        default='2', type=int, action='store')
    parser.add_argument('-d', '--data_folder',
                        help='name of the folder containing the data, i.e. the pickle files',
                        default='../data/encoded/', action='store')
    parser.add_argument('-p', '--precision_range',
                        help='precision values used for coding (default [2^3, 2^4, ..., 2^10])',
                        default=[2**k for k in range(3,10)], type=list, action='store')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])

    # fit all the models for the given dataset
    fit_all_precisions(parameters['dataset_string'],
    			   paramters('model_name')
                   parameters['signature'],
                   parameters['beat_subdivisions'],
                   parameters['data_folder'],
                   parameters['precision_range'])
