
"""
dataio.py includes helper functions to saves and load a pickle file. 

savedata(obj, file) accepts any python object - obj and file name. 
It pickles the object.ArithmeticError

loaddata(file) reloads the file and return the pickled object.

"""

import pickle


def savedata(obj, file):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)
   
def loaddata(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    print("Data: {0}".format(data))    
    return data    




    
    