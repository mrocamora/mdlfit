# encoding: utf-8
# pylint: disable=C0103
"""
Data-IO
===========

Reading and writing annotations
-------------------------------

.. autosummary::
    :toctree: generated/

    load_dataset

"""

import glob
import warnings
import numpy as np
import music21

__all__ = ['load_dataset']


def load_dataset(dataset_folder, file_ext='xml', signature='4/4', beats_measure=8):
    """Load dataset from folder with music xml files.

    Parameters
    ----------
    labels_file : str
        name (including path) of the input file
    delimiter : str
        string used as delimiter in the input file
    times_col : int
        column index of the time data
    labels_col : int
        column index of the label data

    Returns
    -------
    beat_times : np.ndarray
        time instants of the beats
    beat_labels : list
        labels at the beats (e.g. 1.1, 1.2, etc)

    Examples
    --------

    Load an included example file from the candombe dataset.
    http://www.eumus.edu.uy/candombe/datasets/ISMIR2015/

    >>> annotations_file = carat.util.example_beats_file(num_file=1)
    >>> beats, beat_labs = annotations.load_beats(annotations_file)
    >>> beats[0]
    0.548571428
    >>> beat_labs[0]
    '1.1'

    Load an included example file from the samba dataset.
    http://www.smt.ufrj.br/~starel/datasets/brid.html

    >>> annotations_file = carat.util.example_beats_file(num_file=2)
    >>> beats, beat_labs = annotations.load_beats(annotations_file, delimiter=' ')
    >>> beats
    array([ 2.088,  2.559,  3.012,   3.48,  3.933,   4.41,  4.867,   5.32,
            5.771,  6.229,   6.69,  7.167,  7.633,  8.092,  8.545,   9.01,
             9.48,  9.943, 10.404, 10.865, 11.322, 11.79 , 12.251, 12.714,
           13.167, 13.624, 14.094, 14.559, 15.014, 15.473, 15.931,   16.4,
           16.865, 17.331, 17.788, 18.249, 18.706, 19.167, 19.643, 20.096,
           20.557, 21.018, 21.494, 21.945, 22.408, 22.869, 23.31 , 23.773,
           24.235, 24.692, 25.151, 25.608, 26.063, 26.52 ])

    >>> beat_labs
    ['1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2',
     '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2',
     '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2',
     '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2']


    Notes
    -----
    It is assumed that the beat annotations are provided as a text file (csv).
    Apart from the time data (mandatory) a label can be given for each beat (optional).
    The time data is assumed to be given in seconds.
    The labels may indicate the beat number within the rhythm cycle (e.g. 1.1, 1.2, or 1, 2).
    """

    # files in folder
    filenames = glob.glob(dataset_folder + "*." + file_ext)
    # number of files
    num_files = len(filenames)

    # dataset as a list of pieces, each piece is a list of
    # measures each measure is a numpy array of onsets
    dataset = num_files*[[]]

    # for each file in the dataset
    for ind_file, filename in enumerate(filenames):
        print('ind_file: %d, %s', (ind_file, filename))
        # open file using music21 parser (and get only first part)
        piece = music21.converter.parse(filename).parts[0]
        # get the time signatures
        time_signature = piece.getTimeSignatures()[0]

        # check time signature
        if time_signature.ratioString == signature:

            # encode piece
            piece_measures = encode_piece(piece, signature=signature, beats_measure=beats_measure)

            # save piece in dataset
            dataset[ind_file] = piece_measures

        else:
            warnings.warn("Piece with wrong TimeSignature.", RuntimeWarning)

    return dataset


def encode_piece(piece, signature='4/4', beats_measure=8):
    """Encode the onsets in the given piece as a list, each element being a sequence of 0s and 1s
    corresponding to each measure.

    Parameters
    ----------
    piece: music21.stream
        piece to be encoded
    signature : str
        string that defines the time signature
    beats_meatsure : int
        number of beats per measure

    Returns
    -------
    piece_measures : list of np.ndarray
        a list of arrays containing a 1 for a note onset and 0 otherwise

    Notes
    -----
    The note positions are obtained with note.beat but could be also obtained with note.offset.
    """

    # convert time signature into numerator denominator
    ts_num = int(signature.split('/')[0])
    # ratio used to convert to our beats per measure
    beats_ratio = beats_measure / ts_num

    # get the measures of the piece
    measures = piece.getElementsByClass('Measure')
    # number of measures
    num_measures = len(measures)
    # list of measures in the piece
    piece_measures = num_measures*[[]]

    # for each measure
    for ind_m, m in enumerate(measures):
        # notes in current measure
        measure_notes = m.flat.notes
        # positions of all onsets
        onsets_pos = []
        # for each note in measure
        for note in measure_notes:
            # if not chord
            if not note.isChord:
                # compute onset position in grid (Note: this could alse be obtained with offset)
                ons_pos = (note.beat-1) * beats_ratio
                if ons_pos.is_integer():
                    onsets_pos.append(int(ons_pos))
                else:
                    warnings.warn("Onset position out of grid.", RuntimeWarning)
        # encode note positions as 0/1
        bin_pos = np.zeros((beats_measure,), dtype=int)
        bin_pos[onsets_pos] = 1

        # save coded measure in piece
        piece_measures[ind_m] = bin_pos

    return piece_measures

