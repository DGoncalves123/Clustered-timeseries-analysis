import pandas
from sklearn.cluster import DBSCAN
import numpy as np


def plot(db,treino,data):
	import matplotlib.pyplot as plt
	avgs=[]
	core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	labels = db.labels_
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
	# Black removed and is used for noise instead.
	unique_labels = set(labels)
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
		#new=para_prever.loc[:,'1st':'2nd']

		plt.plot(xy.ix[:, 0], xy.ix[:, 1], 'o', markerfacecolor=tuple(col),
				 markeredgecolor='k', markersize=14)
		#if new.isin(xy).all().all():
		#	if len(y)!=0:
		#		print('Next time of arrival')
		#		print(y2.iloc[0])
		#		print('Next duration of stay')
		#		print(y2.iloc[1])
		#	else:
		#		print('nothing here')

		xy = treino[class_member_mask & ~core_samples_mask]
		
		#if new.isin(xy).all().all():
		#	if len(y)!=0:
		#		print('Next time of arrival')
		#		print(y2.iloc[0])
		#		print('Next duration of stay')
		#		print(y2.iloc[1])
		#	else:
		#		print('nothing here')
		#plt.plot(xy.ix[:, 0], xy.ix[:, 1], 'o', markerfacecolor=tuple(col),
		#		 markeredgecolor='k', markersize=6)

	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.show()
	return avgs

#fazer gpx reader para ter estes dados
#escolher um para prever
#files = ['casa.csv','dei.csv']
files = ['casa.csv']
#dados para prever  CHEGADA1, CHEGADA2
informacao=[570989, 30374, ' ', ' ']
for file in files:
	df = pandas.read_csv(file, header=None)
	inf=pandas.DataFrame([informacao],columns=['1st','2nd','3rd times','Duration of 3rd'])
	data=[]
	antes =0
	for i in range(len(df)-2):
		arrival = df.loc[i][0]
		duration = df.loc[i][1]
		data.append([arrival,df.loc[i+1][0],df.loc[i+2][0],df.loc[i+2][1]])

	#data.append(informacao)
	data=pandas.DataFrame(data=data,columns=['1st','2nd','3rd times','Duration of 3rd'])  # 1st row as the column names
	#data=data.append(inf,ignore_index=True)
	#data=pandas.DataFrame(data=data)
	data2 = data.sample(frac=0.2).reset_index(drop=True)
	print(data)
	print(data2)
	#print(data.dtypes)
	treino=data.loc[:,'1st':'2nd']
	inf=treino.tail(1)
	#print(inf.dtypes)
	db = DBSCAN(eps=40, min_samples=10)
	db.fit(treino)
	#print(db)
	#print(db.core_sample_indices_)
	#print(db.components_)
	#print(db.labels_)
	#db.predict()
	avgs=plot(db,treino,data)
	#print('///////////////////////////////////////////////////////////////////')
	#print(avgs)

