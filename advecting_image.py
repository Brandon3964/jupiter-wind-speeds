from zonalwind import *

from astropy.io import fits


def interpolate_sphere(lon_interp,lon,val,plotting=False, mask = False): 
    # Interpolate onto 360 grid (flip for Jupiter)
    #lon: longitude to be interpolat, val:brightness
    cover = np.nan
    outOfBound = False
    if mask:
        cover = 0

    for i in range(len(lon)):
        if lon[i] < 0:
            outOfBound = True
            break
    if outOfBound:
        # Remove interpolated values outside of input range
        val_interp = np.flipud(np.interp(np.flipud(lon_interp),np.flipud(lon),np.flipud(val),period=360))
        idx_left = np.where(lon_interp > np.mod(np.min(lon),360))[0][-1]
        idx_right = np.where(lon_interp < np.mod(np.max(lon),360))[0][0]
        val_interp[idx_left:idx_right] = np.nan
    else:
        val_interp = np.interp(full_deg, lon , val, left = cover, right = cover)

    return val_interp[::-1]


    #Only for plotting the result
    if plotting:
        plt.figure() 
        plt.plot(lon,val,label='Input')
        plt.plot(lon_interp,val_interp,label='Interpolated onto sphere')
        plt.plot([359,359],[0,100],color='gray',linestyle='--')
        plt.plot([0,0],[0,100],color='gray',linestyle='--')

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





    # for line in file1:
    #     temp2 = (line.strip()).split()
    #     y = geographic2pixel(advected_target, 0, float(temp2[0]))
    #     result_lon.append(advection(file, advected_target, y[1], float(temp2[1]))[0])

    advected_rows = []
    advected_mask = []
    full_deg = []
    start = 360
    while start > 0:
        start = round(start, 2)
        full_deg.append(start)
        start -= 0.05

    for item in range(0, len(result_lon)):


        advected_rows.append(interpolate_sphere(full_deg, result_lon[item][::-1], temp[item], mask = False))

        advected_mask.append(interpolate_sphere(full_deg, result_lon[item][::-1], mask[item], mask = True))

    advected_rows = np.asarray(advected_rows)
    advected_mask = np.asarray(advected_mask)

    advected_rows = np.hstack((advected_rows, advected_rows[:,-1:]))
    advected_mask = np.hstack((advected_mask, advected_mask[:,-1:]))
    


    hdul[0].data = advected_rows
    hdul[1].data = advected_mask
    hdul[0].header['LON_LEFT'] = 360
    hdul[0].header['LON_RIGH'] =0
    hdul[0].header['LAT_TOP'] = 65
    hdul[0].header['LAT_BOT'] = -65
    hdul[0].header['NAXSI1'] = 2601
    hdul[0].header['NAXSI2'] =7201


    hdul.writeto(file,overwrite=True)
    file1.close()
    hdul.close()
print("done")









