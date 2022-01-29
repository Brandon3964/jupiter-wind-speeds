from zonalwind import *
import shutil
from astropy.io import fits
path2data = './new_201904/'
path2advected = './advected_data/'
images = glob.glob(path2advected + '*.fits')
# hdul = fits.open(path2fits) 
# print(hdul[0].header['TIME-OBS'])
# print(hdul[0].header['DATE-OBS'])
# for item in images:
#     shutil.copy(item, path2advected)

# copied_image = glob.glob(path2advected + '*.fits')
# copied_image.remove('./advected_data/190409_631_1639_reg_trim.fits')
advected_target = './new_201904/190409_631_1639_reg_trim.fits'
for file in images:


    hdul = fits.open(file)
    temp = hdul[0].data
    result_lon = []



    file1 = open('./full_201904_result.txt', 'r')
    count = 0
# for other_img in copied_image:
    for line in file1:
        count += 1
        temp2 = (line.strip()).split()
        y = geographic2pixel(advected_target, 0, float(temp2[0]))
        result_lon.append(advection(file, advected_target, y[1], float(temp2[1]))[0])

    advected_rows = []
    full_deg = []
    start = 0
    while start < 360:
        full_deg.append(round(start, 1))
        start += 0.05

    for item in range(0, len(result_lon)):
        advected_rows.append(np.interp(full_deg, result_lon[item], temp[item], left = np.nan, right = np.nan))
    hdul[0].data = advected_rows
    hdul.writeto(file,overwrite=True)
    file1.close()
    hdul.close()
print("done")

# test_target = './advected_data/190409_631_0833_reg_trim.fits'

# result_lon = []

# file1 = open('./full_201904_result.txt', 'r')
# count = 0

# for line in file1:
#     count += 1
#     temp2 = (line.strip()).split()
#     y = geographic2pixel(test_target, 0, float(temp2[0]))
#     result_lon.append(advection(test_target, advected_target, y[1], float(temp2[1]))[0])

# advected_rows = []
# full_deg = []
# start = 0
# while start < 360:
#     full_deg.append(round(start, 1))
#     start += 0.05


# hdul = fits.open(test_target)
# temp = hdul[0].data
# for item in range(0, len(result_lon)):
#     advected_rows.append(np.interp(full_deg, result_lon[item], temp[item], left = np.nan, right = np.nan))
# file1.close()
# hdul[0].data = advected_rows
# hdul.writeto(test_target,overwrite=True)

# hdul.close()


