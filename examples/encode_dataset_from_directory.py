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


Encode a music dataset from the files in a given directory.

'''

import sys
import argparse
from mdlfit.dataio import encode_dataset
from mdlfit.dataio import save_encoded_dataset


def encode_dataset_from_string(dataset_string, signature='4/4', beat_subdivisions=2,
                               file_ext='xml', output_file=None):
    """Load and encode a symbolic music dataset from the files in a given directory.

    Parameters
    ----------
    dataset_string : str
        complete path to the dataset folder containing the music files
    signature : str
        string denoting the time signature (e.g. 4/4, 2/4).
        Only pieces with that time signature (exclusively) will be encoded.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.
    file_ext : str
        file extension of the dataset's files
    output_file : str
        name of the output file to save the encoded dataset (as a pickle dump).
        If not given nothing is saved.

    Returns
    -------
    dataset : list
        list of dictionaries, each one corresponds to a piece
    """

    # encode the dataset
    dataset = encode_dataset(dataset_string,
                             signature=signature,
                             beat_subdivisions=beat_subdivisions,
                             file_ext=file_ext)

    # show some information about the encoded dataset
    print(__doc__)
    print('-'*80)
    print('Corpus name (from directory name): ', dataset[0]['dataset'])
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

    if output_file is not None:
        # save encoded dataset to pickle file
        save_encoded_dataset(dataset, output_file + "_" + signature.replace('/', '') +
                             "_" + str(beat_subdivisions) + ".pkl")



def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_string',
                        action='store',
                        help='complete path to the dataset folder containing the music files')
    parser.add_argument('-s', '--signature',
                        help='string denoting the time signature (e.g. 4/4, 2/4)',
                        default='4/4', type=str, action='store')
    parser.add_argument('-b', '--beat_subdivisions',
                        help='number of (equal) subdivisions of each beat',
                        default='2', type=int, action='store')
    parser.add_argument('-e', '--file_ext',
                        help='string denoting the extension of the music files',
                        default='xml', type=str, action='store')
    parser.add_argument('-o', '--output_file',
                        help='output file to save the encoded dataset (optional)',
                        action='store')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])

    # run the dataset encoding
    encode_dataset_from_string(parameters['dataset_string'],
                               parameters['signature'],
                               parameters['beat_subdivisions'],
                               parameters['file_ext'],
                               parameters['output_file'])
