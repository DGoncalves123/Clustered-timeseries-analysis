import pandas as pd
import xml.etree.ElementTree as ET
import gpxpy
import geopy.distance
from datetime import timedelta,date,datetime
import numpy
import time

def get_first_dow(year, week):
	d = date(year, 1, 1)
	d = d - timedelta(d.weekday())
	dlt = timedelta(days = (week - 1) * 7)
	return d + dlt

def distance(p1,p2):
	return geopy.distance.vincenty(p1, p2).m
#file='semana01(15.02-20.02).gpx'              
#file='semana02(22.02-27.02).gpx'       
#file='semana03(01.03-06.03).gpx'             
#file='semana04(08.03-13.03).gpx'   
file = 'semanas.gpx'          
casa = [40.20032, -8.41810]
dei = [40.18652,-8.41575]
f = open(file, 'r')
gpx = gpxpy.parse(f)
tudo=[]
casad = []
deid=[]
casaF=[]
deiF=[]
DEBUG=False
DEBUG2=False

for track in gpx.tracks:
	for segment in track.segments:
		for point in segment.points:
			tudo.append([point.latitude, point.longitude,point.time])
#print(tudo)
c=0
d=0
week=timedelta(weeks=1)
week=week.total_seconds()
for point in tudo:
	tempo=point[2]
	point[2]=(point[2]-datetime.combine(get_first_dow(2018,point[2].isocalendar()[1]), datetime.min.time())).total_seconds()
	p1=[point[0],point[1]]
	if distance(p1,casa)<500:
		if (c!=1):
			if DEBUG:
				print('\n\n')
				print("++chegou a casa")
				print(tempo)
			casaF.append(point)
		if d==1:
			time = (point[2]-deiF[-1][2])
			if DEBUG:
				print('duracao: ',time)
			if time<0:
				if DEBUG:
					print("--saiu do dei")
					print(week+time)
				deiF.append(week+time) 
			elif time<140:
				if DEBUG:
					print('--dei pouco')
				del deiF[-1]
			else:
				if DEBUG:
					print("--saiu do dei")
					print(tempo)
				deiF.append(time) 
		c=1
		d=0
		casad.append(point)
	elif distance(p1,dei)<400:
		if (d!=1):
			if DEBUG:
				print('\n\n')
				print("++chegou ao dei")
				print(tempo)
			deiF.append(point)
		if c==1:
			time = (point[2]-casaF[-1][2])
			if time<0:
				if DEBUG:
					print("--saiu de casa")
					print(week+time)
				casaF.append(week+time) 
			elif time<140:
				if DEBUG:
					print('--casa pouco')
				del casaF[-1]
			else:
				if DEBUG:
					print("--saiu de casa")
					print(tempo)
				casaF.append(time)  
		d=1
		c=0
		deid.append(point)
	else:
		if d==1:
			time = (point[2]-deiF[-1][2])
			if DEBUG:
				print('duracao: ',time)
			if time<0:
				if DEBUG:
					print("--saiu do dei")
					print(week+time)
				deiF.append(week+time) 
			elif time<140:
				if DEBUG:
					print('--dei pouco')
				del deiF[-1]
			else:
				if DEBUG:
					print("--saiu do dei")
					print(tempo)
				deiF.append(time) 
		elif c==1:
			time = (point[2]-casaF[-1][2])
			if DEBUG:
				print('duracao: ',time)
			if time<0:
				if DEBUG:
					print("--saiu de casa")
					print(week+time)
				casaF.append(week+time) 
			elif time<140:
				if DEBUG:
					print('--casa pouco')
				del casaF[-1]
			else:
				if DEBUG:
					print("--saiu de casa")
					print(tempo)
				casaF.append(time)    
		d=0
		c=0


#para corrigir um erro
if len(deiF)%2!=0:
	time = (tudo[-1][2]-deiF[-1][2])
	casaF.append(time)
if len(casaF)%2!=0:
	time = (tudo[-1][2]-casaF[-1][2])
	casaF.append(time)

if DEBUG2:
	print('\n\nCASA---')
	for ob in casaF:
		print(ob,'\n')
	print('\n\n\nDEI---')
	for ob in deiF:
		print(ob,'\n')


tosave=[]
for i in range(0,len(casaF),2):
	tosave.append([casaF[i][2],casaF[i+1]])
numpy.savetxt("casa.csv", tosave, delimiter=",",fmt='%i')
tosave=[]
for i in range(0,len(deiF),2):
	tosave.append([deiF[i][2],deiF[i+1]])
numpy.savetxt("dei.csv", tosave, delimiter=",",fmt='%i')