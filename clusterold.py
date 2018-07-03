import pandas
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from math import floor

def plot(db,treino,data, para_prever):
	
	avgs=[]
	core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	labels = db.labels_
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
	# Black removed and is used for noise instead.
	unique_labels = set(labels)
	print('num clusters: ',n_clusters_)
	ret=0
	ret2=0
	colors = [plt.cm.Spectral(each)
			  for each in np.linspace(0, 1, len(unique_labels))]
	for k, col in zip(unique_labels, colors):
		if k == -1:
			# Black used for noise.
			col = [0, 0, 0, 1]

		class_member_mask = (labels == k)
		xy = pandas.DataFrame(treino[class_member_mask & core_samples_mask])
		y=data[class_member_mask & core_samples_mask]
		y=y.loc[:,'3rd times':'Duration of 3rd'].values
		y2=pandas.DataFrame(y)
		if len(y)!=0:
			#print(y2)
			y2=y2.mean()
			#print(y2)
			avgs.append(y2.values)
		new=para_prever.loc[:,'1st':'2nd']

		#plt.plot(xy.ix[:, 0], xy.ix[:, 1], 'o', markerfacecolor=tuple(col),
		#		 markeredgecolor='k', markersize=14)
		if new.isin(xy).all().all():
			if len(y)!=0:
				print('Next time of arrival')
				day = floor(y2.iloc[0]/60/60/24)
				hora = floor((y2.iloc[0]-day*60*60*24)/60/60)
				minuto = floor((y2.iloc[0]-day*60*60*24-hora*60*60)/60)
				stri='Dia ' + str(day) + '  ' + str(hora) + ':' + str(minuto)
				print(stri)
				print('Next duration of stay')
				hora = floor((y2.iloc[1])/60/60)
				minuto = floor((y2.iloc[1]-hora*60*60)/60)
				stri=str(hora) + ':' + str(minuto)
				print(stri)
				ret=y2.iloc[0]
				ret2=y2.iloc[1]
			else:
				ret=0
				ret2=0

		xy = treino[class_member_mask & ~core_samples_mask]
		
		if new.isin(xy).all().all():
			if len(y)!=0:
				print('Next time of arrival')
				day = floor(y2.iloc[0]/60/60/24)
				hora = floor((y2.iloc[0]-day*60*60*24)/60/60)
				minuto = floor((y2.iloc[0]-day*60*60*24-hora*60*60)/60)
				stri='Dia ' + str(day) + '  ' + str(hora) + ':' + str(minuto)
				print(stri)
				print('Next duration of stay')
				hora = floor((y2.iloc[1])/60/60)
				minuto = floor((y2.iloc[1]-hora*60*60)/60)
				stri=str(hora) + ':' + str(minuto)
				print(stri)
				ret=y2.iloc[0]
				ret2=y2.iloc[1]
			else:
				ret=0
				ret2=0
				print('nothing here')
		#plt.plot(xy.ix[:, 0], xy.ix[:, 1], 'o', markerfacecolor=tuple(col),
		#		 markeredgecolor='k', markersize=6)

	#plt.title('Estimated number of clusters: %d' % n_clusters_)
	#plt.show()
	return ret,ret2

#fazer gpx reader para ter estes dados
#escolher um para prever
files = ['casa.csv','dei.csv']
#files = ['casa.csv']
#dados para prever  CHEGADA1, CHEGADA2  VEEM DA CASA E DO DEI.csv
arr=[]
for file in files:
	df = pandas.read_csv(file, header=None)
	data=[]
	antes =0
	for i in range(len(df)-2):
		arrival = df.loc[i][0]
		duration = df.loc[i][1]
		data.append([arrival,df.loc[i+1][0],df.loc[i+2][0],df.loc[i+2][1]])
		informacao=[df.loc[i+1][0],df.loc[i+2][0],'  ','  ']

	inf=pandas.DataFrame([informacao],columns=['1st','2nd','3rd times','Duration of 3rd'])
	data.append(informacao)
	data=pandas.DataFrame(data=data,columns=['1st','2nd','3rd times','Duration of 3rd'])  # 1st row as the column names
	#data=data.append(inf,ignore_index=True)
	#data=pandas.DataFrame(data=data)
	data = data.sample(frac=1).reset_index(drop=True)
	#print(data.dtypes)
	treino=data.loc[:,'1st':'2nd']
	inf=treino.tail(1)
	#print(inf.dtypes)
	db = DBSCAN(eps=3900, min_samples=2)
	db.fit(treino)
	#print(db)
	#print(db.core_sample_indices_)
	#print(db.components_)
	#print(db.labels_)
	#db.predict()

	[um,dois]=plot(db,treino,data,inf)
	arr.append([um,dois])
	#print('///////////////////////////////////////////////////////////////////')
	#print(avgs)

print('\nPREVISAO:')
if (arr[0][0]<arr[1][0] and arr[0][0]>0.0):
	print('--Casa--')
	print('Next time of arrival')
	day = floor(arr[0][0]/60/60/24)
	hora = floor((arr[0][0]-day*60*60*24)/60/60)
	minuto = floor((arr[0][0]-day*60*60*24-hora*60*60)/60)
	stri='Dia ' + str(day) + '  ' + str(hora) + ':' + str(minuto)
	print(stri)
	print('Next duration of stay')
	hora = floor((arr[0][1])/60/60)
	minuto = floor((arr[0][1]-hora*60*60)/60)
	stri=str(hora) + ':' + str(minuto)
	print(stri)
else:
	if (arr[1][0]>0):
		print('--DEI--')
		print('Next time of arrival')
		day = floor(arr[1][0]/60/60/24)
		hora = floor((arr[1][0]-day*60*60*24)/60/60)
		minuto = floor((arr[1][0]-day*60*60*24-hora*60*60)/60)
		stri='Dia ' + str(day) + '  ' + str(hora) + ':' + str(minuto)
		print(stri)
		print('Next duration of stay')
		hora = floor((arr[1][1])/60/60)
		minuto = floor((arr[1][1]-hora*60*60)/60)
		stri=str(hora) + ':' + str(minuto)
		print(stri)
	else:
		print('--DADOS NAO PERMITEM PREVISAO--')
#VER O MENOR
