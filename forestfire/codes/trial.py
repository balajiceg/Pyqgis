from PyQt4.QtCore import *
from osgeo import *
import numpy as np
ulti_fname="C:/Users/Idiot/Desktop/forestfire/ulti_reach.tif";
ds = gdal.Open(ulti_fname)
gt=ds.GetGeoTransform()
rb=ds.GetRasterBand(1)

mx= 80.06990
my=13.53683

px = int((mx - gt[0]) / gt[1])
py = int((my - gt[3]) / gt[5])

arr= np.array(rb.ReadAsArray())
print arr[px][py]