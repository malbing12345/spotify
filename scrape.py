# -*- coding: UTF-8 -*-
#^ keep that as the first line of the file.
#mxb130530&smd170030
import urllib
import time
import json
import zen
import matplotlib.pyplot as plt
plt.ioff()
import random
from numpy import *
from numpy.linalg import eig,norm
import numpy
import sys
sys.path.append('../zend3js/')
import d3js
import colorsys
import unicodedata
#http://json.parser.online.fr/
'''
DATA STRUCTURE KEY:

#artist_ids_CUML = list of all album id's added to the graph. useful for indexing and comparing their arrays.


'''
#FUNCTION DEFINITIONS_________________________________________________
#gets the spotify web api html info at that URL
def get_URL(URL):
	f=urllib.urlopen(URL)
	string = f.read()
	f.close
	return string

#get artist albums: need artist id
def get_albums(artist_id, limit):
	prefix= 'https://api.spotify.com/v1/artists/'
	suffix='/albums?album_type=album&market=US&limit='
	URL=prefix+artist_id+suffix+limit
	album_string=get_URL(URL)
	json_albums=json.loads(album_string)
	if (json_albums['total']>int(limit)):
		num_albums=int(limit)
	else:
		num_albums=json_albums['total']
	album_ids = list()
	album_names=list()
	substring1='(Deluxe)'
	substring2 = '(Deluxe Edition)'
	for i in range (0,num_albums):
		indicator1=1
		indicator2=1
		#make sure you don't load the copy cat albums:
		curr_album_name=json_albums['items'][i]['name']
		curr_album_id=json_albums['items'][i]['id']
		if (i==0): #no need to check
			album_ids.append(json_albums['items'][i]['id'])	#a list to store all album id's
			album_names.append(json_albums['items'][i]['name'])#a list to store all album nam
		elif (curr_album_name.endswith(substring1)): #replace smaller/older album with deluxe version
			curr_album_name_trunc=curr_album_name[:-9]
		elif (curr_album_name.endswith(substring2)):
			curr_album_name_trunc=curr_album_name[:-17]
			for j in range(0,len(album_names)):
				if (album_names[j]==curr_album_name_trunc or album_names[j]==curr_album_name):
					album_names[j]=curr_album_name
					album_ids[j]=album_ids[j]
					indicator1=0
			if (indicator1==1and album_names[j]):
				album_ids.append(curr_album_id)
				album_names.append(curr_album_name)
			
		else: #make sure we only get one album of each name.
			for k in range (0, len(album_names)):
				if (curr_album_name == album_names[k]):
					indicator2=0
			if (indicator2==1):
				album_ids.append(curr_album_id)	#a list to load all album id's
				album_names.append(curr_album_name)
		if (len(album_ids)>20):
			for r in range(20, len(album_ids)):
				album_ids.pop(20)
	return (album_ids)

def get_tracks(main_artist, main_artist_id, album_ids,G,artist_ids_CUML):
	album_ids_str=','.join(album_ids)
	prefix='https://api.spotify.com/v1/albums?ids='
	suffix='&market=US'
	URL=prefix+album_ids_str+suffix
	tracks_string=get_URL(URL)
	json_track=json.loads(tracks_string)
	artists_new_nodes=list() #initialize an empty list to store artist's featureds
	m=0 #album counter
	if (json_track.get('albums')): #only if the artist has albums
		#if you have time make it an if/else thing and still check their neighbors
		for m in range (0,len(json_track['albums'])-1): #loop through all of artist's albums
			for n in range (0, len (json_track['albums'][m]['tracks']['items'])):#loop through all songs on album
				curr_track_name=json_track['albums'][m]['tracks']['items'][n]['name']
				for p in range(0,len(json_track['albums'][m]['tracks']['items'][n]['artists'])):#loop all artist in each song
					indicator3=1
					curr_track_artist=json_track['albums'][m]['tracks']['items'][n]['artists'][p]['name']
					curr_track_artist=curr_track_artist.encode('utf-8') #because we may add this to graph.
					curr_track_artist_id=json_track['albums'][m]['tracks']['items'][n]['artists'][p]['id']
					if (curr_track_artist_id!=main_artist_id):
						#for q in range(0, G.max_node_idx):#Make sure it is not already in the graph
						print'num nodes', G.num_nodes
						print 'len cuml', len (artist_ids_CUML)
						for q in range(0, G.num_nodes):
							if (artist_ids_CUML[q]==curr_track_artist_id):#make sure id is not in graph
								indicator3=0
							#make a new version if they have the saem name
							print q
							print str(G.nodes()[q])
							print curr_track_artist
							print artist_ids_CUML[q]
							print curr_track_artist_id
						
							if (str(G.nodes()[q])==curr_track_artist and artist_ids_CUML[q]!=curr_track_artist_id):
								#give newer one a numerical id at end of name.
								curr_track_artist =curr_track_artist+curr_track_artist_id
						if (indicator3==1): #dont add new node
							G.add_node(curr_track_artist)
							artists_new_nodes.append(curr_track_artist)
							artist_ids_CUML.append(curr_track_artist_id)
						if (G.has_edge(main_artist, curr_track_artist)):
							if (G.weight(main_artist, curr_track_artist)==0):#because of edge directionality
								G.add_edge(main_artist, curr_track_artist)
							else:
								w=G.weight(main_artist, curr_track_artist)
								G.set_weight(main_artist, curr_track_artist, w+1)
						else:
							G.add_edge(main_artist, curr_track_artist)

	return (artists_new_nodes,artist_ids_CUML,G)

