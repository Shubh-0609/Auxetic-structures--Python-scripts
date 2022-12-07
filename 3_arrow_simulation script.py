Mdb()
from abaqus import *
from abaqusConstants import *
from assembly import *
from connectorBehavior import *
from interaction import *
from job import *
from load import *
from material import *
from mesh import *
from odbAccess import *
from part import *
from section import *
from sketch import *
from step import *
from visualization import *
from viewerModules import *
from decimal import *
from operator import *
from string import *
from numpy import *
import datetime
import math
import mesh
import meshEdit
import os
import random
import shutil
import time
import numpy as np
import visualization


JobName ='DisY' 
ModelName ='3_arrow' 
PathName =str(os.getcwd())
E_Module  = 193000.0000
Poisson_R = 0.330000
Den = 8.36e9
Conduct=230
Spec_Heat=380000000
Expan_co=2e-5
epsilon=0.01
Strain_Y=0.05
platethick=2
Seedsize=0.5
loadTime=2
Massscal=1000000.0
numIntervals=20


#               Name change
mdb.models.changeKey(fromName='Model-1', toName='3_arrow')

#            part generation

# Arrow-1
parameter=np.load('parameter.npy',)
arrow_1=np.load('arrow_1.npy')

h,l,theta,thick1,thick2,stars=parameter
s = mdb.models['3_arrow'].ConstrainedSketch(name='Arrow1', 
sheetSize=200.0)
phi=math.pi/stars
rotx=((h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta))-thick2)/math.tan(phi*0.5)
roty=(h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta))-thick2

g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
x=arrow_1[:,0]
y=arrow_1[:,1]
z=len(arrow_1)
for i in range(z-1):
    s.Line(point1=(x[i],y[i]),point2=(x[i+1],y[i+1]))
