# encoding: utf-8
# pylint: disable=C0103
"""
Models
======

Defining, fitting and applying models
-------------------------------------

.. autosummary::
    :toctree: generated/

    Bernoulli
    Position
    RefinedPosition
    Hierarchical
    RefinedHierarchical

"""

import numpy as np
from . import util

__all__ = ['Model', 'Bernoulli', 'Position', 'RefinedPosition',
           'Hierarchical', 'RefinedHierarchical', 'createModel']

def createModel(model_string, dataset, signature, beat_subdivisions, d=None):
    """ Function to create a model of any kind.

    Parameters
    ----------
    model_string : str
        name of the model to create (Bernoulli, Position, RefinedPosition, Hierarchical,
        RefinedHierarchical)
    dataset : list
        list of dictionaries, each one corresponds to a piece
    signature : str
        string denoting the time signature to consider.
        Only pieces with that time signature (exclusively) will be encoded.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.
    d : int, optional
        Precision parameter

    Returns
    -------
    model : Model
        a model of the type specified

    Examples
    --------
    Give some examples here, please.

    """

    model = None

    if model_string == 'Bernoulli':
        model = Bernoulli(dataset, signature, beat_subdivisions, d=d)
    elif model_string == 'Position':
        model = Position(dataset, signature, beat_subdivisions, d=d)
    elif model_string == 'RefinedPosition':
        model = RefinedPosition(dataset, signature, beat_subdivisions, d=d)
    elif model_string == 'Hierarchical':
        model = Hierarchical(dataset, signature, beat_subdivisions, d=d)
    elif model_string == 'RefinedHierarchical':
        model = RefinedHierarchical(dataset, signature, beat_subdivisions, d=d)

    return model


