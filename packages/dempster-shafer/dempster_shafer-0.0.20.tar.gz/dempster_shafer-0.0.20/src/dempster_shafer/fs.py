"""
.. module:: FocalSet
    :platform: Unix, Windows
    :synopsis: A useful module indeed.

.. moduleauthor:: Noelia Rico <noeliarico@uniovi.es>

"""

import numpy as np

class FocalSet:
    
    """Class for representing the focal sets associated to a frame of discerment.
    """

    def __init__(self, fod, bpa, fe = None):
        """Focal set class

        :param fod: FrameOfDiscernment for which the focal set is defined
        :type fod: FrameOfDiscernment
        :param bpa: This parameter can be given using two different types:
            1) dict: associating each subsest with the basic probability assigments
            2) ndarray: if this type is used then the  giving the indexes of the e
        :type bpa: dict, np.array
        """     
        
        # self.bpas is a dictionary containing the elements and it assigned bpa
        
        #TODO if bpa is dict y fe is not None 
        
        if fod == None:
            raise ValueError("The focal set must be associated with a frame of discernment.")
        else:
            self.fod = fod
        
        # Type of bpa
        if isinstance(bpa,(list,np.ndarray)):
            if not isinstance(fe, (list,np.ndarray)):
                raise ValueError("If bpa is a list, the set of focal element must be algo given using 'fe'")
            
            # Check that there are not repeated focal elements
            r = np.unique(fe, return_counts=True)[1]
            if np.any(r > 1):
                raise ValueError("There cannot be repeated focal elements.")
            
            # Check the distance of both is equal
            if len(bpa) != len(fe):
                raise ValueError("There must be exactly one bpa value to each focal element")
            
            # TODO check that fe sum 1
            # TODO if fe are integeres then are Indexes
            # TODO if bpa are strings then check if are subsets and translate
            
            
            # Create the dictionary
            self.bpas = dict(zip(fe, bpa))
            
        elif isinstance(bpa,(dict)):
            # Ensure that the sum of the probabilities is 1
            self.bpas = bpa
            
        else:
            raise TypeError("Invalid type, bpa must be a list or a dictionary")
        
    def as_arrays(self):
        """Returns the dictionary representing the focal set as two numpy
        arrays, one with the indexes of the focal elements and another one
        with the values.

        :return: tuple with two numpy arrays, one for the indexes of the
            focal elements and another for their corresponding bpa value
        :rtype: tuple(np.ndarray, np.ndarray)
        """
        return (np.array(list(self.bpas.keys())), np.array(list(self.bpas.values())))

        
    def __checkSubsets(self):
        """Check that all the subsets belong to the FrameOfDiscernment.
        
        This method should not be used by the user. It is used internally
        when the Focal set is initiallized and ensures that every element
        of the focal set is a subset of the items in the frame of discernment.
        """
        
    def get_bpa(self, subset):
        
        if isinstance(subset, (str)):
            return self.fes.get(subset)
        elif isinstance(subset, (int)):
            return self.fes.values()[subset]
        else:
            raise TypeError("subset must be a string representing a subset or an index.")
    
    def __repr__(self):
        return "Items {} \nFocal set {} \n".format(self.fod.items, self.bpas)
        
    def __str__(self):
        return "Items {} \nFocal set {} \n".format(self.fod.items, self.bpas)