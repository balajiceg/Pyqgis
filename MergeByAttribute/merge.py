#author Idiot
#pipeline
from PyQt4.QtCore import QVariant
from itertools import cycle
from qgis.core import *
from qgis.utils import *
import random

#field name that has to be added when merging
str1='LULC'
#new field name
str2='LULC1'
#field based on which merging will take place
unique_tag='Tag'


layer = iface.activeLayer()
if not layer.isValid():
    print "Layer failed to load!"
    exit(1)
else:
    print  "layer valid"
    
init_index=layer.dataProvider().fieldNameIndex(str2)
init_index1=layer.dataProvider().fieldNameIndex(str1)
unique_idx=layer.dataProvider().fieldNameIndex(unique_tag)
iter = layer.getFeatures()
attrs=[]
grids=[]
features=[]
lulc=[]
for feature in iter:
    att = feature.attributes()
    attrs.append(att)
    #grid column
    grids.append(att[unique_idx])
    features.append(feature)
    lulc.append(att[init_index1])

myset = set(grids)
layer.startEditing()
go=1
for grid in myset:
    indices = [i for i, x in enumerate(grids) if x == grid]
    print go
    print grid
    names=[lulc[x] for x in indices]
    unique_names=set(names)
    name = ",".join(unique_names)
    indices.sort(reverse=True)
    fin=indices.pop()
    layer.changeAttributeValue(features[fin].id(),init_index, name)
    geom=features[fin].geometry()
    for ii in indices:
        geom = geom.combine(features[ii].geometry())
    layer.dataProvider().changeGeometryValues({ features[fin].id() : geom })
    ids=[features[i].id() for i in indices]
    #res = layer.dataProvider().deleteFeatures(ids)
    go=go+1
#    if go == 6:break 
layer.updateFields()
layer.commitChanges()
del layer
layer = iface.activeLayer()
iter = layer.getFeatures()
delete_ids=[]
for feature in iter:
    att = feature.attributes()
#    print att[init_index]
    if not att[init_index] :
        delete_ids.append(feature.id())
layer.startEditing()
res = layer.dataProvider().deleteFeatures(delete_ids)
layer.updateFields()
layer.commitChanges()
