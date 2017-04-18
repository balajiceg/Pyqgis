vlayer = QgsVectorLayer("C:/Users/Idiot/Documents/ArcGIS/tab.dbf", "layer_name_you_like", "ogr")
fea=vlayer.getFeatures()
points = []
for feat in fea:
    attrs = feat.attributes()
    print attrs[1]
    points.append(QgsPoint(attrs[0],attrs[1]))
print points
vectorLyr =  QgsVectorLayer('C:/Users/Idiot/Desktop/pyqgis/line.shp', 'Paths' , "ogr")
QgsMapLayerRegistry.instance().addMapLayers([vectorLyr])
vectorLyr.isValid()
vpr = vectorLyr.dataProvider()
line = QgsGeometry.fromPolyline(points)
f = QgsFeature()
f.setGeometry(line)
vpr.addFeatures([f])
vectorLyr.updateExtents()