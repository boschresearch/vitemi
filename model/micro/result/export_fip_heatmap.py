"""
Export images of heatmaps for FIP in simulation.
Execute with `Run script...` funtion in ABAQUS/CAE.
"""

from abaqusConstants import *
from abaqus import *

# Parameters to define
# --------------------
# Path to ABAQUS result file
odb_path = '/gpfs3/scratch/user/nae2rng/simulation_212/PRJ03_Substructure_IWM/P8_Full/P8_SmSt_856x500x10/result/RVE.odb'
# Map of FIP names to SDV names
fip_names = {"FIP_P": 'SDV26', "FIP_FS": "SDV27", "FIP_W": "SDV88"}
# Exclude elastic embedding
element_sets_to_exclude = ("RVE_1.G_959", )

o1 = session.openOdb(name=odb_path)
vp = session.viewports['Viewport: 1']
vp.setValues(displayedObject=o1)
vp.odbDisplay.commonOptions.setValues(visibleEdges=FREE)

vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_UNDEF,))
vp.view.setValues(session.views['Back'])
vp.viewportAnnotationOptions.setValues(
    triad=OFF,
    legend=OFF,
    title=OFF,
    state=OFF,
    annotations=OFF,
    compass=OFF)
    
leaf = dgo.LeafFromElementSets(elementSets=element_sets_to_exclude)
vp.odbDisplay.displayGroup.remove(leaf=leaf)

for fn, sdv in fip_names.items():
    vp.odbDisplay.setPrimaryVariable(
        variableLabel=sdv, outputPosition=INTEGRATION_POINT, )
    session.pngOptions.setValues(imageSize=(4096, 1683))
    session.printToFile(fileName=fn, format=PNG, canvasObjects=(vp, ))
