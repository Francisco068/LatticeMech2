import numpy as np

def rotate_vector(vector, angle):
    """ Rotate a vector according to an angle (rad)"""
    vect1=np.array([[np.cos(angle),-np.sin(angle)],
            [np.sin(angle),np.cos(angle)]])
    vect2=np.matmul(vect1,vector)
    return vect2

def normalize_vector(vector):
    """return vector normalised"""
    vect1=vector/np.linalg.norm(vector)
    return vect1
