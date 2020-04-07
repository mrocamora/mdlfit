# encoding: utf-8
# pylint: disable=C0103
"""



"""

import warnings
import numpy as np
import music21


def remove_duplicates(input_dataset):
    """Remove duplicate elements in a dataset

    Parameters
    -------
    input_dataset : list
        list of dictionaries, each one corresponds to a piece


    Returns
    -------
    output_dataset : list
        list of dictionaries, each one corresponds to a piece
    """
    # total number of pieces of the input dataset
    N = len(input_dataset)

    # indexes of the elements to delete
    del_indexes = []

    # number of measures of each piece
    num_measures = N*[0]

    # save in advance the number of measures of each piece
    for ind, piece in enumerate(input_dataset):
        num_measures[ind] = len(piece["measures"])

    # for each element in input dataset
    for ind1, piece1 in enumerate(input_dataset):
        # compare to each other element in the dataset
        for ind2, piece2 in enumerate(input_dataset):
            # avoid self comparison and duplicate comparison
            if ind1 < ind2:
                # see if measure length is the same
                if num_measures[ind1] == num_measures[ind2]:
                    # if same they have the same number of measures
                    # then compare notes and rests
                    notes1 = piece1["score"].flat.notesAndRests
                    notes2 = piece2["score"].flat.notesAndRests
                    # check if they have the same number of notes and rests
                    if len(notes1) == len(notes2):
                        # flag to indicate they are different
                        are_different = False
                        ind = 0
                        # compare not by note untill they are different
                        while not are_different and ind < len(notes1):
                            d1 = notes1[ind].duration.quarterLength
                            d2 = notes2[ind].duration.quarterLength
                            f1 = notes1[ind].pitch
                            f2 = notes2[ind].pitch
                            print(d1, d2)
                            print(f1, f2)
                            #if notes1[ind] != notes2[ind]:
                            if (d1 != d2) or (f1 != f2):
                                are_different = True
                            ind += 1
                        # save index if they are different
                        if not are_different:
                            del_indexes.append(ind2)

    # set to None the elements we want to remove
    for ind in del_indexes:
        input_dataset[ind] = None

    print(del_indexes)

    # remove empty elements in list
    output_dataset = list(filter(None, input_dataset))

    return output_dataset


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

    # get the measures of the piece
    measures = piece.getElementsByClass('Measure')
    # current time signature
    current_time_signature = ""
    # flag to see if there is a single time signature
    single_signature = True

    # for each measure
    for measure in measures:
        # get time signature of current measure
        time_signature = measure.getTimeSignatures()[0]
        # set current time signature for the first time
        if current_time_signature == "":
            current_time_signature = time_signature.ratioString
        # check time signatures are the same
        if time_signature.ratioString != current_time_signature:
            single_signature = False
            break

    if not single_signature:
        current_time_signature = None

    return current_time_signature

###############################################################################
#                            MAIN PROGRAM
###############################################################################

music21.environment.set('musicxmlPath', '/usr/bin/musescore')

signature = '4/4'
beat_subdivisions = 2
dataset_name = 'oneills1850'

#corpus = ['/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/0626-0635.abc',
#          '/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/0626-0700.abc']
#corpus = ['/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/0732-0758_bs.abc',
#          '/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/0732-0758_mh.abc']
#corpus = ['/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/0951-0981.abc',
#          '/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/0981-1000.abc']
#corpus = ['/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1001-1031.abc',
#          '/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1031-1115.abc']
corpus = ['/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1556-1576.abc',
          '/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1556-1624.abc']
#corpus = ['/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1116-1135_mh.abc',
#          '/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1116-1135_ml.abc']
#corpus = ['/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1701-1780.abc',
#          '/usr/local/lib/python3.5/dist-packages/music21/corpus/oneills1850/1710-1750.abc']


# total number of parts in dataset
num_parts = 0

# save opus to avoid repeating parse
opus_list = len(corpus)*[[]]

# for each path int the corpus
for ind_path, path in enumerate(corpus):
    print(path)
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
                # print(num_parts)
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
        # print(num_parts)
    else:
        warnings.warn("The path has not given an Opus nor a Score and is ignored.",
                      RuntimeWarning)
    #input("Press Enter to continue...")


# dataset as a list of dictionaries, each one corresponds to a piece/part
# each dictionary has attributes 'name' (str) and 'measures' (list of numpy arrays of onsets)
dataset = num_parts*[[]]

# index of the piece
ind_piece = 0

# we now process each part/piece in the dataset
for opus in opus_list:
    # for each score in the opus
    for score in opus:
        # we get the part in the score
        piece = score.parts[0]
        # check if there is Metadata object in score
        if len(score.getElementsByClass('Metadata')) > 0:
            # we get the title of the piece, assuming there is a title
            title = score.metadata.title
        # check time signature
        if signature == single_time_signature(piece):

            # encode piece
            piece_measures = encode_piece(piece, signature, beat_subdivisions)

            # get the name of the piece from filename
            name = dataset_name + '_' + str(ind_piece)

            # create dictionary corresponding to current piece
            dict_piece = {"title": title "name": name, "score": piece, "measures": piece_measures}

            # save piece in dataset
            dataset[ind_piece] = dict_piece

        elif single_time_signature(piece) is None:
            warnings.warn("Piece with several Time Signatures.", RuntimeWarning)
        else:
            warnings.warn("Piece with wrong TimeSignature.", RuntimeWarning)

        # increment piece index
        ind_piece += 1


# remove empty elements in list
dataset_filtered = list(filter(None, dataset))
dataset = dataset_filtered

print(len(dataset))

for piece in dataset:
    print(piece["name"], len(piece["measures"]))

# remove duplicate elements in list
dataset_unique = remove_duplicates(dataset)
dataset = dataset_unique

print(len(dataset))

for piece in dataset:
    print(piece["name"], len(piece["measures"]))
    print(piece["measures"])


## show parts
#show_indxs = [2, 12]
#
#for ind in show_indxs:
#    score = dataset[ind]["score"]
#    score.show()
#    #score.show('text')
