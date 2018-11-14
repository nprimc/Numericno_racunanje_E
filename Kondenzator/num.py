from sys import argv
import json

from operator import add
from operator import sub

import plotly.plotly as py
import plotly.graph_objs as go

from collections import OrderedDict

script, txt_file, xt, yt, zt =argv

k=1.112123*10**(-12) #4*pi*epsilon
mnoz=1
eks=0


lok=[float(xt), float(yt), float(zt)]

pointPositions={
	"tocka1": lok
	}

endResultE={}

plotlyx=[lok[0]]
plotlyy=[lok[1]]
plotlyz=[lok[2]]


print "Lokacija: ", lok
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
#E calculation
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

EinPoint=endResultE['tocka1']
MagnitudeE = sum(map(lambda x: x**2, EinPoint))**0.5

print EinPoint, "V/m"
print MagnitudeE, "V/m"

if MagnitudeE>(10**(-20)):
	while (MagnitudeE*mnoz)<0.1:
		mnoz=mnoz*10
		eks=eks+1
	while (MagnitudeE*mnoz)>2:
		mnoz=mnoz/10
		eks=eks-1

coorPoint=pointPositions['tocka1']

vectEx=[coorPoint[0]]
vectEy=[coorPoint[1]]
vectEz=[coorPoint[2]]

vectEx.append(lok[0]+EinPoint[0]*mnoz)
vectEy.append(lok[1]+EinPoint[1]*mnoz)
vectEz.append(lok[2]+EinPoint[2]*mnoz)


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
		
		if path[0] == 0.1:
			break
		EMagnitude=sum(map(lambda x: x**2, sumEonPath))**0.5		
		partEUnitVect=map(lambda x: x/(100*EMagnitude), sumEonPath)

		path=list(map(add, path, partEUnitVect))
		ForceLineCoorX.append(path[0])
		ForceLineCoorY.append(path[1])
		ForceLineCoorZ.append(path[2])
		i=i+1
		
	return ForceLineCoorX, ForceLineCoorY, ForceLineCoorZ
		
#Get list of lists (2-dimentional array) with all coordinates [[x1, x2...], [y1, y2...], [z1, z2...]]
#Starting point of line of force

Path0=[0.0001, 25, 25]
Path1=[0.0001, 25, 30]
Path2=[0.0001, 25, 35]
Path3=[0.0001, 25, 40]
Path4=[0.0001, 25, 45]
Path5=[-0.0001, 25, 49.5]





ForceLine0=LineOfForce(Path0, 500)
ForceLine1=LineOfForce(Path1, 500)
ForceLine2=LineOfForce(Path2, 500)
ForceLine3=LineOfForce(Path3, 500)
ForceLine4=LineOfForce(Path4, 500)
ForceLine5=LineOfForce(Path5, 550)


########################################################################
# Plotting feat. PLOTLY
########################################################################
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



points=go.Scatter3d(
	x=pointsx,
	y=pointsy,
	z=pointsz,
	mode='markers',
	name='Naboji',
	marker=dict(
		size=2,
		color='rgb(255, 0, 0)'
		)
	)

tocka=go.Scatter3d(
	x=plotlyx,
	y=plotlyy,
	z=plotlyz,
	mode='markers',
	name='Tocka',
	marker=dict(
		size=2,
		color='rgb(20, 20, 20)'
		)
	)

vektorE=go.Scatter3d(
	x=vectEx,
	y=vectEy,
	z=vectEz,
	mode='lines',
	line=dict(
		width=10
		),
	name='E1*10^{0}V/m'.format(eks)
	)
layout = go.Layout(title='Kroznica', yaxis=dict(scaleanchor="x", scaleratio=1))

plot=[plotlyForceLine0, plotlyForceLine1, plotlyForceLine2, plotlyForceLine3, plotlyForceLine4, plotlyForceLine5,  points, tocka, vektorE]

fig=go.Figure(data=plot, layout=layout)

py.plot(plot, filename='Kondenzator', auto_open=True)
