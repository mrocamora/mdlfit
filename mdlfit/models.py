# encoding: utf-8
# pylint: disable=C0103
"""
Models
======

Defining, fitting and applying models
-------------------------------------

.. autosummary::
    :toctree: generated/

    new_model

"""

import warnings
import numpy as np

__all__ = ['Bernoulli', 'RefinedPosition']


def log2(value):
    """ Function to compute log2 checking for nan values.
        A nan value is substituted by 0 and a warning is raised.

    Parameters
    ----------
    value : float
        input value

    Returns
    -------
    logval : float
        returned value

    """
    # compute log2 value
    logval = np.log2(value)
    
    # check if is nan
    if np.isinf(logval):
        logval = 0
        warnings.warn("Warning: nan value found, substitued by zero. ", RuntimeWarning)

    return logval



def metric_levels(signature, beat_subdivisions):
    """ Given a time signature and the number of subdivision per beat
        this function returns a list indicating the number of metric
        levels in which a subdivision position is present

    Parameters
    ----------
    signature : str
        string denoting the time signature to consider.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.

    Returns
    -------
    levels : list
        list of the number of metric levels in which each subdivision position is present

    """
    # time signature
    if signature == '4/4':
        # number of subdivision per beat
        if beat_subdivisions == 2:
            levels = [4, 1, 2, 1, 3, 1, 2, 1]

        elif beat_subdivisions == 4:
            levels = [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]

        else:
            warnings.warn("Number of subdivision per beat not implemented yet. ", RuntimeWarning)
    elif signature == '2/4':
        if beat_subdivisions == 2:
            levels = [3,1,2,1]

        elif beat_subdivisions == 4:
            levels = [4, 1, 2, 1, 3, 1, 2, 1]

        else:
            warnings.warn("Number of subdivision per beat not implemented yet. ", RuntimeWarning)

    else:
        warnings.warn("Time signature not implemented yet. ", RuntimeWarning)


    return levels



class Bernoulli:
    """Class to represent a Bernoulli model

    Attributes
    ----------
    num_pieces : int
        Number of pieces of the dataset
    beats_measure : int 
        Number of beat subdivisions per measure
    d : int, optional
        Precision parameter

    Methods
    -------
    fit(dataset)
        Fit model parameters from dataset
    description_length()
        Compute description length
    show()
        Show model parameters


    """

    def __init__(self, dataset, d=None):

        # number of pieces in the dataset
        self.num_pieces = len(dataset)

        # beats subdivisions per measure
        self.beats_measure = dataset[0]['measures'][0].shape[0]

        # fit the model using dataset
        self.fit(dataset)

        # set the precision parameter d
        if d is None:
            self.d = np.sqrt(self.n)
        else:
            self.d = d

        # compute description length
        self.description_length()


    def fit(self, dataset):
        """Fit model parameters from dataset
        """

        # number of onsets (i.e. 1s)
        n1 = 0
        # total number of beat position (i.e. 0s and 1s)
        n = 0

        # for each piece in the dataset
        for piece in dataset:
            # add total number of 0s and 1s in piece
            n += len(piece['measures']) * self.beats_measure
            # for each measure in piece
            for measure in piece['measures']:
                # add the number of 1s in measure
                n1 += np.sum(measure)

        # save number of onset (i.e. 1s)
        self.n1 = n1
        # save number of beat position (i.e. 0s and 1s)
        self.n = n
        # save proportion
        self.p = n1/n
        #save total number of measures
        self.len_measures = n/self.beats_measure



    def description_length(self):
        """Compute description length
        """

        # dataset description length
        dataset_dl = - (self.n1 * log2(self.p) + (self.n - self.n1) * log2(1-self.p))
        # model description length
        model_dl = 2 * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self):
        """Show model parameters
        """

        print("Bernoulli model. ")
        print("Dataset Parameters")
        print("number of pieces: %d, number of beats per measure: %d" % (self.num_pieces,
                                                                         self.beats_measure))
        print("Model Parameters")
        print("number of 1s: %d, total number of beats: %d, proportion: %f" % (self.n1, self.n,
                                                                               self.p))
        print("Description length")
        print("description length per measure (bits): %f" % self.dl)



