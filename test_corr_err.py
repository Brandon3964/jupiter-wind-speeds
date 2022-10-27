
from zonalwind import *
start_time = time()
ray.init()

#This is the path to the data
path2data = './201904/'

# This is the path to where you want to store the result




#Get an array of latitudes from -70 to 70 degrees in increments of +0.05 to refer to when printing out latitudes below.
images = glob.glob(path2data + '*.fits')
image1 = images[0]
hdulist = fits.open(image1) 
lat_bot, lat_top, lat_step = hdulist[0].header['LAT_BOT'], hdulist[0].header['LAT_TOP'], hdulist[0].header['LAT_STEP']
latitude = np.linspace(lat_bot, lat_top, int((lat_top - lat_bot)/lat_step) + 1)



# This sets the latitude range and step the the resulting velocity profile.
lats = []
start = -65
end = 65
step = 0.05

#round the result to 2 decimal for 0.05 to avoid python floating error
lats = np.round(np.arange(start, end, step), 2)
v_corr = np.zeros_like(latitude)*np.nan


# Gets all the ray object for each latitude.
obj_list = []
for lat in lats:

    obj_list.append(v_maxcorr.remote(lat, path2data=path2data, plotting=False, vstep=361))


fwidth = open('./vel_width.txt', 'w')

err = 0.003
#Get the velocity from the ray object
for result in range(len(lats)):
    cur_lat = lats[result]

    f = open('./201904_corr_vel/' + str(cur_lat) + '.txt', 'w')




    result = ray.get(obj_list[result])

    for num in range(len(result[0])):

        tempStr = str(result[0][num]) + " " + str(result[1][num]) + "\n"
        f.write(tempStr)
    f.close()
    
    max_corr_index = np.argmax(result[1])
    max_corr = result[1][max_corr_index]
    max_v = result[0][max_corr_index]
    
    err_corr = max_corr - (err * max_corr)
    

    right_corr = result[1][max_corr_index:]
    for i in range(len(right_corr)):
        if right_corr[i] < err_corr:
            if err_corr - right_corr[i] > prev - err_corr:
                err_index = i - 1
            else:
                err_index = i
            break
        else:
            prev = right_corr[i]
    
    right_vel_width = result[0][max_corr_index + err_index] - max_v


    left_corr = result[1][:max_corr_index]
    for i in range (len(left_corr)):
        if left_corr[len(left_corr) - i - 1] < err_corr:
            if err_corr - left_corr[len(left_corr) - i - 1] > prev - err_corr:
                err_index = len(left_corr) - i
            else:
                err_index = len(left_corr) - i - 1
            break
        else:
            prev = left_corr[len(left_corr) - i - 1]        

    left_vel_width = max_v - result[0][err_index]

    avg_width = (right_vel_width + left_vel_width) / 2
    fwidth.write(str(cur_lat) + " " + str(avg_width) + "\n")

fwidth.close()
end = time()


#Plot results along with currently accepted ZWP to compare. 
# path2wp = path2data + 'ZWP_j2016_PJ03.txt'
# lat_zwp, zwp = readZWP(path2wp) 
# fig, axs = plt.subplots(1, 1,figsize=(8,4))
# axs.plot(zwp,lat_zwp,label='JT - ZWP')
# axs.plot(v_corr,latitude,label='DP')
# axs.set_ylabel('Latitude (deg)')
# axs.set_xlabel('Velocity (m/s)')
# axs.set_ylim([-70,70])
# plt.show()

ray.shutdown()
