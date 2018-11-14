from sys import argv
import json

from operator import add
from operator import sub

import plotly.plotly as py
import plotly.graph_objs as go
import math

from collections import OrderedDict

script, txt_file, xt0, yt0, zt0, xt1, yt1, zt1 =argv

potConst=1.438*10**(-9)

k=1.112123*10**(-12) #4*pi*epsilon
mnoz=1
eks=0


lok0=[float(xt0), float(yt0), float(zt0)]
lok1=[float(xt1), float(yt1), float(zt1)]

pointPositions={
	"tocka0": lok0,
	"tocka1": lok1
	}

endResultE={}

plotlyx0=[lok0[0]]
plotlyy0=[lok0[1]]
plotlyz0=[lok0[2]]


plotlyx1=[lok1[0]]
plotlyy1=[lok1[1]]
plotlyz1=[lok1[2]]



print "Lokacija tock: ", lok0, lok1
print "Odpiram: ", txt_file

########################################################################
#Input Parsing
########################################################################

with open(txt_file, 'r') as txt:
		naboji_dict = json.loads(txt.read(), object_pairs_hook=OrderedDict)

charges=[]

for (n, nabojDataItem) in naboji_dict.items():
	charge={
		"position": [nabojDataItem[0], nabojDataItem[1], nabojDataItem[2]],
		"quantity": nabojDataItem[3]
	}
	charges.append(charge)

########################################################################
# E calculation
#
#	Input:
#		-point location
#		-locations of charges
#		-quantity of charges
#
#	Output:
#		-electric field vector
#
########################################################################

def racE (pointPosition, chargePosition, chargeQuantity):
	# Calculate R-vector, vector components as list
	
	rVect		= list( map(sub, pointPosition, chargePosition))
	rMagnitude	= sum(	map(lambda x: x**2, rVect))**0.5
	rUnitVect	= map(	lambda x: x/rMagnitude, rVect)

	# Calculate Emagnitude in poin caused by one charge
	electricFieldMagnitude = chargeQuantity*1.6*10**(-19)/(rMagnitude**2*k)

	# Calculate E_vector
	electricFieldVect = map(lambda x: x*electricFieldMagnitude, rUnitVect)

	return electricFieldVect			


	
	
for(key, pointPosition) in pointPositions.items():
	pointElectricField=[0, 0, 0]
	for charge in charges:
		EatPointDueToCharge=racE(pointPosition, charge['position'], charge['quantity'])
		pointElectricField=list(map(add, pointElectricField, EatPointDueToCharge))
	endResultE[key]=pointElectricField #{tocka1:[Ex, Ey, Ez], ...}

EinPoint0=endResultE['tocka0']
MagnitudeE0 = sum(map(lambda x: x**2, EinPoint0))**0.5

EinPoint1=endResultE['tocka1']
MagnitudeE1 = sum(map(lambda x: x**2, EinPoint1))**0.5

print "Vektor E v tocki T0= ", EinPoint0, "V/m"
print "Absolutna vrednost E v tocki T0= ", MagnitudeE0, "V/m"

print "Vektor E v tocki T1= ", EinPoint1, "V/m"
print "Absolutna vrednost E v tocki T1= ", MagnitudeE1, "V/m"

if MagnitudeE1>(10**(-18)):
	while (MagnitudeE1*mnoz)<0.1:
		mnoz=mnoz*10
		eks=eks+1
	while (MagnitudeE1*mnoz)>1:
		mnoz=mnoz/10
		eks=eks-1

coorPoint0=pointPositions['tocka0']

vectEx0=[coorPoint0[0]]
vectEy0=[coorPoint0[1]]
vectEz0=[coorPoint0[2]]

vectEx0.append(lok0[0]+EinPoint0[0]*mnoz)
vectEy0.append(lok0[1]+EinPoint0[1]*mnoz)
vectEz0.append(lok0[2]+EinPoint0[2]*mnoz)


coorPoint1=pointPositions['tocka1']

vectEx1=[coorPoint1[0]]
vectEy1=[coorPoint1[1]]
vectEz1=[coorPoint1[2]]

