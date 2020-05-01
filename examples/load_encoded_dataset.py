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


Load encoded dataset from a pickle file

'''

import sys
import argparse
from mdlfit.dataio import load_encoded_dataset


def load_encoded_dataset_from_pkl(dataset_string, signature='4/4', beat_subdivisions=2,
                                  data_folder='../data/encoded/'):
    """Load and encode a symbolic music dataset from the files in a given directory.

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

    Returns
    -------
    dataset : list
        list of dictionaries, each one corresponds to a piece
    """

    # strings for the signature and beat_subdivision
    signature_subdivisions = signature.replace('/', '') + "_" + str(beat_subdivisions)
    # dataset filename
    dataset_filename = dataset_string + "_" + signature_subdivisions + ".pkl"

    # load encoded the dataset
    dataset = load_encoded_dataset(data_folder + dataset_filename)

    # show some information about the encoded dataset
    print(__doc__)
    print('-'*80)
    print('Corpus name (from directory name): ', dataset_string)
    print('Time signature: ', signature)
    print('Beat subdivisions: ', beat_subdivisions)
    print('Number of encoded pieces: ', len(dataset))
    print('-'*80)

    # number of elements to show
    N = min(10, len(dataset))
    print('Show some information for the first ' + str(N) + ' elements of the dataset:')

    for ind in range(N):
        print('Index: ' +  str(dataset[ind]["ind_piece"]) +
              ' Number of measures: '  + str(len(dataset[ind]["measures"])) +
              ' Title: ' + dataset[ind]["title"])


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

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])

    # load the dataset from a pickle file
    load_encoded_dataset_from_pkl(parameters['dataset_string'],
                                  parameters['signature'],
                                  parameters['beat_subdivisions'],
                                  parameters['data_folder'])