########
class Position:
    """Class to represent a Position model


    Attributes
    ----------
    num_pieces : int
        Number of pieces of the dataset
    beats_measure : int 
        Number of beat subdivisions per measure
    levels : list
        List containing the maximum metric level at each position
    d : int, optional
        Precision parameter

    Methods
    -------
    fit(dataset)
        Fit model parameters from dataset
    description_length()
        Compute description length
    show()
        Show model parameters


    """

    def __init__(self, dataset, signature, beat_subdivisions, d=None):

        # number of pieces in the dataset
        self.num_pieces = len(dataset)

        # beats subdivisions per measure
        self.beats_measure = dataset[0]['measures'][0].shape[0]

        # determine the metric levels
        self.levels = metric_levels(signature, beat_subdivisions)

        # fit the model using dataset
        self.fit(dataset)

        # set the precision parameter d
        if d is None:
            self.d = np.sqrt(self.n)
        else:
            self.d = d

        # compute description length
        self.description_length()


    def fit(self, dataset):
        """Fit model parameters from dataset
        """

        # number of onsets on each metrical position
        self.onsets = self.levels[0]*[0]
        n = 0
        for piece in dataset:
            # add total number of 0s and 1s in piece
            n += len(piece['measures']) * self.beats_measure
            for k in range(self.beats_measure):
                #sum onsets in each metrical level for all measures in piece
                self.onsets[self.levels[k]-1] += sum([measure[k] == 1
                                                      for measure in piece['measures']])

        # save total number of beat positions (i.e. 0s and 1s)
        self.n = n
        # save total number of measures
        self.len_measures = n/self.beats_measure
        # get rate instead of absolute quantity
        self.ratios = [self.onsets[i]/(self.len_measures * self.levels.count(i+1))
                       for i in range(len(self.onsets))]



    def description_length(self):
        """Compute description length
        """

        # dataset description length
        dataset_dl = - (self.len_measures *
                        sum([self.ratios[x-1]*log2(self.ratios[x-1]) +
                             (1-self.ratios[x-1])*log2(1-self.ratios[x-1])
                             for x in self.levels]))

        # model description length
        model_dl = (len(self.ratios) + 1) * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self):
        """Show model parameters
        """

        print("Position model. ")
        print("Dataset Parameters")
        print("number of pieces: %d, number of beats per measure: %d, number of measures: %d"
              % (self.num_pieces, self.beats_measure, self.len_measures))
        print("Metrical levels: %s" % (str(self.levels)))
        print("Model Parameters")
        print("Onsets per level: %s, total number of beats: %d, ratios: %s"
              % (str(self.onsets), self.n, str(self.ratios)))
        print("Description length")
        print("description length per measure (bits): %f" % self.dl)



########
class RefinedPosition:
    """Class to represent a Refined Position model


    Attributes
    ----------
    num_pieces : int
        Number of pieces of the dataset
    beats_measure : int 
        Number of beat subdivisions per measure
    d : int, optional
        Precision parameter

    Methods
    -------
    fit(dataset)
        Fit model parameters from dataset
    description_length()
        Compute description length
    show()
        Show model parameters


    """

    def __init__(self, dataset, d=None):

        # number of pieces in the dataset
        self.num_pieces = len(dataset)

        # beats subdivisions per measure
        self.beats_measure = dataset[0]['measures'][0].shape[0]

        # fit the model using dataset
        self.fit(dataset)

        # set the precision parameter d
        if d is None:
            self.d = np.sqrt(self.n)
        else:
            self.d = d

        # compute description length
        self.description_length()


    def fit(self, dataset):
        """Fit model parameters from dataset
        """

        #number of onsets on each metrical position
        self.onsets = self.beats_measure*[0]
        n = 0
        for piece in dataset:
            # add total number of 0s and 1s in piece
            n += len(piece['measures']) * self.beats_measure
            for k in range(self.beats_measure):
                #sum onsets in each metrical position for all measures in piece
                self.onsets[k] += sum([measure[k] == 1 for measure in piece['measures']])

        #save total number of beat positions (i.e. 0s and 1s)
        self.n = n
        #save total number of measures
        self.len_measures = n/self.beats_measure
        #get rate instead of absolute quantity
        self.ratios = [i/self.len_measures for i in self.onsets]



    def description_length(self):
        """Compute description length
        """

        # dataset description length
        dataset_dl = - (self.len_measures *
                        sum([x*log2(x) + (1-x)*log2(1-x) for x in self.ratios]))
        # model description length
        model_dl = (self.beats_measure +1)*np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self):
        """Show model parameters
        """

        print("Refined Position model. ")
        print("Dataset Parameters")
        print("number of pieces: %d, number of beats per measure: %d, number of measures: %d"
              % (self.num_pieces, self.beats_measure, self.len_measures))
        print("Model Parameters")
        print("Onsets per position: %s, total number of beats: %d, ratios: %s"
              % (str(self.onsets), self.n, str(self.ratios)))
        print("Description length")
        print("description length per measure (bits): %f" % self.dl)