p = mdb.models['3_arrow'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
p = mdb.models['3_arrow'].parts['Part-1']
p.BaseShell(sketch=s)

# Arrow-2
arrow_2=np.load('arrow_2.npy')
s1 = mdb.models['3_arrow'].ConstrainedSketch(name='Arrow2', 
sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
x1=arrow_2[:,0]
y1=arrow_2[:,1]
z1=len(arrow_2)
for i in range(z1-1):
    s1.Line(point1=(x1[i],y1[i]),point2=(x1[i+1],y1[i+1]))
p = mdb.models['3_arrow'].Part(name='Part-2', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
p = mdb.models['3_arrow'].parts['Part-2']
p.BaseShell(sketch=s1)

# Arrow-3
arrow_3=np.load('arrow_3.npy')
s2 = mdb.models['3_arrow'].ConstrainedSketch(name='Arrow3', 
sheetSize=200.0)
g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
s2.setPrimaryObject(option=STANDALONE)
x2=arrow_3[:,0]
y2=arrow_3[:,1]
z=len(arrow_3)
for i in range(z-1):
    s2.Line(point1=(x2[i],y2[i]),point2=(x2[i+1],y2[i+1]))
p = mdb.models['3_arrow'].Part(name='Part-3', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
p = mdb.models['3_arrow'].parts['Part-3']
p.BaseShell(sketch=s2)



    # VIRTUAL POINTS 
Part_VirtPoint_X = mdb.models['3_arrow'].Part(dimensionality=TWO_D_PLANAR, name='VirtPoint_X', type=DEFORMABLE_BODY)
Part_VirtPoint_X.ReferencePoint(point=(((h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta))-thick2)/math.tan(phi*0.5), 
    (h+l*(math.sin(theta)/math.tan(phi)))-thick2, 0.0))

Part_VirtPoint_Y = mdb.models['3_arrow'].Part(dimensionality=TWO_D_PLANAR, name='VirtPoint_Y', type=DEFORMABLE_BODY)
Part_VirtPoint_Y.ReferencePoint(point=(((h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta))-thick2)/math.tan(phi*0.5), 
    (h+l*(math.sin(theta)/math.tan(phi)))-thick2, 0.0))
    
 #               Assembly and instances with merge function  for 3star
a = mdb.models['3_arrow'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['3_arrow'].rootAssembly
p = mdb.models['3_arrow'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=ON)
p = mdb.models['3_arrow'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=ON)
p = mdb.models['3_arrow'].parts['Part-3']
a.Instance(name='Part-3-1', part=p, dependent=ON)

a = mdb.models['3_arrow'].rootAssembly
a.InstanceFromBooleanMerge(name='Arrow_3_Part', instances=(
    a.instances['Part-1-1'], a.instances['Part-2-1'], 
    a.instances['Part-3-1'], ), 
    originalInstances=DELETE,  domain=GEOMETRY)
p = mdb.models['3_arrow'].parts['Arrow_3_Part']


# Assembly and merge funtion for unit cell
a = mdb.models['3_arrow'].rootAssembly
a.RadialInstancePattern(instanceList=('Arrow_3_Part-1', ), point=(rotx, 
    roty, 0.0), axis=(0.0, 0.0, 1.0), number=6, totalAngle=360.0)

Partins=a.InstanceFromBooleanMerge(name='Unit_Cell', instances=(
        a.instances['Arrow_3_Part-1'], a.instances['Arrow_3_Part-1-rad-2'], 
        a.instances['Arrow_3_Part-1-rad-3'], 
        a.instances['Arrow_3_Part-1-rad-4'], 
        a.instances['Arrow_3_Part-1-rad-5'], 
        a.instances['Arrow_3_Part-1-rad-6'], ), originalInstances=DELETE,  domain=GEOMETRY)
a = mdb.models['3_arrow'].rootAssembly

InstVP_X = a.Instance(dependent=ON, name='VirtPointInst_X', part=Part_VirtPoint_X)
InstVP_Y = a.Instance(dependent=ON, name='VirtPointInst_Y', part=Part_VirtPoint_Y)



# Right
s5 = mdb.models['3_arrow'].ConstrainedSketch(name='Arrow', 
sheetSize=200.0)
g, v, d, c = s5.geometry, s5.vertices, s5.dimensions, s5.constraints
s5.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['3_arrow'].parts['Unit_Cell']
s5.rectangle(point1=(2*rotx, -(h+l*(math.sin(theta)/math.tan(phi)))), point2=(2*rotx+((h+l*(math.sin(theta)/math.tan(phi)))+thick2)*math.sin(2*phi), (h+l*(math.sin(theta)/math.tan(phi)))+2*roty))
p.Cut(sketch=s5)
s5.unsetPrimaryObject() 

# Left
s6 = mdb.models['3_arrow'].ConstrainedSketch(name='Arrow', 
sheetSize=200.0)
g, v, d, c = s6.geometry, s6.vertices, s6.dimensions, s6.constraints
s6.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['3_arrow'].parts['Unit_Cell']
s6.rectangle(point1=(0, -(h+l*(math.sin(theta)/math.tan(phi)))), point2=(-((h+l*(math.sin(theta)/math.tan(phi)))+thick2)*math.sin(2*phi), (h+l*(math.sin(theta)/math.tan(phi)))+2*roty))
p.Cut(sketch=s6)
s6.unsetPrimaryObject() 



        


Stepstatic = mdb.models['3_arrow'].StaticStep(description='Uniaxial compression in Y direction',
    name='Step-1', previous='Initial')
Stepstatic.setValues(adaptiveDampingRatio=None, continueDampingFactors=False, nlgeom=OFF,
    matrixSolver=SOLVER_DEFAULT, solutionTechnique=FULL_NEWTON, stabilizationMethod=NONE)
    

    #                Material assignment and section generation
mdb.models['3_arrow'].Material(name='Structure_Material')
mdb.models['3_arrow'].materials['Structure_Material'].Elastic(table=((
193000000000.0000, 0.33), ))
mdb.models['3_arrow'].materials['Structure_Material'].Density(table=((0.00836000, ), 
))
mdb.models['3_arrow'].HomogeneousSolidSection(name='Section_Star', 
material='Structure_Material', thickness=platethick)

    #           SectionAssignment   

p = mdb.models['3_arrow'].parts['Unit_Cell']
p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Region(faces=mdb.models['3_arrow'].parts['Unit_Cell'].faces.getByBoundingBox(-epsilon,-roty-(h+l*(math.sin(theta)/math.tan(phi)))-1,-1,2*rotx+1,3*roty+(h+l*(math.sin(theta)/math.tan(phi)))+1,1)
    ), sectionName='Section_Star', 
    thicknessAssignment=FROM_SECTION)   

#                   Meshing
p = mdb.models['3_arrow'].parts['Unit_Cell']
p.seedPart(size=Seedsize, deviationFactor=0.1, minSizeFactor=0.5)
elemType1 = mesh.ElemType(elemCode=CPS4R, elemLibrary=EXPLICIT, 
    secondOrderAccuracy=ON, hourglassControl=ENHANCED, 
    distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=EXPLICIT,secondOrderAccuracy=ON)
pickedRegions =(p.faces[0], )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED)
# p.setMeshControls(regions=pickedRegions, elemShape=TRI)
p.generateMesh()



# DEFINE SETS CONTAINING ALL NODES AND ELEMENTS 
p.Set(name='All_Elems', elements=p.elements)       # A SET OF ALL ELEMENTS 
p.Set(name='All_Nodes', nodes=p.nodes)             # A SET OF ALL NODES 

p.Set(name='Down_Nodes', nodes=
    p.nodes.getByBoundingBox( rotx-thick2*0.5-epsilon,-roty-(h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta))-epsilon, 0,rotx+thick2*0.5+epsilon, -roty-(h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta))+epsilon, epsilon) )              