vectEx1.append(lok1[0]+EinPoint1[0]*mnoz)
vectEy1.append(lok1[1]+EinPoint1[1]*mnoz)
vectEz1.append(lok1[2]+EinPoint1[2]*mnoz)


########################################################################
# Get all locations of charges for plotting
########################################################################

pointsx=[]
pointsy=[]
pointsz=[]

for (n, pos) in naboji_dict.items():
	pointsx.append(pos[0])
	pointsy.append(pos[1])
	pointsz.append(pos[2])


########################################################################
# Calculatin Equipotentials
########################################################################


### Functions used in process
def getPoint (angle, radius):
	pointX=1-math.sin(angle*math.pi/50)*radius
	pointY=0
	pointZ=math.cos(angle*math.pi/50)*radius
	Point=[pointX, pointY, pointZ]

	return Point

def calculatePotential (pointPot, chargesData):
	potential=0
	for charge in chargesData:
		chargePosition=charge['position']
		chargeQty=charge['quantity']
		rVect=list(map(sub, chargePosition, pointPot))
		rMagnitude=sum(map(lambda x: x**2, rVect))**0.5
		potential=potential+potConst*chargeQty/rMagnitude
		#print chargePosition, rMagnitude, potential
	
	return potential




equiPotX0=[]
equiPotY0=[]
equiPotZ0=[]

radius=0.0001

for angle in range(101):
	pointPot=getPoint(angle, radius)
	potential=calculatePotential(pointPot, charges)

	while potential>0.002:
		radius=radius+0.0001
		pointPot=getPoint(angle, radius)
		potential=calculatePotential(pointPot, charges)


	equiPotX0.append(pointPot[0])
	equiPotY0.append(pointPot[1])
	equiPotZ0.append(pointPot[2])	
	#print equiPotX, equiPotY, equiPotZ

	radius=0.0001

print "Potencial V0=", potential, " V"


equiPotX1=[]
equiPotY1=[]
equiPotZ1=[]
radius=0.0001

for angle in range(101):
	pointPot=getPoint(angle, radius)
	potential=calculatePotential(pointPot, charges)

	while potential>0.0015:
		radius=radius+0.0001
		pointPot=getPoint(angle, radius)
		potential=calculatePotential(pointPot, charges)


	equiPotX1.append(pointPot[0])
	equiPotY1.append(pointPot[1])
	equiPotZ1.append(pointPot[2])	

	radius=0.0001

print "Potencial V1=", potential, " V"



equiPotX2=[]
equiPotY2=[]
equiPotZ2=[]
radius=0.0001

for angle in range(101):
	pointPot=getPoint(angle, radius)
	potential=calculatePotential(pointPot, charges)

	while potential>0.001:
		radius=radius+0.0001
		pointPot=getPoint(angle, radius)
		potential=calculatePotential(pointPot, charges)


	equiPotX2.append(pointPot[0])
	equiPotY2.append(pointPot[1])
	equiPotZ2.append(pointPot[2])	
	
	radius=0.0001

print "Potencial V2=", potential, " V"




equiPotX3=[]
equiPotY3=[]
equiPotZ3=[]
radius=0.0001

for angle in range(101):
	pointPot=getPoint(angle, radius)
	potential=calculatePotential(pointPot, charges)

	while potential>0.0005:
		radius=radius+0.0001
		pointPot=getPoint(angle, radius)
		potential=calculatePotential(pointPot, charges)


	equiPotX3.append(pointPot[0])
	equiPotY3.append(pointPot[1])
	equiPotZ3.append(pointPot[2])	

	radius=0.0001

print "Potencial V3=", potential, " V"

equiPotX4=[]
equiPotY4=[]
equiPotZ4=[]
radius=0.0001

for angle in range(51):
	pointPot=getPoint(angle, radius)
	potential=calculatePotential(pointPot, charges)

	while potential>0.0001:
		radius=radius+0.001
		pointPot=getPoint(angle, radius)
		potential=calculatePotential(pointPot, charges)


	equiPotX4.append(pointPot[0])
	equiPotY4.append(pointPot[1])
	equiPotZ4.append(pointPot[2])	

	radius=0.0001

print "Potencial V4=", potential, " V"

equiPotX5=[]
equiPotY5=[]
equiPotZ5=[]
radius=0.0001