########
class Hierarchical:
    """Class to represent a Hierarchical model


    Attributes
    ----------
    num_pieces : int
        Number of pieces of the dataset
    beats_measure : int 
        Number of beat subdivisions per measure
    levels : list
        List containing the maximum metric level at each position
    d : int, optional
        Precision parameter

    Methods
    -------
    fit(dataset)
        Fit model parameters from dataset
    description_length()
        Compute description length
    show()
        Show model parameters


    """

    def __init__(self, dataset, signature, beat_subdivisions, d=None):

        # number of pieces in the dataset
        self.num_pieces = len(dataset)

        # beats subdivisions per measure
        self.beats_measure = dataset[0]['measures'][0].shape[0]

        # determine the metric levels
        self.levels = metric_levels(signature, beat_subdivisions)

        # fit the model using dataset
        self.fit(dataset)

        # set the precision parameter d
        if d is None:
            self.d = np.sqrt(self.n)
        else:
            self.d = d

        # compute description length
        self.description_length()


    def fit(self, dataset):
        """Fit model parameters from dataset
        """

        # number of onsets of each anchor type
        self.onsets = {'pre': self.levels[0]*[0],
                       'pos': self.levels[0]*[0],
                       'un': self.levels[0]*[0],
                       'bi': self.levels[0]*[0]}

        # number of instances of each anchor type
        self.anchors = {'pre': self.levels[0]*[0],
                       'pos': self.levels[0]*[0],
                       'un': self.levels[0]*[0],
                       'bi': self.levels[0]*[0]}

        # save location of previous and next neighbour
        neighbours = self.beats_measure*[[0, 0]]
        for ind in range(self.beats_measure):
            if ind == 0:
                # first level has no neighbours
                neighbours[ind] = [-1, -1]
            elif ind == self.levels.index(self.levels[0]-1):
                # second level has only one neighbour in the measure (and another in next measure)
                neighbours[ind] = [0, -1]
            else:
                # for the rest find the position of the nearest neighbours
                ind_dist = np.where(np.array(levels[ind:]) > levels[ind])
                ind_back = ind - ind_dist[0][0]
                ind_next = ind + ind_dist[0][0]
                neighbours[ind] = [ind_back, ind_next]

        n = 0
        for piece in dataset:
            # add total number of 0s and 1s in piece
            n += len(piece['measures']) * self.beats_measure
            # for each measure in piece
            for measure in piece['measures']:
                # for each position in measure
                for pos in range(self.beats_measure):
                    # check if there is an onset in pos
                    is_onset = measure[pos] == 1
                    # check if there are onsets at the neighbours
                    ons_neigh = [0, 0]
                    if measure[neighbours[pos][0]] == 1:
                        ons_neigh[0] = 1
                    if measure[neighbours[pos][1]] == 1:
                        ons_neigh[1] = 1
                    # check and save the anchor type
                    # un-anchored location
                    if ons_neigh == [0, 0]:
                        self.anchors['un'][levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['un'][levels[pos]-1] += 1
                    # bi-anchored location 
                    if ons_neigh == [1, 1]:
                        self.anchors['bi'][levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['bi'][levels[pos]-1] += 1
                    # pre-anchored location
                    if ons_neigh == [1, 0]:
                        self.anchors['pre'][levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['pre'][levels[pos]-1] += 1
                    # pos-anchored location
                    if ons_neigh == [1, 1]:
                        self.anchors['pos'][levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['pos'][levels[pos]-1] += 1





        # save total number of beat positions (i.e. 0s and 1s)
        self.n = n
        # save total number of measures
        self.len_measures = n/self.beats_measure
        # get rate instead of absolute quantity
        self.ratios = [self.onsets[i]/(self.len_measures * self.levels.count(i+1))
                       for i in range(len(self.onsets))]



    def description_length(self):
        """Compute description length
        """

        # dataset description length
        dataset_dl = - (self.len_measures *
                        sum([self.ratios[x-1]*log2(self.ratios[x-1]) +
                             (1-self.ratios[x-1])*log2(1-self.ratios[x-1])
                             for x in self.levels]))

        # model description length
        model_dl = (len(self.ratios) + 1) * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self):
        """Show model parameters
        """

        print("Position model. ")
        print("Dataset Parameters")
        print("number of pieces: %d, number of beats per measure: %d, number of measures: %d"
              % (self.num_pieces, self.beats_measure, self.len_measures))
        print("Metrical levels: %s" % (str(self.levels)))
        print("Model Parameters")
        print("Onsets per level: %s, total number of beats: %d, ratios: %s"
              % (str(self.onsets), self.n, str(self.ratios)))
        print("Description length")
        print("description length per measure (bits): %f" % self.dl)



