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

import os
import glob
import warnings
import pickle
import numpy as np
import music21

__all__ = ['encode_dataset', 'load_encoded_dataset', 'save_encoded_dataset']


def encode_dataset(dataset_string, file_ext='xml', signature='4/4', beat_subdivisions=2):
    """Load and encode a symbolic music dataset either from a folder with music files (xml) or from
    the datasets provided by music21. If a valid directory is given as `dataset_string` then the
    dataset is built from the files in the directory. If not `dataset_string` is not valid
    directory, then it is assumed that `dataset_string` is a valid dataset name as defined in
    music21 (e.g. 'airdsAirs', 'oneills1850', 'EssenFolksong').

    Parameters
    ----------
    dataset_string : str
        name (including path) of the dataset's folder or name of the dataset as defined in music21
    file_ext : str
        file extension of the dataset's files (only valid when loading dataset from directory)
    signature : str
        string denoting the time signature to consider.
        Only pieces with that time signature (exclusively) will be encoded.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.

    Returns
    -------
    dataset : list
        list of dictionaries, each one corresponds to a piece

    Examples
    --------

    Load the tango dataset included in the mdlfit package.
    Load a dataset from the ones included in musi21.
    """

    # check if dataset_string is a directory
    if os.path.isdir(dataset_string):

        # encode dataset from folder
        dataset = encode_dataset_folder(dataset_string,
                                        file_ext=file_ext,
                                        signature=signature,
                                        beat_subdivisions=beat_subdivisions)
    else:
        # if not a folder we assume it is a dataset name as in music21
        dataset = encode_dataset_music21(dataset_string,
                                         signature=signature,
                                         beat_subdivisions=beat_subdivisions)


    return dataset


def encode_dataset_music21(dataset_name, signature='4/4', beat_subdivisions=2):
    """Load a dataset provided by music21

    Parameters
    ----------
    dataset_name : str
        name of the dataset in music21
    file_ext : str
        file extension of the dataset's files
    signature : str
        string denoting the time signature to consider.
        Only pieces with that time signature (exclusively) will be encoded.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.

    Returns
    -------
    dataset : list
        list of dictionaries, each one corresponds to a piece
    """

    # get muic21 corpus from corpus name
    corpus = music21.corpus.getComposer(dataset_name)

    # total number of parts in dataset
    num_parts = 0

    # save opus to avoid repeating parse
    opus_list = len(corpus)*[[]]

    # save opus paths
    opus_paths = len(corpus)*['']

    # in the following we compute the total number of pieces to initialize list

    # for each path int the corpus
    for ind_path, path in enumerate(corpus):
        print(path)
        # save opus path
        opus_paths[ind_path] = path
        # convert path to opus
        opus = music21.converter.parse(path)
        # check that we get an opus
        if isinstance(opus, music21.stream.Opus):
            # list to save scores in opus
            scores_list = len(opus)*[[]]
            # for each score in the opus
            for ind_score, score in enumerate(opus):
                # check that we get an score
                if isinstance(score, music21.stream.Score):
                    # count the number of parts
                    # WARNING: if folksongs are considered then we assume
                    # there is only one part (melody)
                    num_parts += 1
                    # save score in the scores list
                    scores_list[ind_score] = score
                else:
                    warnings.warn("The Opus has not given a Score and is ignored.", RuntimeWarning)
            # save list of scores
            opus_list[ind_path] = scores_list
        # if not an opus then it can be a score (ex. oneills1850/0731-0731.abc)
        elif isinstance(opus, music21.stream.Score):
            scores_list = []
            scores_list.append(opus)
            opus_list[ind_path] = scores_list
            num_parts += 1
        else:
            warnings.warn("The path has not given an Opus nor a Score and is ignored.",
                          RuntimeWarning)
        #input("Press Enter to continue...")

    # dataset as a list of dictionaries, each one corresponds to a piece/part
    # each dictionary has attributes 'name' (str) and 'measures' (list of numpy arrays of onsets)
    dataset = num_parts*[[]]
    # list to save the score of each element in the dataset
    scores = num_parts*[None]

    # index of the piece
    ind_piece = 0

    # we now process each part/piece in the dataset
    for ind_opus, opus in enumerate(opus_list):
        # for each score in the opus
        for ind_score, score in enumerate(opus):
            # we get the part in the score
            piece = score.parts[0]

            # check if there is a title in the metadata
            if hasattr(score.metadata, 'title'):
                title = score.metadata.title
            else:
                title = 'Empty-Title'

            # check time signature
            if signature == single_time_signature(piece):

                # encode piece
                piece_measures = encode_piece(piece, signature, beat_subdivisions)

                # create dictionary corresponding to current piece
                dict_piece = {"dataset": dataset_name, "ind_piece": ind_piece,
                              "title": title, "path": opus_paths[ind_opus],
                              "ind_score": ind_score, "measures": piece_measures}

                # save piece in dataset
                dataset[ind_piece] = dict_piece
                # save score of the piece
                scores[ind_piece] = piece

            elif single_time_signature(piece) is None:
                warnings.warn("Piece with several Time Signatures.", RuntimeWarning)
            else:
                warnings.warn("Piece with wrong TimeSignature.", RuntimeWarning)

            # increment piece index
            ind_piece += 1


    # remove empty elements in list
    dataset_filtered = list(filter(None, dataset))
    scores_filtered = list(filter(None, scores))

    # remove duplicate elements in list
    dataset, scores = remove_duplicates(dataset_filtered, scores_filtered)

    return dataset


