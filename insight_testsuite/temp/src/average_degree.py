import json
import pprint
#from dateutil import parser
input = open('./tweet_input/tweets.txt', 'r')
output = open('./tweet_output/output.txt', 'w')




class Node:
   'Common base class for all nodes'
   children = []
   uid = ""
   timestamp = ""

   def __init__(self, uid, timestamp,children=[]):   	
	self.children = children
	self.uid = uid
	self.timestamp = timestamp
   
   def addChild(self,child):
	v= False
	if child is None:    	
		return False
	#v = False
	for i in self.children:
		if child.uid==i.uid:
			i.timestamp = child.timestamp
			v = True

	if v == False:
		self.children+=[child]

	return True     

   def getCountChildren(self):
    return len(self.children)

   def removeChild(self,child):
	if len(child)<1:
		return False
	if self.children.count(child)>=1:
		self.children.delete(self.children.index(child))
	return True









def getValidTweets():
	result = []
	for line in input.readlines( ):
		j = json.loads(line)
		r = {}
		try:
			hashtags = j['entities']['hashtags']
			if len(hashtags)>=2:
				r['hash'] = ''
				for tag in hashtags:
					r['hash']= r['hash'] + ','+ tag['text'].replace(',','')
				r['hash']  = r['hash'][1:]			
				r['timestamp']  = j['created_at']
				r['id']  = j['id']
				result+=[(r)]
				#output.write(json.dumps(r)+"\n")
		except:
			pass
	return result
def addToGraph(graph,node):
	if node is None:
		return 
	valid = False
	for gNode in graph:
		if node.uid==gNode.uid:
			valid = True
			gNode.timestamp = node.timestamp
			for n in node.children:
				gNode.addChild(n)
	if valid==False:
		graph.append(node)

def getGraphDegree(graph):
	totalNodes = len(graph)
	totalEdges = 0
	for g in graph:
		totalEdges+=len(g.children)
	degree = totalEdges/float(totalNodes)
	return degree

def printExit(val):
	print(val)
	exit()

def printObject(obj):
	if obj is None :
		return 
	print obj.uid.encode('utf-8').strip(),
	for i in obj.children:
		print i.uid.encode('utf-8').strip(),
	print '-'
	return 

def printGraph(graph):
	for g in graph:
		printObject(g)


def updateGraph(graph,timestamp):
	removeNodes = []
	for g in graph:
		diff = dateDifference(g.timestamp,timestamp)
		if diff > 60:
			removeNodes.append(g)
	for g in graph:
		if len(removeNodes)>1 and g in removeNodes:
			graph.remove(g)
		else:
			for child in g.children:
				if len(removeNodes)>1 and child in removeNodes:
					g.children.remove(child)

def dateDifference(time1, time2):
	return 
	d1 = parser.parse(time1)
	d2 = parser.parse(time2)
	diff = int(abs(  d2-d1 ).total_seconds())
	return diff

	








if __name__ == '__main__':
	#print getValidTweets()
	#print 'Output Begins-----'
	#get valid tweets
	graph = []
	validTweets = getValidTweets()  # works
	count = 0
	for validTweet in validTweets:		
		#each tweet
		
		#validNode = Node(validTweet['id'],validTweet['timestamp'],[])
		validHash = validTweet['hash'].split(',')
		
		tempNodes = []
		for h in validHash:
			tempNodes.append(Node(h,validTweet['timestamp'],[]))

		for x in tempNodes:
			for y in tempNodes:
				if x.uid!=y.uid:
					x.addChild(y)
		# add nodes to the graph
		
		for i in tempNodes:
			addToGraph(graph,i)				
		#update graph
		
		# if count>50:
		# 	printGraph(graph)
		# 	exit()
		# count+=1

		updateGraph(graph,validTweet['timestamp'])
		#return degree
		degree = getGraphDegree(graph)
		output.write(str(round(degree,2))+"\n" )
	#printGraph(graph)



		
	