p.Set(name='Up_Nodes', nodes=
    p.nodes.getByBoundingBox(rotx-thick2*0.5-epsilon, 3*roty+(h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta)) -epsilon, 0, rotx+thick2*0.5+epsilon, 3*roty+(h+l*(math.sin(theta)/math.tan(phi))- l * math.cos(theta))+epsilon, epsilon) )    

p.Set(name='Left_Nodes', nodes=
    p.nodes.getByBoundingBox( -epsilon,-roty-thick2*0.5-epsilon, 0, epsilon ,3*roty+thick2*0.5+epsilon, epsilon))    
p.Set(name='Right_Nodes', nodes=
    p.nodes.getByBoundingBox( 2*rotx-epsilon,-roty-thick2*0.5-epsilon, 0, 2*rotx+epsilon ,3*roty+thick2*0.5+epsilon, epsilon) )

 # THE MID-NODE OF THE VERTICAL LINE IN THE MIDDLE OF THE RVE IS CONSTRAINED TO PREVENT RIGID BODY MOTION OF THE MODEL
# SINCE THE MESH MIGHT BE VERY FINE, epsilon*epsilon IS USED FOR THE BOUNDARIES OF THE BOX
p.Set(name='LowerMidVert_Line_Nodes', nodes=p.nodes.getByBoundingBox
    (rotx-epsilon, -roty- epsilon, -epsilon, rotx+epsilon, 3*roty + epsilon, epsilon))

Mid_Line_Size = len(p.sets['LowerMidVert_Line_Nodes'].nodes)
Mid_Node_Num = int(Mid_Line_Size/3.0)
Mid_Node_Label = p.sets['LowerMidVert_Line_Nodes'].nodes[Mid_Node_Num].label
p.SetFromNodeLabels(name='Fixed_Node', nodeLabels=(Mid_Node_Label, ))
    
# CREATE SETS FOR VIRTUAL NODES 
Part_VirtPoint_X.Set(name='VPoint_X', referencePoints=(Part_VirtPoint_X.referencePoints[1], ))
Part_VirtPoint_Y.Set(name='VPoint_Y', referencePoints=(Part_VirtPoint_Y.referencePoints[1], ))

                
Model_Arrow=mdb.models['3_arrow']
PartInst_Arrow = Partins
          