def remove_duplicates(input_dataset, input_scores):
    """Remove duplicate elements in a dataset

    Parameters
    -------
    input_dataset : list
        list of dictionaries, each one corresponds to a piece
    input_scores : list
        list of scores of each piece


    Returns
    -------
    output_dataset : list
        list of dictionaries, each one corresponds to a piece
    """
    # total number of pieces of the input dataset
    N = len(input_dataset)

    # copy input list into output list
    output_dataset = input_dataset[:]
    # copy input list into output list
    output_scores = input_scores[:]

    # indexes of the elements to delete
    del_indexes = []

    # number of measures of each piece
    num_measures = N*[0]

    # save in advance the number of measures of each piece
    for ind, piece in enumerate(input_dataset):
        num_measures[ind] = len(piece["measures"])

    # for each element in input dataset
    for ind1 in range(len(input_dataset)):
        # compare to each other element in the dataset
        for ind2 in range(len(input_dataset)):
            # avoid self comparison and duplicate comparison
            if ind1 < ind2:
                # see if measure length is the same
                if num_measures[ind1] == num_measures[ind2]:
                    # if same they have the same number of measures then compare notes
                    notes1 = input_scores[ind1].flat.getElementsByClass('Note')
                    notes2 = input_scores[ind2].flat.getElementsByClass('Note')
                    # check if they have the same number of notes
                    if len(notes1) == len(notes2):
                        # flag to indicate they are different
                        are_different = False
                        ind = 0
                        # compare note by note untill they are different
                        while not are_different and ind < len(notes1):
                            d1 = notes1[ind].duration.quarterLength
                            d2 = notes2[ind].duration.quarterLength
                            f1 = notes1[ind].pitch
                            f2 = notes2[ind].pitch
                            # if durations or pitches are different
                            if (d1 != d2) or (f1 != f2):
                                are_different = True
                            ind += 1
                        # save index if they are different
                        if not are_different:
                            del_indexes.append(ind2)

    # set to None the elements we want to remove
    for ind in del_indexes:
        output_dataset[ind] = None
        output_scores[ind] = None

    # remove empty elements in list
    output_dataset = list(filter(None, output_dataset))
    output_scores = list(filter(None, output_scores))

    return output_dataset, output_scores


