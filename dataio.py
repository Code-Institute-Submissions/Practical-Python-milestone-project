import pickle


def savedata(obj, file):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)
   
def loaddata(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    print("Data: {0}".format(data))    
    return data    




    
    