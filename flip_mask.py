from zonalwind import *
import os
from astropy.io import fits

path2data = './202008_OPALj2020a/'

for file in os.listdir(path2data):
    name = file
    file = path2data + file
    
    print(file)
    hdul = fits.open(file)

    mask = hdul[1].data

    new_mask = []

    for item in mask:
        new_mask.append((item - 1) * -1)

    new_mask = np.asarray(new_mask)

    hdul[1].data = new_mask

    hdul.writeto('./flipped_mask_202008/' + name)
    hdul.close()