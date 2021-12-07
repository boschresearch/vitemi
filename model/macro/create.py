"""
Import specimen border geometry in ABAQUS/CAE.
To be executed with `Run script...` function.
"""

from abaqus import *
from abaqusConstants import *

print("Initializing")
myModel = mdb.Model(name='Model A')

mySketch = myModel.ConstrainedSketch(name='Sketch A', sheetSize=200.0)

# Values in micrometer
print("Reading border coordinates")
execfile("../../data/P8/border_coordinates.txt")

# Values should be in mm therefore /1000
print("Transforming xyCoords")
list_xyCoords = [list(i) for i in xyCoords]
for i in range(len(list_xyCoords)):
    list_xyCoords[i][0] = list_xyCoords[i][0] / 1000.0
    list_xyCoords[i][1] = list_xyCoords[i][1] / 1000.0
xyCoords = tuple(tuple(i) for i in list_xyCoords)

print("Creating Sketch")
for i in range(len(xyCoords) - 1):
    mySketch.Line(point1=xyCoords[i], point2=xyCoords[i + 1])

print("Creating part")
myPart = myModel.Part(name='main_model', dimensionality=THREE_D,
                      type=DEFORMABLE_BODY)

with open("microstructure/sample_thickness.txt", 'r') as fl:
    thickness = float(fl.read()) / 1000.
myPart.BaseSolidExtrude(sketch=mySketch, depth=thickness)

print("Saving mdb")
mdb.saveAs(pathName='main_model')