def encode_dataset_folder(dataset_folder, file_ext='xml', signature='4/4', beat_subdivisions=2):
    """Load dataset from folder with music xml files.

    Parameters
    ----------
    dataset_folder : str
        name (including path) of the dataset's folder
    file_ext : str
        file extension of the dataset's files
    signature : str
        string denoting the time signature to consider.
        Only pieces with that time signature (exclusively) will be encoded.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.

    Returns
    -------
    dataset : list
        list of dictionaries, each one corresponds to a piece

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
    # get the dataset name from the last directory of the path
    dataset_name = os.path.basename(os.path.dirname(dataset_folder))

    # dataset as a list of dictionaries, each one corresponds to a piece
    # each dictionary has attributes 'name' (str) and 'measures' (list of numpy arrays of onsets)
    dataset = num_files*[[]]

    # for each file in the dataset
    for ind_file, filename in enumerate(filenames):
        print('ind_file: %d, %s' % (ind_file, filename))
        # open file using music21 parser
        score = music21.converter.parse(filename)

        # check if there is a title in the metadata
        if hasattr(score.metadata, 'title'):
            title = score.metadata.title
        else:
            title = 'Empty-Title'

        # get only first part
        piece = score.parts[0]

        # check time signature
        if signature == single_time_signature(piece):

            # encode piece
            piece_measures = encode_piece(piece, signature, beat_subdivisions)

            # create dictionary corresponding to current piece
            dict_piece = {"dataset": dataset_name, "ind_piece": ind_file,
                          "title": title, "path": filename,
                          "ind_score": 0, "measures": piece_measures}

            # save piece in dataset
            dataset[ind_file] = dict_piece

        elif single_time_signature(piece) is None:
            warnings.warn("Piece with several Time Signatures.", RuntimeWarning)
        else:
            warnings.warn("Piece with wrong TimeSignature.", RuntimeWarning)

    # remove empty elements in list
    dataset_filtered = list(filter(None, dataset))
    dataset = dataset_filtered

    return dataset


def encode_piece(piece, signature='4/4', beat_subdivisions=2):
    """Encode the onsets in the given piece as a list, each element being a sequence of 0s and 1s
    corresponding to each measure.

    Parameters
    ----------
    piece: music21.stream
        piece to be encoded
    signature : str
        string that defines the time signature
    beat_subdivisions : int
        number of subdivisions per beat

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
    # beats subdivisions per measure
    beats_measure = ts_num * beat_subdivisions

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
                ons_pos = float((note.beat-1) * beat_subdivisions)
                # check if onset is integer
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


#def single_time_signature(piece):
#    """Check if piece has a single time signature and return it. Otherwise return None.
#
#    Parameters
#    ----------
#    piece : music21.stream
#        piece to check time signature
#
#    Returns
#    -------
#    time_signature : str
#        string describing the time signature or None if not single time signature in the whole piece
#
#    """
#
#    # get the measures of the piece
#    measures = piece.getElementsByClass('Measure')
#    # current time signature
#    current_time_signature = ""
#    # flag to see if there is a single time signature
#    single_signature = True
#
#    # for each measure
#    for measure in measures:
#        # get time signature of current measure
#        time_signature = measure.getTimeSignatures()[0]
#        # set current time signature for the first time
#        if current_time_signature == "":
#            current_time_signature = time_signature.ratioString
#        # check time signatures are the same
#        if time_signature.ratioString != current_time_signature:
#            single_signature = False
#            break
#
#    if not single_signature:
#        current_time_signature = None
#
#    return current_time_signature


def single_time_signature(piece):
    """Check if piece has a single time signature and return it. Otherwise return None.

    Parameters
    ----------
    piece : music21.stream
        piece to check time signature

    Returns
    -------
    time_signature : str
        string describing the time signature or None if not single time signature in the whole piece

    """

    # get time signatures in the piece
    time_signatures = [ts.ratioString for ts in
                       piece.recurse().getElementsByClass(music21.meter.TimeSignature)]
    # use a set to remove duplicate time signatures
    time_signatures = list(set(time_signatures))

    # check if single time signature
    if len(time_signatures) == 1:
        time_signature = time_signatures[0]
    else:
        # set None if not single time signature
        time_signature = None

    return time_signature


def load_encoded_dataset(filename):
    """Load encoded dataset from file using serialization.

    Parameters
    ----------
    filename : str
        file name of the encoded dataset (as a pkl file)

    Returns
    -------
    dataset : list
        list of dictionaries, each one corresponds to a piece


    """
    # load dataset
    dataset = pickle.load(open(filename, "rb"))


    return dataset


def save_encoded_dataset(dataset, filename):
    """Save encoded dataset to a file using serialization.

    Parameters
    ----------
    dataset : list
        list of dictionaries, each one corresponds to a piece

    filename : str
        path and file name to save the encoded dataset

    """

    pickle.dump(dataset, open(filename, "wb"))
