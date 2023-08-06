# FUNCTIONS FOR SAVING, CREATING, LOADING DATA AND MODELS

import os
import functools
import pickle


def load_or_make(creator):
    """
    Loads data that is pickled at filepath if filepath exists;
    otherwise, calls creator(*args, **kwargs) to create the data 
    and pickle it at filepath.
    Returns the data in either case.
    
    Inputs:
    - filepath: path to where data is / should be stored
    - creator: function to create data if it is not already pickled
    - *args, **kwargs: arguments passed to creator()
    
    Outputs:
    - item: the data that is stored at filepath
    """
    @functools.wraps(creator)
    def cached_creator(filepath, update=False, *args, **kwargs):
        if os.path.isfile(filepath) and not update:
            with open(filepath, 'rb') as pkl:
                item = pickle.load(pkl)
        else:
            item = creator(*args, **kwargs)
            with open(filepath, 'wb') as pkl:
                pickle.dump(item, pkl)
        return item
    return cached_creator