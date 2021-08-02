# Grafica de Computadoras

# -----------------------------------------------------------------------
# DISCLAIMER: Dado que no contamos con tanto espacio de memoria
# he de aclarar que se evadio la programación defensiva, esto con el 
# proposito de parecerse lo mas posible a una libreria y no un programa
# -----------------------------------------------------------------------

import struct

frBff = ''
currentColor = ''
width = ''
height = ''

def char(c): # 1 bit
  return struct.pack('=c', c.encode('ascii'))

def word(w): # 2 bits
  return struct.pack('=h', w)

def dword(dw): # 4 bits
  return struct.pack('=l', dw)

def color(b, g, r): # generador de colores
  return bytes([b, g, r])

def glCreatorWindow(width, height): # Crea la ventana, ancho x alto
	fb =  [
    [0 for x in range(width)] # Inicializa el framebuffer con ceros
    for y in range(height)
  	]
	return fb

def glViewPort(x, y, width, height): # Crea delimitantes a partir de limites
	width = round(width/2,1)
	height = round(height/2,1)
	xMin = x - width
	xMax = x + width
	yMin = y - height
	yMax = y + height

	return xMin, xMax, yMin, yMax

def glClear(): # Limpia el framebuffer aplicandole color rojo
	global frBff
	frBff =  [
    [color(0,0,255) for x in range(len(frBff))]
    for y in range(len(frBff[0]))
  	]
	return frBff

def glClearColor(r, g, b): # Personaliza el color del framebuffer
	global frBff
	frBff =  [
    [color(round(r*255), round(g*255), round(b*255)) for x in range(len(frBff))]
    for y in range(len(frBff[0]))
  	]
	return frBff

def vertex(x,y): # Ubica un punto dentro del viewPort
	global frBff
	xMin, xMax, yMin, yMax = glViewPort(width/2, height/2, width/2, height/2) # Delimitadores
	xMid = round((xMax-xMin)/2)
	yMid = round((yMax-yMin)/2)

	if ((x >= -1 and x <= 1) and (y >= -1 and y <= 1)): # Si esta en rango
		# Casos para X
		if (x < 0 and x >= -1):
			x += 1
			x = xMin + round(x*xMid)
		elif (x > 0 and x <= 1):
			x = 1 - x
			x = xMax - round(x*xMid)
		elif x == 0:
			x = xMin + xMid
		# Casos para Y
		if (y < 0 and y >= -1):
			y += 1
			y = yMin + round(y*yMid)
		elif (y > 0 and y <= 1):
			y = 1 - y
			y = yMax - round(y*yMid)
		elif y == 0:
			y = yMin + yMid

		frBff[int(y)][int(x)] = currentColor 


def write(filename, width, height, framebuffer): # Escribe el .bmp
	
	f = open(filename, 'bw')

    # file header 14
	f.write(char('B'))
	f.write(char('M'))
	f.write(dword(14 + 40 + 3*(width*height)))
	f.write(dword(0))
	f.write(dword(54))

	# info header 40
	f.write(dword(40))
	f.write(dword(width))
	f.write(dword(height))
	f.write(word(1))
	f.write(word(24))
	f.write(dword(0))
	f.write(dword(3*(width*height)))
	f.write(dword(0))
	f.write(dword(0))
	f.write(dword(0))
	f.write(dword(0))

	# bitmap
	for y in range(height):
		for x in range(width):
			f.write(framebuffer[x][y])

	f.close()

def glColor(r, g, b): # Cambia el color recurrente
	global currentColor
	currentColor = color(round(r*255), round(g*255), round(b*255))

"""
def glFinish(): # Ejecuta la inscripcion del bitmap
	write('prueba1.bmp', len(frBff), len(frBff[0]), frBff)
"""