for angle in range(51):
	pointPot=getPoint(angle, radius)
	potential=calculatePotential(pointPot, charges)

	while potential>0.00001:
		radius=radius+0.0001
		pointPot=getPoint(angle, radius)
		potential=calculatePotential(pointPot, charges)
	


	equiPotX5.append(pointPot[0])
	equiPotY5.append(pointPot[1])
	equiPotZ5.append(pointPot[2])	

	radius=0.0001

print "Potencial V5=", potential, " V"


'''
#Test whether the calculation of potential is actually correct, It is!

potencial0=calculatePotential([0, 0, 0], charges)
potencial1=calculatePotential([0, 0, 1], charges)

print potencial0, potencial1
'''
'''
#Test whether the incrementation of angle and radius works correctly, It does!

equiPotX=[]
equiPotY=[]
equiPotZ=[]
radius=0.00001
for angle in range(10):
	print angle
	pointPot=getPoint(angle, radius)
	#potential=calculatePotential(pointPot, charges)

	while radius<1:
		radius=radius+0.1
		pointPot=getPoint(angle, radius)
		equiPotX.append(pointPot[0])
		equiPotY.append(pointPot[1])
		equiPotZ.append(pointPot[2])	
		print equiPotX, equiPotY, equiPotZ

	radius=0.00001
'''



########################################################################
# Calculating the line of force due to electric field
########################################################################
def LineOfForce(path, numRepetitions):
	i=0		
	ForceLineCoorX=[path[0]]
	ForceLineCoorY=[path[1]]
	ForceLineCoorZ=[path[2]]
	while i<=numRepetitions:

		sumEonPath=[0, 0, 0]

		for charge in charges:
			EonPathSingleCharge=racE(path, charge['position'], charge['quantity'])
			sumEonPath=list(map(add, sumEonPath, EonPathSingleCharge))
		
		EMagnitude=sum(map(lambda x: x**2, sumEonPath))**0.5		
		partEUnitVect=map(lambda x: x/(100*EMagnitude), sumEonPath)

		path=list(map(add, path, partEUnitVect))
		ForceLineCoorX.append(path[0])
		ForceLineCoorY.append(path[1])
		ForceLineCoorZ.append(path[2])
		i=i+1
		
	return ForceLineCoorX, ForceLineCoorY, ForceLineCoorZ
		
#Get list of lists with all coordinates [[x1, x2...], [y1, y2...], [z1, z2...]]

Path0=[0.99, 0,  0.0001]
Path1=[0.99076, 0,  0.003827]
Path2=[0.99293, 0,  0.007071]
Path3=[0.996173, 0,  0.009239]
Path4=[1, 0, 0.01]
Path5=[1.00383, 0,  0.009239]
Path6=[1.007071, 0,  0.007071]
Path7=[1.009238, 0, 0.003827]
Path8=[1.01, 0,  0]




ForceLine0=LineOfForce(Path0, 200)
ForceLine1=LineOfForce(Path1, 200)
ForceLine2=LineOfForce(Path2, 200)
ForceLine3=LineOfForce(Path3, 200)
ForceLine4=LineOfForce(Path4, 200)
ForceLine5=LineOfForce(Path5, 200)
ForceLine6=LineOfForce(Path6, 200)
ForceLine7=LineOfForce(Path7, 200)
ForceLine8=LineOfForce(Path8, 200)

########################################################################
# Plotting feat. PLOTLY
########################################################################

equiPotential0=go.Scatter3d(
	x=equiPotX0,
	y=equiPotY0,
	z=equiPotZ0,
	mode='lines',
	line=dict(
		color='rgb(50, 50, 50)',
		width=1
		),
	name='Equipotential0'
	)


equiPotential1=go.Scatter3d(
	x=equiPotX1,
	y=equiPotY1,
	z=equiPotZ1,
	mode='lines',
	line=dict(
		color='rgb(50, 50, 50)',
		width=1
		),
	name='Equipotential1'
	)



equiPotential2=go.Scatter3d(
	x=equiPotX2,
	y=equiPotY2,
	z=equiPotZ2,
	mode='lines',
	line=dict(
		color='rgb(50, 50, 50)',
		width=1
		),
	name='Equipotential2'
	)



