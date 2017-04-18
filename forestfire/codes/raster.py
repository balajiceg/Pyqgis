from PyQt4.QtCore import *
from osgeo import *
import numpy as np

st_lon=78.15
st_lat=10.80
steps=400


def latlonToPix(mx,my,gt):#gt:geotransform param
    col = int((mx - gt[0]) / gt[1])
    row = int((my - gt[3]) / gt[5])
    return (row,col)


def burncell(i,j,val):
    #print val
    if np.isnan(new[i][j]) :
        new[i][j]=val
        ulti_array[i][j]=no_data
    
    if new[i][j]==-1 or new[i][j]==np.float32(-1):
        print "new less than 0"
        return
        
    if val>=steps:
        print "steps over"
        return
    
    if(i>=imax or i<1 or j>=jmax or j<1):
        print "border"
        return
  
    neigh=np.copy(ulti_array[i-1:i+2,j-1:j+2])
    neigh[1][1]=no_data
    
    if np.unique(neigh).size==1 and np.unique(neigh)[0]==no_data :
        print "all burnt"
        return
   
    
    ####################################
    w=wind_array[i][j].item()
    
    if((w>=316.0) or (w>-0.1 and w<=44.00)):
        neigh[0][1]*=2
    elif(w>44.0 and w<46.0):
        neigh[0][2]*=2
    elif(w>=46.0 and w<=134.0):
        neigh[1][2]*=2
    elif(w>134.0 and w<136.0):
        neigh[2][2]*=2
    elif(w>=136.0 and w<=224.0):
        neigh[2][1]*=2
    elif(w>224.0 and w<226.0):
        neigh[2][0]*=2
    elif(w>=226.0 and w<=314.0):
        neigh[1][0]*=2
    elif(w>314.0 and w<316.0):
        neigh[0][0]*=2

    ####################################
    if neigh.max()<0.0000 :
        print neigh.max()
        return

    indices=np.where(neigh == neigh.max())
    x=indices[0][0]
    y=indices[1][0] 
    burncell((i-1)+x,(j-1)+y,val+1)
    burncell(i,j,val+1)
    print(val,"------------------------------")

####################
####################

wind_fname="C:/Users/Idiot/Desktop/forestfire/windirfinresa.tif";
ulti_fname="C:/Users/Idiot/Desktop/forestfire/ulti_reach.tif";
fileInfo = QFileInfo(wind_fname)
baseName = fileInfo.baseName()
wind = QgsRasterLayer(wind_fname, baseName)
if not wind.isValid():
  print "WindLayer failed to load!"

fileInfo = QFileInfo(ulti_fname)
baseName = fileInfo.baseName()
flayer = QgsRasterLayer(ulti_fname, baseName)
if not flayer.isValid():
  print "UltiLayer failed to load!"


ds = gdal.Open(ulti_fname)
ds1 = gdal.Open(wind_fname)
#Get projection
prj = ds.GetProjection()
#setting band
number_band = 1
#Get raster metadata
geotransform = ds.GetGeoTransform()


ulti = ds.GetRasterBand(number_band)
wind = ds1.GetRasterBand(number_band)
no_data= ulti.GetNoDataValue()


ulti_array = np.array(ulti.ReadAsArray())
wind_array = np.array(wind.ReadAsArray())

no_data=np.float32(no_data)

(burni,burnj)= latlonToPix(st_lon,st_lat,geotransform)
new = np.empty(shape=(ulti.YSize,ulti.XSize),dtype=ulti_array.dtype)
new.fill(None)

neigh=np.empty(shape=(3,3),dtype=ulti_array.dtype)
print ulti_array.dtype

#for i,row in enumerate(ulti_array):
#    for j,cell in enumerate(row):
#        if cell==np.float32(no_data):
#            new[i][j]=-1

for i in range(len(new)):
    for j in range(len(new[0])):
        if ulti_array[i][j]==no_data:
            new[i][j]=-1

imax=ulti.YSize-2
jmax=ulti.XSize-2
burncell(burni,burnj,0)










#########################################
##creating output raster
output_file = "C:/Users/Idiot/Desktop/forestfire/output/trial.tiff"
driver = gdal.GetDriverByName("GTiff")
dst_ds = driver.Create(output_file, 
                       ulti.XSize, 
                       ulti.YSize, 
                       number_band, 
                       ulti.DataType)


#writting output raster
dst_ds.GetRasterBand(number_band).WriteArray( new )
#set no data value
dst_ds.GetRasterBand(number_band).SetNoDataValue(-1)
#setting extension of output raster
# top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
dst_ds.SetGeoTransform(geotransform)
# setting spatial reference of output raster 
srs = osr.SpatialReference(wkt = prj)
dst_ds.SetProjection( srs.ExportToWkt() )
#dst_ds.SetMetadata({'STATISTICS_MAXIMUM':'10.0'});
#dst_ds.SetMetadata({'STATISTICS_MINIMUM':'0.0'});
#dst_ds.SetMetadata('','0');

#Close output raster dataset 
dst_ds = None
#Close main raster dataset
ds= None
#display the output
iface.addRasterLayer("C:/Users/Idiot/Desktop/forestfire/output/trial.tiff", "result")

