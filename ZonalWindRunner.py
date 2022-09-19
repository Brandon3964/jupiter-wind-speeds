from zonalwind import *
start_time = time()
ray.init()

#This is the path to the data
path2data = './202009/flipped_normal/'

# This is the path to where you want to store the result
path2Result = './test_custom_flip.txt'

f = open(path2Result, 'w')



#Get an array of latitudes from -70 to 70 degrees in increments of +0.05 to refer to when printing out latitudes below.
images = glob.glob(path2data + '*.fits')
image1 = images[0]
hdulist = fits.open(image1) 
lat_bot, lat_top, lat_step = hdulist[0].header['LAT_BOT'], hdulist[0].header['LAT_TOP'], hdulist[0].header['LAT_STEP']
latitude = np.linspace(lat_bot, lat_top, int((lat_top - lat_bot)/lat_step) + 1)



# This sets the latitude range and step the the resulting velocity profile.
lats = []
start = 25
end = 26
step = 0.05

#round the result to 2 decimal for 0.05 to avoid python floating error
lats = np.round(np.arange(start, end, step), 2)
v_corr = np.zeros_like(latitude)*np.nan


# Gets all the ray object for each latitude.
obj_list = []
for lat in lats:
    try:
        obj_list.append(v_maxcorr.remote(lat, path2data=path2data, plotting=False, vstep=361))
    except:
        f.write("error at " + str(lat))


f.write("#Latitude Velocity\n")

#Get the velocity from the ray object
for result in range(len(lats)):
    cur_lat = lats[result]
    try:
        result_v = ray.get(obj_list[result])
        tempStr = str(cur_lat) + " " + str(result_v) + "\n"
        f.write(tempStr)
        print(tempStr)
        #v_corr[np.where(cur_lat == np.around(latitude,2))] = result_v 
    except:
        f.write("error at " + str(cur_lat))





end = time()
f.write("#program Runtime" + str(end - start_time))
f.close()
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