equiPotential3=go.Scatter3d(
	x=equiPotX3,
	y=equiPotY3,
	z=equiPotZ3,
	mode='lines',
	line=dict(
		color='rgb(50, 50, 50)',
		width=1
		),
	name='Equipotential3'
	)

equiPotential4=go.Scatter3d(
	x=equiPotX4,
	y=equiPotY4,
	z=equiPotZ4,
	mode='lines',
	line=dict(
		color='rgb(50, 50, 50)',
		width=1
		),
	name='Equipotential4'
	)

equiPotential5=go.Scatter3d(
	x=equiPotX5,
	y=equiPotY5,
	z=equiPotZ5,
	mode='lines',
	line=dict(
		color='rgb(50, 50, 50)',
		width=1
		),
	name='Equipotential5'
	)


plotlyForceLine0=go.Scatter3d(
	x=ForceLine0[0],
	y=ForceLine0[1],
	z=ForceLine0[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine0'
	)
plotlyForceLine1=go.Scatter3d(
	x=ForceLine1[0],
	y=ForceLine1[1],
	z=ForceLine1[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine1'
	)
plotlyForceLine2=go.Scatter3d(
	x=ForceLine2[0],
	y=ForceLine2[1],
	z=ForceLine2[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine2'
	)
plotlyForceLine3=go.Scatter3d(
	x=ForceLine3[0],
	y=ForceLine3[1],
	z=ForceLine3[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine3'
	)
plotlyForceLine4=go.Scatter3d(
	x=ForceLine4[0],
	y=ForceLine4[1],
	z=ForceLine4[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine4'
)


plotlyForceLine5=go.Scatter3d(
	x=ForceLine5[0],
	y=ForceLine5[1],
	z=ForceLine5[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine5'
	)

plotlyForceLine6=go.Scatter3d(
	x=ForceLine6[0],
	y=ForceLine6[1],
	z=ForceLine6[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine6'
	)

plotlyForceLine7=go.Scatter3d(
	x=ForceLine7[0],
	y=ForceLine7[1],
	z=ForceLine7[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine7'
	)

plotlyForceLine8=go.Scatter3d(
	x=ForceLine8[0],
	y=ForceLine8[1],
	z=ForceLine8[2],
	mode='lines',
	line=dict(
		width=2
		),
	name='ForceLine8'
	)




points=go.Scatter3d(
	x=pointsx,
	y=pointsy,
	z=pointsz,
	mode='markers',
	name='Naboji',
	marker=dict(
		size=3,
		color='rgb(255, 0, 0)'
		)
	)

tocka0=go.Scatter3d(
	x=plotlyx0,
	y=plotlyy0,
	z=plotlyz0,
	mode='markers',
	name='Tocka',
	marker=dict(
		size=1,
		color='rgb(20, 20, 20)'
		)
	)


tocka1=go.Scatter3d(
	x=plotlyx1,
	y=plotlyy1,
	z=plotlyz1,
	mode='markers',
	name='Tocka',
	marker=dict(
		size=1,
		color='rgb(20, 20, 20)'
		)
	)

vektorE0=go.Scatter3d(
	x=vectEx0,
	y=vectEy0,
	z=vectEz0,
	mode='lines',
	line=dict(
		width=5
		),
	name='E0*10^{0}V/m'.format(eks)
	)


vektorE1=go.Scatter3d(
	x=vectEx1,
	y=vectEy1,
	z=vectEz1,
	mode='lines',
	line=dict(
		width=5
		),
	name='E1*10^{0}V/m'.format(eks)
	)


layout = go.Layout(
	)

plot=[equiPotential0, equiPotential1, equiPotential2, equiPotential3, plotlyForceLine4, equiPotential5, plotlyForceLine0, plotlyForceLine1, plotlyForceLine2, plotlyForceLine3, plotlyForceLine4, plotlyForceLine5, plotlyForceLine6, plotlyForceLine7, plotlyForceLine8,  points, tocka0, vektorE0, vektorE1, tocka1]

fig=go.Figure(data=plot, layout=layout)

py.plot(plot, filename='Dipol', auto_open=True)