# SETS OF PERIODIC NODE PAIRS
# UP AND DOWN 
for i in p.sets['Up_Nodes'].nodes:
	TopCoordinate = i.coordinates
	p.SetFromNodeLabels(name='Up_Node_Pair_' + str(i.label), nodeLabels=(i.label,))
	for j in p.sets['Down_Nodes'].nodes:
		DownCoordinate = j.coordinates
		if (fabs(TopCoordinate[0] - DownCoordinate[0]) < epsilon):
			p.SetFromNodeLabels(name='Down_Node_Pair_' + str(i.label), nodeLabels=(j.label,))
			break
            
            
# LEFT AND RIGHT
for i in p.sets['Right_Nodes'].nodes:
	LeftCoordinate = i.coordinates
	p.SetFromNodeLabels(name='Right_Node_Pair_' + str(i.label), nodeLabels=(i.label,))
	for j in p.sets['Left_Nodes'].nodes:
		RightCoordinate = j.coordinates
		if (fabs(RightCoordinate[1] - LeftCoordinate[1]) < epsilon):
			p.SetFromNodeLabels(name='Left_Node_Pair_' + str(i.label), nodeLabels=(j.label,))
			break
 
# PERIODIC BOUNDARY CONDITIONS 

# RIGHT AND LEFT EDGES
for i in p.sets['Right_Nodes'].nodes:
    
    # COEFFICIENTS PREPARATION
    InDependCoord=p.sets['Left_Node_Pair_' + str(i.label)].nodes[0].coordinates
    DependCoord=p.sets['Right_Node_Pair_' + str(i.label)].nodes[0].coordinates
    
    coeff1=-(DependCoord[0]-InDependCoord[0])
    coeff2=-(DependCoord[1]-InDependCoord[1])
    
    # X-COORDINATE OF DEPENDENT SET
    mdb.models['3_arrow'].Equation(name='LR_Const_at_X_' + str(i.label), terms=(
        ( 1.0, 'Unit_Cell-1.Right_Node_Pair_' + str(i.label), 1), 
        (-1.0, 'Unit_Cell-1.Left_Node_Pair_' + str(i.label), 1), 
        (coeff1, 'VirtPointInst_X.VPoint_X', 1), 
        (coeff2, 'VirtPointInst_Y.VPoint_Y', 1)))
        
    # Y-COORDINATE OF DEPENDENT SET
    mdb.models['3_arrow'].Equation(name='LR_Const_at_Y_' + str(i.label), terms=(
        ( 1.0, 'Unit_Cell-1.Right_Node_Pair_' + str(i.label), 2), 
        (-1.0, 'Unit_Cell-1.Left_Node_Pair_' + str(i.label), 2), 
        (coeff1, 'VirtPointInst_X.VPoint_X', 2), 
        (coeff2, 'VirtPointInst_Y.VPoint_Y', 2)))

# UP AND DOWN EDGES
for i in p.sets['Up_Nodes'].nodes:
    
    # COEFFICIENTS PREPARATION
    InDependCoord=p.sets['Down_Node_Pair_' + str(i.label)].nodes[0].coordinates
    DependCoord=p.sets['Up_Node_Pair_' + str(i.label)].nodes[0].coordinates
    
    coeff1=-(DependCoord[0]-InDependCoord[0])
    coeff2=-(DependCoord[1]-InDependCoord[1])
    
    # X-COORDINATE OF DEPENDENT SET
    mdb.models['3_arrow'].Equation(name='UD_Const_at_X_' + str(i.label), terms=(
        ( 1.0, 'Unit_Cell-1.Up_Node_Pair_' + str(i.label), 1), 
        (-1.0, 'Unit_Cell-1.Down_Node_Pair_' + str(i.label), 1), 
        (coeff1, 'VirtPointInst_X.VPoint_X', 1), 
        (coeff2, 'VirtPointInst_Y.VPoint_Y', 1)))
        
    # Y-COORDINATE OF DEPENDENT SET
    mdb.models['3_arrow'].Equation(name='UD_Const_at_Y_' + str(i.label), terms=(
        ( 1.0, 'Unit_Cell-1.Up_Node_Pair_' + str(i.label), 2), 
        (-1.0, 'Unit_Cell-1.Down_Node_Pair_' + str(i.label), 2), 
        (coeff1, 'VirtPointInst_X.VPoint_X', 2), 
        (coeff2, 'VirtPointInst_Y.VPoint_Y', 2))) 


           
                #BOUNDARY CONDITIONS 