def glLine(x0, y0, x1, y1): # Pinta una linea
	global frBff
	xMin, xMax, yMin, yMax = glViewPort(width/2, height/2, 9*width/10, 9*height/10)
	# Traduccion de los puntos ingresados
	points = [x0, y0, x1, y1]
	values = list(map(int,points))

	# ----------------------------------------------------------
	# DISCLAIMER: Translator is not used in this lab
	# ----------------------------------------------------------

	"""
	mid = 0
	currentMin = 0
	currentMax = 0
	for i in values: # Establece los valores segun el eje
		index = values.index(i)
		if (index%2 == 0): 
			mid = round((xMax-xMin)/2)
			currentMin = xMin
			currentMax = xMax
		else:
			mid = round((yMax-yMin)/2)
			currentMin = yMin
			currentMax = yMax
		if ((i >= -1 and i <= 1)): # Si esta en rango
			# Casos 
			if (i < 0 and i >= -1):
				i += 1
				i = currentMin + round(i*mid)
			elif (i > 0 and i <= 1):
				i = 1 - i
				i = currentMax - round(i*mid)
			elif i == 0:
				i = currentMin + mid
			values[index] = int(i)
	"""
	currentX = values[0]
	currentY = values[1]
	finalX = values[2]
	finalY = values[3]
	
	# ----------------------------------------------------------
	# DISCLAIMER: Improvable Functional Code
	# ----------------------------------------------------------

	if (finalY - currentY) != 0:
		slope = (finalX - currentX)/(finalY - currentY)

		if slope < 0:

			if ((finalX > currentX) and (finalY < currentY)):
				finalX, currentX = currentX, finalX
				finalY, currentY = currentY, finalY

			if slope <= -1:
				while ((currentX >= finalX) and (currentY <= finalY)):
					frBff[int(round(currentY))][int(round(currentX))] = currentColor
					flag = currentX + slope
					for i in range(int(round(currentX))-1,int(round(flag)), -1):
						if ((currentX >= finalX) and (currentY <= finalY)):
							frBff[int(round(currentY))][int(round(i))] = currentColor
							currentX -= 1
					currentX = flag
					currentY += 1
			if slope > -1:
				while ((currentX >= finalX) and (currentY <= finalY)):
					frBff[int(round(currentY))][int(round(currentX))] = currentColor
					currentX += slope
					currentY += 1

		if ((finalX < currentX) and (finalY < currentY)):
			finalX, currentX = currentX, finalX
			finalY, currentY = currentY, finalY

		if slope >= 1:
			while ((currentX <= abs(finalX)) and (currentY <= abs(finalY))):
				frBff[int(round(currentY))][int(round(currentX))] = currentColor
				flag = currentX + slope
				for i in range(int(round(currentX))+1, int(round(flag))):
					if ((currentX <= abs(finalX)) and (currentY <= abs(finalY))):
						frBff[int(round(currentY))][int(round(i))] = currentColor
						currentX += 1
				currentX = flag
				currentY += 1

		elif slope < 1:
			while ((currentX <= abs(finalX)) and (currentY <= abs(finalY))):
				frBff[int(round(currentY))][int(round(currentX))] = currentColor
				currentX += slope
				currentY += 1
	elif (finalY - currentY) == 0:
		if (finalX < currentX):
			finalX, currentX = currentX, finalX

		while ((currentX <= abs(finalX))):
			for i in range(currentX, finalX+1):
				frBff[int(round(currentY))][int(round(i))] = currentColor
				currentX += 1

def polygonOne():

	# Raw coordinates are been submitted 
	glLine(165, 380,185, 360)
	glLine(185, 360,180, 330)
	glLine(180, 330,207, 345)
	glLine(207, 345,233, 330)
	glLine(233, 330,230, 360)
	glLine(230, 360,250, 380) 
	glLine(250, 380,220, 385) 
	glLine(220, 385,205, 410) 
	glLine(205, 410,193, 383) 
	glLine(193, 383,165, 380)
	write('polygonOne.bmp', len(frBff), len(frBff[0]), frBff)




	
def glInit(): # Inicializa el programa
	
	global frBff
	global currentColor
	global width
	global height
	currentColor = color(1,0,0)
	width = 1024
	height =  1024
	frBff = glCreatorWindow(width, height) # Framebuffer
	frBff = glClear() # Pinta el bg de un color
	frBff = glClearColor(0,0,1) # Modifica color de bg
	glColor(0,0,0)

	polygonOne()


	# LAB 1 -----------------------------------------------
	# vertex(1,1)
	# vertex(0,0)
	# vertex(-1,-1)

	# LAB 2 -----------------------------------------------
	# glFinish()

glInit()