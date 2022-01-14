from zonalwind import *
start_time = time()
ray.init(_node_ip_address="0.0.0.0")
path2data = './new_201904/'





#Get an array of latitudes from -70 to 70 degrees in increments of +0.05 to refer to when printing out latitudes below.
images = glob.glob(path2data + '*.fits')
image1 = images[0]
hdulist = fits.open(image1) 
lat_bot, lat_top, lat_step = hdulist[0].header['LAT_BOT'], hdulist[0].header['LAT_TOP'], hdulist[0].header['LAT_STEP']
latitude = np.linspace(lat_bot, lat_top, int((lat_top - lat_bot)/lat_step) + 1)

# Caveat, this only works if all the images have the same latitude cut off 

#Generate an array of latitudes (pixels) and best velocities (m/s). 

#for lat in latitude:
lats = []
start = -65
while start < 0:
    lats.append(start)
    start += 0.1
v_corr = np.zeros_like(latitude)*np.nan
obj_list = []
for lat in lats:
    try:
        obj_list.append(v_maxcorr.remote(lat, path2data=path2data, plotting=False, vstep=361))
    except:
        print("error at ", lat)

print("Latitude", " Velocity")
for result in range(len(lats)):
    cur_lat = lats[result]
    result_v = ray.get(obj_list[result])
    print(cur_lat, " ", result_v)
    v_corr[np.where(cur_lat == np.around(latitude,2))] = result_v 



end = time()
print("Program Runtime ", end - start_time)
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