'''
#write a function to get the names from any rank website MALLLLLL
def read_file(fname,): #open file with names of artists from billboard list: http://www.billboard.com/charts/year-end/2016/hot-r-and-and-b-hip-hop-songs
	artist = 'empty'#initialize as string
	file=open(fname, 'r')
	with open(fname) as f:
		for i, l in enumerate(f):
			artist= file.readline()
			artist =unicodedata.normalize('NFKD',artist.strip().decode('utf-8')).encode('ascii','ignore')
			G.add_node(artist)#add the node, the node didnt exist yet.
		d3.update()
		
	return (G.num_nodes)
	'''
def read_file(fname): #open file with names of artists from billboard list: http://www.billboard.com/charts/year-end/2016/hot-r-and-and-b-hip-hop-songs
	artist = 'empty'#initialize as string
	file=open(fname, 'r')
	prefix ='https://api.spotify.com/v1/search?q='
	suffix='&type=artist'
	with open(fname) as f:
		for i, l in enumerate(f):
			artist= file.readline()
			artist =unicodedata.normalize('NFKD',artist.strip().decode('utf-8')).encode('ascii','ignore')
			G.add_node(artist)#add the node, the node didnt exist yet.
			URL=prefix+str(artist)+suffix
			artist_string=get_URL(URL)
			print artist
			json_artist=json.loads(artist_string)
			#can pick the first one[0] since in snowballing out, we are wanting the most popular drake or 'X'
			artist_ids_CUML.append(json_artist['artists']['items'][0]['id'])
	#print 'names'
	return (G.num_nodes)

#____________________________________________MAIN FILE_____________________________________________

#graph basics
G=zen.DiGraph()
d3 = d3js.D3jsRenderer(G, event_delay=0.1, interactive=False, autolaunch=True)

#read file
fname='start_art.txt' #will be more dynamic when we build the file
limit = '50'#size limiting number of albums we return; spotify API maximum
maxart = 2000 #max number artists
artist_ids_CUML = list()
num_orig_nodes= read_file(fname)
layer_size=G.num_nodes #for starters
h=0
layer_count=0
d3.update()

#while (h <5):
#while (G.num_nodes <maxart):
while (h <maxart):
	album_ids=get_albums(artist_ids_CUML[h],limit) #get the artist's albums
	artists_new_nodes,artist_ids_CUML,G=get_tracks(str(G.nodes()[h]),artist_ids_CUML[h], album_ids,G,artist_ids_CUML) #get the artist's tracks
	
	if (h==layer_size+1):
		layer_count=layer_count+1
		layer_size=G.num_nodes #size of network to search to search 2nd degree artist's neighbors
		print 'Starting new layer: ', layer_count, '.'
		print 'The Previous layer had ', G.num_nodes-1, 'nodes.'
	
	d3.update()
	h=h+1
	print h

print 'num nodes' ,G.num_nodes



#____________________________________________ANALYSIS________________________________________________


'''IDEAS:
get the centrality of the original graph: original graph is 50 nodes,



G is a directed graph made up of nodes that are identified with bc artist names. 
The original graph is 50 artists on Billboard's top 2016 year end rnb/hip hop song list.
These nodes are initially inserted into the graph by themselves. 


Interesting qualities of these artists can be observed when we step through these artists featured artists, and give the original node a directed, weighted edge to neighboring nodes which are their featured artist. 
Original node: Drake. song: No Long Talk (by Drake, ft. Giggs). Add Giggs Node and draw a weighted (w=1) edge from Drake to Giggs.

To get the qualites of these node's connections with each other:

find centrality measures of main 50 artists:
	betweenness/eigenvector
	every node iniitally is a source node,  mutual featuring


Biases: when the link to the other artist is wrong so we add them to the network even though they are the wrong version of the artist
when an artist doensnt have all their discography on spotify @chance therapper


'''

#compare that network to a new network only using spotify's related artist network.





