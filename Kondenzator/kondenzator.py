import json

### Input values
chargeQuantity = 1



capY = 50
capZ = 50
deltaX = 5

# Starting point
x=0
y=0
z=0
chargeNumber=0
capacitor_dict={}


while y<=capY and z<=capZ:
	capacitor_dict.update({chargeNumber:[float(x), float(y), float(z), chargeQuantity]})
	y=y+1
	chargeNumber=chargeNumber+1

	if y >= capY:

		z=z+1
		y=0

		if z>capZ and x!=deltaX:
			x=x+deltaX
			y=0
			z=0
			chargeQuantity=(-1)*chargeQuantity
		

		if z>capZ and x==deltaX:
			y=y+1
			z=z+1

#print capacitor_dict

with open("kondenzator50x50.txt", "w") as file:
	file.write(json.dumps(capacitor_dict))

		