#def load_dataset_old(dataset_folder, file_ext='xml', signature='4/4', beats_measure=8):
#    """Load dataset from folder with music xml files.
#
#    Parameters
#    ----------
#    labels_file : str
#        name (including path) of the input file
#    delimiter : str
#        string used as delimiter in the input file
#    times_col : int
#        column index of the time data
#    labels_col : int
#        column index of the label data
#
#    Returns
#    -------
#    beat_times : np.ndarray
#        time instants of the beats
#    beat_labels : list
#        labels at the beats (e.g. 1.1, 1.2, etc)
#
#    Examples
#    --------
#
#    Load an included example file from the candombe dataset.
#    http://www.eumus.edu.uy/candombe/datasets/ISMIR2015/
#
#    >>> annotations_file = carat.util.example_beats_file(num_file=1)
#    >>> beats, beat_labs = annotations.load_beats(annotations_file)
#    >>> beats[0]
#    0.548571428
#    >>> beat_labs[0]
#    '1.1'
#
#    Load an included example file from the samba dataset.
#    http://www.smt.ufrj.br/~starel/datasets/brid.html
#
#    >>> annotations_file = carat.util.example_beats_file(num_file=2)
#    >>> beats, beat_labs = annotations.load_beats(annotations_file, delimiter=' ')
#    >>> beats
#    array([ 2.088,  2.559,  3.012,   3.48,  3.933,   4.41,  4.867,   5.32,
#            5.771,  6.229,   6.69,  7.167,  7.633,  8.092,  8.545,   9.01,
#             9.48,  9.943, 10.404, 10.865, 11.322, 11.79 , 12.251, 12.714,
#           13.167, 13.624, 14.094, 14.559, 15.014, 15.473, 15.931,   16.4,
#           16.865, 17.331, 17.788, 18.249, 18.706, 19.167, 19.643, 20.096,
#           20.557, 21.018, 21.494, 21.945, 22.408, 22.869, 23.31 , 23.773,
#           24.235, 24.692, 25.151, 25.608, 26.063, 26.52 ])
#
#    >>> beat_labs
#    ['1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2',
#     '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2',
#     '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2',
#     '1', '2', '1', '2', '1', '2', '1', '2', '1', '2', '1', '2']
#
#
#    Notes
#    -----
#    It is assumed that the beat annotations are provided as a text file (csv).
#    Apart from the time data (mandatory) a label can be given for each beat (optional).
#    The time data is assumed to be given in seconds.
#    The labels may indicate the beat number within the rhythm cycle (e.g. 1.1, 1.2, or 1, 2).
#    """
#
#    # files in folder
#    filenames = glob.glob(dataset_folder + "*." + file_ext)
#    # number of files
#    num_files = len(filenames)
#
#    # convert time signature into numerator denominator
#    ts_num = int(signature.split('/')[0])
#    ts_den = int(signature.split('/')[1])
#    # ratio used to convert to our beats per measure
#    beats_ratio = beats_measure / ts_num
#
#    # dataset as a list of pieces
#    # each piece is a list of measures
#    # each measure is a numpy array of onsets
#    dataset = num_files*[[]]
#
#    # for each file in the dataset
#    for ind_file, filename in enumerate(filenames):
#        print('ind_file: %d, %s', (ind_file, filename))
#        # open file using music21 parser (and get only first part)
#        piece = music21.converter.parse(filename).parts[0]
#        # get the measures of the piece
#        measures = piece.getElementsByClass('Measure')
#
#        # number of measures
#        num_measures = len(measures)
#        # list of measures in the piece
#        piece_measures = num_measures*[[]]
#
#        # for each measure
#        for ind_m, m in enumerate(measures):
#            # check time signature
#            time_signature = m.getTimeSignatures()[0]
#            num = time_signature.numerator
#            den = time_signature.denominator
#            # if time signature is correct
#            if (num == ts_num) & (den == ts_den):
#                # notes in current measure
#                measure_notes = m.flat.notes
#                # positions of all onsets
#                onsets_pos = []
#                # for each note in measure
#                for note in measure_notes:
#                    # if not chord
#                    if not note.isChord:
#                        # compute onset position in grid
#                        # Note: this could alse be obtained with offset
#                        ons_pos = (note.beat-1) * beats_ratio
#                        if ons_pos.is_integer():
#                            onsets_pos.append(int(ons_pos))
#                        else:
#                            warnings.warn("Onset position out of grid.", RuntimeWarning)
#                # encode note positions as 0/1
#                bin_pos = np.zeros((beats_measure,), dtype=int)
#                bin_pos[onsets_pos] = 1
#
#                # save coded measure in piece
#                piece_measures[ind_m] = bin_pos
#            else:
#                warnings.warn("Measure with wrong TimeSignature.", RuntimeWarning)
#
#            # save piece in dataset
#            dataset[ind_file] = piece_measures
#
#    return dataset