# FIXED NODE
Model_Arrow.DisplacementBC(amplitude=UNSET, createStepName=
    'Step-1', distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'Fixing_RB_Motion', region=PartInst_Arrow.sets['Fixed_Node'] , u1=0.0, u2=0.0, ur3=UNSET)    
    
# APPLIED DISPLACEMENT TO VIRTUAL POINTS 
# X VIRTUAL POINT IS FIXED IN Y DIRECTION
Model_Arrow.DisplacementBC(amplitude=UNSET, createStepName=
    'Step-1', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    localCsys=None, name='VP_X_Fixed_at_Y', region=InstVP_X.sets['VPoint_X']
    , u1=UNSET, u2=0.0, ur3=UNSET)
# Y VIRTUAL POINT MOVES IN Y DIRECTION
Model_Arrow.DisplacementBC(amplitude=UNSET, createStepName=
    'Step-1', distributionType=UNIFORM, fieldName='', fixed=OFF,
    localCsys=None, name='VP_Y_Moves_at_Y', region=InstVP_Y.sets['VPoint_Y']
    , u1=0.0, u2=Strain_Y, ur3=UNSET)
    


icup=4

mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=DOUBLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='3_arrow', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=icup,numDomains=icup, queue=None, scratch='', type=ANALYSIS, userSubroutine='', 
    waitHours=0, waitMinutes=0,resultsFormat=ODB)

time_start=time.time()
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1'].waitForCompletion()

name=''
for i in parameter:
    name=name+str(i)+'-'

o1 = session.openOdb('Job-1' +'.odb')

VP_X = o1.rootAssembly.instances['VIRTPOINTINST_X'].nodeSets['VPOINT_X']
Dis_VP_X = o1.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(region = VP_X).values[0].data[0]

VP_Y = o1.rootAssembly.instances['VIRTPOINTINST_Y'].nodeSets['VPOINT_Y']

Dis_VP_Y = o1.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(region = VP_Y).values[0].data[1]
RF_VP_Y = o1.steps['Step-1'].frames[-1].fieldOutputs['RF'].getSubset(region = VP_Y).values[0].data[1]
RF_VP_X = o1.steps['Step-1'].frames[-1].fieldOutputs['RF'].getSubset(region = VP_Y).values[0].data[0]
print(Dis_VP_X)
print(Dis_VP_Y)

PoissonRatio = -Dis_VP_X/Dis_VP_Y
print('PoissonRatio')
print(PoissonRatio)
EModulus = RF_VP_Y*(1)/(platethick*(1)*Dis_VP_Y)
print('EModulusY')
print(EModulus)
print('parameter')
print(parameter)

All_Elems = o1.rootAssembly.instances['UNIT_CELL-1'].elementSets['ALL_ELEMS']

vonMises_Strss = o1.steps['Step-1'].frames[-1].fieldOutputs['S'].getSubset(region = All_Elems, position = INTEGRATION_POINT).values

Max_Stress = 0.0

for i in vonMises_Strss:
    Mises_Stress = i.mises
    if Mises_Stress > Max_Stress: 
        Max_Stress = Mises_Stress
print('Max_Stress')
print(Max_Stress)

parameter=np.load('parameter.npy')

os.chdir(PathName)
text_file_Stress = open("Study" + "_MaxStress" + ".txt", "a")
text_file_E = open("Study" + "_EModule" + ".txt", "a")
text_file_PR = open("Study" + "_PoissonR" + ".txt", "a")

text_file_Stress.write('%16.8f \n' % (Max_Stress))
text_file_E.write('%16.8f \n' % (EModulus))
text_file_PR.write('%16.8f \n' % (PoissonRatio))


text_file_Stress.close()
text_file_E.close()
text_file_PR.close()



time_end=time.time()
print('time cost job',time_end-time_start,'s')