class Model:
    """Class to represent a generic model

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

    def __init__(self, dataset, signature, beat_subdivisions, d=None):


        # number of pieces in the dataset
        self.num_pieces = len(dataset)

        # name of the dataset
        self.dataset_name = dataset[0]['dataset']

        # beats subdivisions per measure
        self.beats_measure = dataset[0]['measures'][0].shape[0]

        # determine the metric levels
        self.levels = util.metric_levels(signature, beat_subdivisions)

        # fit the model using dataset
        self.fit(dataset)

        # set the precision parameter d
        if d is None:
            self.d = np.sqrt(self.n)
            self.default_precision = True
        else:
            self.d = d
            self.default_precision = False

        # compute description length
        self.description_length()


    def fit(self, dataset):
        """Fit model parameters from dataset
        
        Parameters
        ----------
        dataset : list of dictionaries
            list containing the encoded pieces from the dataset to fit
        """

        # total number of beat position (i.e. 0s and 1s)
        n = 0

        # for each piece in the dataset
        for piece in dataset:
            # add total number of 0s and 1s in piece
            n += len(piece['measures']) * self.beats_measure

        # save number of beat position (i.e. 0s and 1s)
        self.n = n
        # save total number of measures
        self.len_measures = n/self.beats_measure


    def description_length(self):
        """Compute description length
        """

        self.dl = 0


    def show(self, colwidth=50):
        """Show model parameters
        """
        # model name
        model_name = self.__class__.__name__ + " model"

        print(model_name.center(colwidth))
        print()
        print("Dataset".center(colwidth))
        print()
        print("Dataset name: ".ljust(colwidth - len(self.dataset_name)) + self.dataset_name)
        print("Number of pieces: ".ljust(colwidth - len(str(self.num_pieces))) +
              str(self.num_pieces))
        print("Number of beats per measure: ".ljust(colwidth - len(str(self.beats_measure))) +
              str(self.beats_measure))
        print("Total number of beat positions: ".ljust(colwidth - len(str(self.n))) +
              str(self.n))

        print()
        print("Description length".center(colwidth))
        print()
        if self.default_precision:
            # use default d
            print("Precision parameter d (default value): ".ljust(colwidth -
                                                                  len("{:d}".format(self.d))) +
                  "{:d}".format(self.d))
            #print("Precision parameter d: %d (Not indicated by user, default value.).", self.d)
        else:
            # user sets d
            print("Precision parameter d (set by user): ".ljust(colwidth -
                                                                len("{:d}".format(self.d))) +
                  "{:d}".format(self.d))
            # print("Precision parameter d: %d" % self.d, " (set by user).")
        print("Description length per measure (bits): ".ljust(colwidth -
                                                              len("{:4.6f}".format(self.dl))) +
              "{:4.6f}".format(self.dl))
        print()



class Bernoulli(Model):
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

    def __init__(self, dataset, signature, beat_subdivisions, d=None):
        super().__init__(dataset, signature, beat_subdivisions, d=d)


    def fit(self, dataset):
        """Fit model parameters from dataset
        
        Parameters
        ----------
        dataset : list of dictionaries
            list containing the encoded pieces from the dataset to fit
        """

        super().fit(dataset)

        # number of onsets (i.e. 1s)
        n1 = 0

        # for each piece in the dataset
        for piece in dataset:
            # for each measure in piece
            for measure in piece['measures']:
                # add the number of 1s in measure
                n1 += np.sum(measure)

        # save number of onset (i.e. 1s)
        self.n1 = n1
        # save proportion
        self.p = n1/self.n



    def description_length(self):
        """Compute description length
        """

        # if not default precision then compute the optimal
        # discrete value of the parameters given the precision
        if not self.default_precision:
            self.p = util.optimal_value(self.d, self.p, self.n, self.n1)


        # dataset description length
        dataset_dl = - (self.n1 * util.log2(self.p) + (self.n - self.n1) * util.log2(1-self.p))
        # model description length
        model_dl = 2 * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self, colwidth=50):
        """Show model parameters
        """

        super().show(colwidth=colwidth)

        print("Model parameters".center(colwidth))
        print()
        print("Total number of 1s: ".ljust(colwidth - len("{:d}".format(self.n1))) +
              "{:d}".format(self.n1))
        print("Proportion of 1s: ".ljust(colwidth - len("{:4.6f}".format(self.p))) +
              "{:4.6f}".format(self.p))


class Position(Model):
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
        super().__init__(dataset, signature, beat_subdivisions, d=d)


    def fit(self, dataset):
        """Fit model parameters from dataset

        Parameters
        ----------
        dataset : list of dictionaries
            list containing the encoded pieces from the dataset to fit
        
        """

        super().fit(dataset)

        # number of onsets on each metrical position
        self.onsets = self.levels[0]*[0]
        for piece in dataset:
            for k in range(self.beats_measure):
                # sum onsets in each metrical level for all measures in piece
                self.onsets[self.levels[k]-1] += sum([measure[k] == 1
                                                      for measure in piece['measures']])

        # get rate instead of absolute quantity
        self.ratios = [self.onsets[i]/(self.len_measures * self.levels.count(i+1))
                       for i in range(len(self.onsets))]



    def description_length(self):
        """Compute description length
        """

        # if not default precision then compute the optimal
        # discrete value of the parameters given the precision
        if not self.default_precision:
            # for each parameter
            for ind in range(len(self.ratios)):
                self.ratios[ind] = util.optimal_value(self.d, self.ratios[ind],
                                                      self.len_measures * self.levels.count(ind+1),
                                                      self.onsets[ind])

        # dataset description length
        dataset_dl = - (self.len_measures *
                        sum([self.ratios[x-1]*util.log2(self.ratios[x-1]) +
                             (1-self.ratios[x-1])*util.log2(1-self.ratios[x-1])
                             for x in self.levels]))

        # model description length
        model_dl = (len(self.ratios) + 1) * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self, colwidth=50):
        """Show model parameters
        """

        super().show(colwidth=colwidth)

        print("Model parameters".center(colwidth))
        print()
        print("Onsets per level: ".ljust(colwidth))
        print((str(self.onsets)).rjust(colwidth))
        print("Onset ratios: ".ljust(colwidth))
        print((str(self.ratios)).rjust(colwidth))



class RefinedPosition(Model):
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

    def __init__(self, dataset, signature, beat_subdivisions, d=None):
        super().__init__(dataset, signature, beat_subdivisions, d=d)


    def fit(self, dataset):
        """Fit model parameters from dataset
        
        Parameters
        ----------
        dataset : list of dictionaries
            list containing the encoded pieces from the dataset to fit
        
        """

        super().fit(dataset)

        # number of onsets on each metrical position
        self.onsets = self.beats_measure*[0]
        for piece in dataset:
            for k in range(self.beats_measure):
                # sum onsets in each metrical position for all measures in piece
                self.onsets[k] += sum([measure[k] == 1 for measure in piece['measures']])

        # get rate instead of absolute quantity
        self.ratios = [i/self.len_measures for i in self.onsets]



    def description_length(self):
        """Compute description length
        """

        # if not default precision then compute the optimal
        # discrete value of the parameters given the precision
        if not self.default_precision:
            # for each parameter
            for ind in range(len(self.ratios)):
                self.ratios[ind] = util.optimal_value(self.d, self.ratios[ind],
                                                      self.len_measures,
                                                      self.onsets[ind])

        # dataset description length
        dataset_dl = - (self.len_measures *
                        sum([x*util.log2(x) + (1-x)*util.log2(1-x) for x in self.ratios]))
        # model description length
        model_dl = (self.beats_measure +1)*np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self, colwidth=80):
        """Show model parameters
        """

        super().show(colwidth=colwidth)

        print("Model parameters".center(colwidth))
        print()
        print("Onsets per position: ".ljust(colwidth))
        print((str(self.onsets)).rjust(colwidth))
        print("Onset ratios: ".ljust(colwidth))
        print((str(self.ratios)).rjust(colwidth))



class Hierarchical(Model):
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
        super().__init__(dataset, signature, beat_subdivisions, d=d)


    def fit(self, dataset):
        """Fit model parameters from dataset

        Parameters
        ----------
        dataset : list of dictionaries
            list containing the encoded pieces from the dataset to fit
        
        """

        super().fit(dataset)

        # number of onsets of each anchor type, and downbeat
        self.onsets = {'pre': (self.levels[0] -1)*[0],
                       'pos': (self.levels[0] -1)*[0],
                       'un': (self.levels[0] -1)*[0],
                       'bi': (self.levels[0] -1)*[0],
                       'db': [0]}

        # number of instances of each anchor type, and downbeat
        self.anchors = {'pre': (self.levels[0] -1)*[0],
                        'pos': (self.levels[0] -1)*[0],
                        'un': (self.levels[0] -1)*[0],
                        'bi': (self.levels[0] -1)*[0],
                        'db': [0]}

        # save location of previous and next neighbour
        neighbours = self.beats_measure*[[0, 0]]
        for ind in range(self.beats_measure):
            if ind == 0:
                # first level has no neighbours
                neighbours[ind] = [-1, -1]
            elif ind == self.levels.index(self.levels[0]-1):
                # second level has only one neighbour in the measure (and another in next measure)
                neighbours[ind] = [0, self.beats_measure]
            else:
                # for the rest find the position of the nearest neighbours
                ind_dist = np.where(np.array(self.levels[ind::-1]) > self.levels[ind])
                ind_back = ind - ind_dist[0][0]
                ind_next = ind + ind_dist[0][0]
                neighbours[ind] = [ind_back, ind_next]

        for piece in dataset:
            # for each measure in piece
            for ind_m in range(len(piece['measures'])):
                # current measure
                measure = piece['measures'][ind_m]
                # extend the current measure to include next downbeat
                # check if measure is the last one
                if ind_m == len(piece['measures']) -1:
                    # extend with an empty measure
                    measure = np.append(measure, 0)
                else:
                    next_measure = piece['measures'][ind_m+1]
                    measure = np.append(measure, next_measure[0])
                # for each position in measure
                # first position, no anchor type
                self.anchors['db'][0] += 1
                is_onset = measure[0] == 1
                if is_onset:
                    self.onsets['db'][0] += 1
                for pos in range(1, self.beats_measure):
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
                        self.anchors['un'][self.levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['un'][self.levels[pos]-1] += 1
                    # bi-anchored location
                    if ons_neigh == [1, 1]:
                        self.anchors['bi'][self.levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['bi'][self.levels[pos]-1] += 1
                    # pre-anchored location
                    if ons_neigh == [1, 0]:
                        self.anchors['pre'][self.levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['pre'][self.levels[pos]-1] += 1
                    # pos-anchored location
                    if ons_neigh == [0, 1]:
                        self.anchors['pos'][self.levels[pos]-1] += 1
                        if is_onset:
                            self.onsets['pos'][self.levels[pos]-1] += 1


        # get rates instead of absolute quantity
        # inicialization
        self.ratios = {'pre': (self.levels[0] -1)*[0],
                       'pos': (self.levels[0] -1)*[0],
                       'un': (self.levels[0] -1)*[0],
                       'bi': (self.levels[0] -1)*[0],
                       'db': [0]}
        # get rates for lower levels
        for lev in range(self.levels[0] -1):
            # check if number of anchors is not zero for each anchor type
            # pre-anchored location
            if self.anchors['pre'][lev] != 0:
                #calculate ratio
                self.ratios['pre'][lev] = self.onsets['pre'][lev]/self.anchors['pre'][lev]
            # post-anchored location
            if self.anchors['pos'][lev] != 0:
                #calculate ratio
                self.ratios['pos'][lev] = self.onsets['pos'][lev]/self.anchors['pos'][lev]
            # un-anchored location
            if self.anchors['un'][lev] != 0:
                #calculate ratio
                self.ratios['un'][lev] = self.onsets['un'][lev]/self.anchors['un'][lev]
            # bi-anchored location
            if self.anchors['bi'][lev] != 0:
                #calculate ratio
                self.ratios['bi'][lev] = self.onsets['bi'][lev]/self.anchors['bi'][lev]
        # get rates for highest level
        # check if number of anchors is not zero
        if self.anchors['db'][0] != 0:
            self.ratios['db'][0] = self.onsets['db'][0]/self.anchors['db'][0]
        #self.ratios = [self.onsets[i]/(self.len_measures * self.levels.count(i+1))
        #               for i in range(len(self.onsets))]



    def description_length(self):
        """Compute description length
        """

        # if not default precision then compute the optimal
        # discrete value of the parameters given the precision
        if not self.default_precision:
            # for each parameter
            for key in self.ratios:
                for ind, e in enumerate(self.ratios[key]):
                    self.ratios[key][ind] = util.optimal_value(self.d,
                                                               self.ratios[key][ind],
                                                               self.anchors[key][ind],
                                                               self.onsets[key][ind])

        # initialization
        dataset_dl = 0
        # number of model parameters
        num_el = 0
        # dataset description length
        for key in self.ratios:
            for ind, e in enumerate(self.ratios[key]):
                num_el += 1
                dataset_dl += - self.anchors[key][ind] * (e * util.log2(e) +
                                                          (1-e) * util.log2(1-e))

        # model description length
        model_dl = (num_el + 1) * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self, colwidth=80):
        """Show model parameters
        """

        super().show(colwidth=colwidth)

        print("Model parameters".center(colwidth))
        print()
        print("Locations per anchor type and level: ".ljust(colwidth))
        for k, v in self.anchors.items():
            print((str(v) + ": " + "{:3s}".format(str(k))).rjust(colwidth))
        print("Onsets per anchor type and level: ".ljust(colwidth))
        for k, v in self.onsets.items():
            print((str(v) + ": " + "{:3s}".format(str(k))).rjust(colwidth))
        print("Ratios per anchor type and level: ".ljust(colwidth))
        for k, v in self.ratios.items():
            print((str(v) + ": " + "{:3s}".format(str(k))).rjust(colwidth))




class RefinedHierarchical(Model):
    """Class to represent a Refined Hierarchical model


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
        super().__init__(dataset, signature, beat_subdivisions, d=d)


    def fit(self, dataset):
        """Fit model parameters from dataset
        
        Parameters
        ----------
        dataset : list of dictionaries
            list containing the encoded pieces from the dataset to fit
        
        """

        super().fit(dataset)

        # number of onsets of each anchor type, and downbeat
        self.onsets = {'pre': (self.beats_measure -1)*[0],
                       'pos': (self.beats_measure -1)*[0],
                       'un': (self.beats_measure -1)*[0],
                       'bi': (self.beats_measure -1)*[0],
                       'db': [0]}

        # number of instances of each anchor type, and downbeat
        self.anchors = {'pre': (self.beats_measure -1)*[0],
                        'pos': (self.beats_measure -1)*[0],
                        'un': (self.beats_measure -1)*[0],
                        'bi': (self.beats_measure -1)*[0],
                        'db': [0]}

        # save location of previous and next neighbour
        neighbours = self.beats_measure*[[0, 0]]
        for ind in range(self.beats_measure):
            if ind == 0:
                # first level has no neighbours
                neighbours[ind] = [-1, -1]
            elif ind == self.levels.index(self.levels[0]-1):
                # second level has only one neighbour in the measure (and another in next measure)
                neighbours[ind] = [0, self.beats_measure]
            else:
                # for the rest find the position of the nearest neighbours
                ind_dist = np.where(np.array(self.levels[ind::-1]) > self.levels[ind])
                ind_back = ind - ind_dist[0][0]
                ind_next = ind + ind_dist[0][0]
                neighbours[ind] = [ind_back, ind_next]

        for piece in dataset:
            # for each measure in piece
            for ind_m in range(len(piece['measures'])):
                # current measure
                measure = piece['measures'][ind_m]
                # extend the current measure to include next downbeat
                # check if measure is the last one
                if ind_m == len(piece['measures']) -1:
                    # extend with an empty measure
                    measure = np.append(measure, 0)
                else:
                    next_measure = piece['measures'][ind_m+1]
                    measure = np.append(measure, next_measure[0])
                # for each position in measure
                # first position, no anchor type
                self.anchors['db'][0] += 1
                is_onset = measure[0] == 1
                if is_onset:
                    self.onsets['db'][0] += 1
                for pos in range(1, self.beats_measure):
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
                        self.anchors['un'][pos - 1] += 1
                        if is_onset:
                            self.onsets['un'][pos - 1] += 1
                    # bi-anchored location
                    if ons_neigh == [1, 1]:
                        self.anchors['bi'][pos - 1] += 1
                        if is_onset:
                            self.onsets['bi'][pos - 1] += 1
                    # pre-anchored location
                    if ons_neigh == [1, 0]:
                        self.anchors['pre'][pos - 1] += 1
                        if is_onset:
                            self.onsets['pre'][pos - 1] += 1
                    # pos-anchored location
                    if ons_neigh == [0, 1]:
                        self.anchors['pos'][pos - 1] += 1
                        if is_onset:
                            self.onsets['pos'][pos - 1] += 1

        # get rates instead of absolute quantity
        # inicialization
        self.ratios = {'pre': (self.beats_measure -1)*[0],
                       'pos': (self.beats_measure -1)*[0],
                       'un': (self.beats_measure -1)*[0],
                       'bi': (self.beats_measure -1)*[0],
                       'db': [0]}
        # get rates for lower levels
        for pos in range(1, self.beats_measure):
            # check if number of anchors is not zero for each anchor type
            # pre-anchored location
            if self.anchors['pre'][pos - 1] != 0:
                #calculate ratio
                self.ratios['pre'][pos - 1] = self.onsets['pre'][pos - 1]/self.anchors['pre'][pos - 1]
            # post-anchored location
            if self.anchors['pos'][pos - 1] != 0:
                #calculate ratio
                self.ratios['pos'][pos - 1] = self.onsets['pos'][pos - 1]/self.anchors['pos'][pos - 1]
            # un-anchored location
            if self.anchors['un'][pos - 1] != 0:
                #calculate ratio
                self.ratios['un'][pos - 1] = self.onsets['un'][pos - 1]/self.anchors['un'][pos - 1]
            # bi-anchored location
            if self.anchors['bi'][pos - 1] != 0:
                #calculate ratio
                self.ratios['bi'][pos - 1] = self.onsets['bi'][pos - 1]/self.anchors['bi'][pos - 1]
        # get rates for highest level
        # check if number of anchors is not zero
        if self.anchors['db'][0] != 0:
            self.ratios['db'][0] = self.onsets['db'][0]/self.anchors['db'][0]
        #self.ratios = [self.onsets[i]/(self.len_measures * self.levels.count(i+1))
        #               for i in range(len(self.onsets))]



    def description_length(self):
        """Compute description length
        """

        # if not default precision then compute the optimal
        # discrete value of the parameters given the precision
        if not self.default_precision:
            # for each parameter
            for key in self.ratios:
                for ind, e in enumerate(self.ratios[key]):
                    self.ratios[key][ind] = util.optimal_value(self.d,
                                                               self.ratios[key][ind],
                                                               self.anchors[key][ind],
                                                               self.onsets[key][ind])

        # initialization
        dataset_dl = 0
        # number of model parameters
        num_el = 0
        # dataset description length
        for key in self.ratios:
            for ind, e in enumerate(self.ratios[key]):
                num_el += 1
                dataset_dl += - self.anchors[key][ind] * (e * util.log2(e) +
                                                          (1-e) * util.log2(1-e))

        # model description length
        model_dl = (num_el + 1) * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) / self.len_measures


    def show(self, colwidth=80):
        """Show model parameters
        """

        super().show(colwidth=colwidth)

        print("Model parameters".center(colwidth))
        print()
        print("Locations per anchor type and level: ".ljust(colwidth))
        for k, v in self.anchors.items():
            print((str(v) + ": " + "{:3s}".format(str(k))).rjust(colwidth))
        print("Onsets per anchor type and level: ".ljust(colwidth))
        for k, v in self.onsets.items():
            print((str(v) + ": " + "{:3s}".format(str(k))).rjust(colwidth))
        print("Ratios per anchor type and level: ".ljust(colwidth))
        for k, v in self.ratios.items():
            print((str(v) + ": " + "{:3s}".format(str(k))).rjust(colwidth))
