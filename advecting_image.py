from zonalwind import *

from astropy.io import fits

def inputSortHelper(full_deg, LonList, bright, mask = False):
    cover = np.nan
    if mask:
        cover = 0
    Neg = []
    for i in range(len(LonList)):
        if LonList[i] < 0:
            Neg = LonList[i:]
            Pos = LonList[:i]
            brightNeg = bright[i:]
            brightPos = bright[:i]
            break

    if Neg.size == 0:
        return np.interp(full_deg, LonList[::-1] , bright, left = cover, right = cover)[::-1]
    else:
        print(Neg)
        print(Pos)
        temp1 = np.interp(full_deg, Pos[::-1] , brightPos, left = cover, right = cover)[::-1]
        Neg = np.mod(Neg, 360)
        temp2 = np.interp(full_deg, Neg[::-1] , brightNeg, left = cover, right = cover)[::-1]
        return temp1.append(temp2)



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
    mask = hdul[1].data
    result_lon = []



    file1 = open('./full_201904_result.txt', 'r')
    velocity_tuple = []
    
    velocity_tuple = []
    for line in file1:
        temp2 = (line.strip()).split()
        velocity_tuple.append((float(temp2[0]), float(temp2[1])))

    velocity_tuple.reverse()

    for pair in velocity_tuple:
        y = geographic2pixel(advected_target, 0, pair[0])
        result_lon.append(advection(file, advected_target, y[1], pair[1])[0])

    for item in range(0, len(result_lon)):
        print(result_lon[item])





#     # for line in file1:
#     #     temp2 = (line.strip()).split()
#     #     y = geographic2pixel(advected_target, 0, float(temp2[0]))
#     #     result_lon.append(advection(file, advected_target, y[1], float(temp2[1]))[0])

#     advected_rows = []
#     advected_mask = []
#     full_deg = []
#     start = 360
#     while start > 0:
#         start = round(start, 2)
#         full_deg.append(start)
#         start -= 0.05

#     for item in range(0, len(result_lon)):


#         advected_rows.append(inputSortHelper(full_deg, result_lon[item], temp[item], False))

#         advected_mask.append(inputSortHelper(full_deg, result_lon[item], mask[item], True))

#     advected_rows = np.asarray(advected_rows)
#     advected_mask = np.asarray(advected_mask)

#     advected_rows = np.hstack((advected_rows, advected_rows[:,-1:]))
#     advected_mask = np.hstack((advected_mask, advected_mask[:,-1:]))
    


#     hdul[0].data = advected_rows
#     hdul[1].data = advected_mask
#     hdul[0].header['LON_LEFT'] = 360
#     hdul[0].header['LON_RIGH'] =0
#     hdul[0].header['LAT_TOP'] = 65
#     hdul[0].header['LAT_BOT'] = -65
#     hdul[0].header['NAXSI1'] = 2601
#     hdul[0].header['NAXSI2'] =7201


#     hdul.writeto(file,overwrite=True)
#     file1.close()
#     hdul.close()
# print("done")


# bright = fits.open("./new_201904/190409_631_0833_reg_trim.fits")[0].data[1400]
# lon = np.arange(-30, 50.05, 0.05)
# lon[lon>0] = 360 - lon[lon>0]

# inputSortHelper(np.arange(360, 0, 0.05), lon, bright)







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
# 


