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

import numpy as np

__all__ = ['Bernoulli']


class Bernoulli:
    """Class to represent a Bernoulli model

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


    def description_length(self):
        """Compute description length
        """

        # dataset description length
        dataset_dl = - (self.n1 * np.log2(self.p) + (self.n - self.n1) * np.log2(1-self.p))
        # model description length
        model_dl = 2 * np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl) * (self.beats_measure / self.n)


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
class RefinedPosition:
    """Class to represent a Refined Position model

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
                self.onsets[k] += sum( [measure[k] == 1 for measure in piece['measures'] ] )

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
        dataset_dl = - ( self.len_measures*sum([x*np.log2(x) + (1-x)*np.log2(1-x) for x in self.ratios ])) 
        # model description length
        model_dl = (self.beats_measure +1)*np.log2(self.d)

        # total description length per measure
        self.dl = (dataset_dl + model_dl)/self.len_measures


    def show(self):
        """Show model parameters
        """

        print("Refined Position model. ")
        print("Dataset Parameters")
        print("number of pieces: %d, number of beats per measure: %d, number of measures: %d" % (self.num_pieces,
                                                                         self.beats_measure, self.len_measures))
        print("Model Parameters")
        print("Onsets per position: %s, total number of beats: %d, ratios: %s" % (str(self.onsets), self.n,
                                                                               str(self.ratios)))
        print("Description length")
        print("description length per measure (bits): %f" % self.dl)

######