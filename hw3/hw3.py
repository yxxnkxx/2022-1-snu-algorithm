import sys

import time

sys.setrecursionlimit(10**9) 


class Adj_matrix(): #start from 0, later +1
    def __init__(self, n):
        self.n=n
        self.matrix = [[0 for col in range(n)] for row in range(n)]
        self.visited=[False for length in range(self.n)]
        self.ftime=[]
        self.trans_matrix=[[0 for col in range(n)] for row in range(n)]
        self.scclist=[]
        self.result=[]
        self.stack=[]

        


    def make_matrix(self, i, j):
        self.matrix[i][j]=1
        self.trans_matrix[j][i]=1
    
    def DFS(self, root, stack): 
        #######################iterative
        self.visited[root]=True
        stack.append(root) #stack=ftime
        self.index= len(self.ftime) #mean index of start node for each dfs 
        
        while stack:     #while stack is not empty (means DFS is running)
            node = stack.pop()
            for i in range(self.n):
                if self.matrix[node][i] == 1 and self.visited[i]==False:
                    self.visited[i]=True
                    stack.append(i)
            else:
                self.ftime.insert(self.index, node) #for each DFS, insert node at index

        
        

    
    def rDFS(self, root, scc, stack):
        self.visited[root]=True
        stack.append(root) #stack for iterative

        while stack:
            node = stack.pop()
            scc.append(node+1) #add in scclist
            for i in range(self.n):
                if self.trans_matrix[node][i] == 1 and self.visited[i]==False:
                    self.visited[i]=True
                    stack.append(i)
                   
        #while loop end, nodes in scc list means strongly connected component

            
    def getSCC(self):
        ##DFS
        for i in range(self.n):
            if self.visited[i]==False:
                self.DFS(i, self.stack)


        self.visited=[False for length in range(self.n)] #make self.visited empty for rDFS 
        
        while len(self.ftime)!=0:
            self.scclist=[] #reset scclist
            root = self.ftime.pop()         #root is the last ftime component
            if self.visited[root]==False:
                self.rDFS(root, self.scclist, self.stack)   
                self.result.append(" ".join(map(str, sorted(self.scclist))))    #add sorted scclist at result
   
        sort_start=time.time()
        self.result.sort()     #sort for lexicographic order
        sort_end=time.time()
        self.sort_time=sort_end-sort_start  #exclude time for sorting
                
    
    
class Node():
    def __init__(self, data, next=None):
        self.data=data
        self.next=next
    
    
    
class Adj_list():
    
    class Node_list(): #linked list 
        def __init__(self, i):
            self.head=Node(i) #head of list = i(vertex)
        
        def append(self, data): #append of linked list
            curr = self.head
            while curr.next:
                curr=curr.next
            curr.next=Node(data, next=None)
    
    def __init__(self, n):

        self.n=n        
        self.visited=[False for length in range(self.n+1)]
        self.ftime=[]
        self.entire_list=[self.Node_list(length) for length in range(self.n+1)] #list for each vertex(Node_list), not use index 0
        self.trans_list=[self.Node_list(length) for length in range(self.n+1)] #for transpose, each node has head data(=vertex)
        self.scclist=[]
        self.result=[]
        self.stack=[]
        
    
    def DFS(self, root, stack):
        self.visited[root]=True
        stack.append(root) #stack=ftime
        self.index= len(self.ftime)
        
        while stack:
            node = stack.pop()
            curr = self.entire_list[node].head 

            while curr!=None:
                curr = curr.next
                if curr!=None and self.visited[curr.data]==False: #if curr has next, DFS recursively for the curr.next
                    self.visited[curr.data]=True
                    stack.append(curr.data)
            else:
                self.ftime.insert(self.index, node)
                        
    

        
    def rDFS(self, root, scc, stack):
        self.visited[root]=True
        stack.append(root)

        while stack:
            node = stack.pop()
            curr = self.trans_list[node].head 
            scc.append(curr.data)
            while curr!=None:
                curr=curr.next
                while curr!=None and self.visited[curr.data]==False:
                    self.visited[curr.data]=True
                    stack.append(curr.data)
            
              


    def getSCC(self):

        for i in range(1, self.n+1):
            if self.visited[i]==False:
                self.DFS(i, self.stack)
                

        self.visited=[False for length in range(self.n+1)] #make self.visited empty for rDFS 
        
        while self.ftime:
            self.scclist=[]
            root = self.ftime.pop()         #root is the last ftime component
            if self.visited[root]==False:
                self.rDFS(root, self.scclist, self.stack)
                self.result.append(" ".join(map(str, sorted(self.scclist))))

        sort_start=time.time()
        self.result.sort()     #sort for lexicographic order
        sort_end=time.time()
        self.sort_time=sort_end-sort_start #exclude time for sorting
        

    
    

class Adj_array():
    vertex_array=[0]
    edge_array=[0] #not use index 0
    def __init__(self, n):
        self.n=n        
        self.visited=[False for length in range(self.n+1)]
        self.ftime=[]
        self.trans_vertex=[0 for length in range(self.n+1)]
        self.trans_edge=[0]
        self.scclist=[]
        self.result=[]
        self.stack=[]


    
    def make_array(self, i, edges, n): #edges=array
        self.vertex_array.append(n)
        self.vertex_array[i] += self.vertex_array[i-1]
        if edges==None: #don't have edges 
            return
        self.edge_array.extend(edges)

        
        
    def DFS(self, root, stack):
        self.visited[root]=True
        stack.append(root) #stack=ftime
        self.index= len(self.ftime)
        
        while stack:
            node = stack.pop()
            start_index=self.vertex_array[node-1]+1     #each root has edges for index[root-1]+1~[root]
            end_index=self.vertex_array[node]
            for j in range(start_index, end_index+1):
                if self.visited[self.edge_array[j]]==False:
                    self.visited[self.edge_array[j]]=True
                    stack.append(self.edge_array[j])
            else:
                self.ftime.insert(self.index, node)
                
   

    def transpose(self):
        self.temp_edge=[[] for length in range(self.n+1)]   
        
        for i in range(1, self.n+1):
            start_index=self.vertex_array[i-1]+1
            end_index=self.vertex_array[i]
            for j in range(start_index, end_index+1):
                trans_data=self.edge_array[j]       #trans_data = originally edge, and will be vertex
                self.trans_vertex[trans_data] +=1   #check for how many edges trans_vertex has
                self.temp_edge[trans_data].append(i)    #temp_edge has edges of trans_vertex
        
        
        for i in range(1, self.n+1):
            self.trans_vertex[i]+=self.trans_vertex[i-1]    #for array that represents index of each vertex(same as vertex_array)
            if self.trans_vertex[i]!=0: 
                self.trans_edge.extend(self.temp_edge[i])   #extend each temp_edge in trans_edge (same as make edge_array)
                
 
    def rDFS(self, root, scc, stack):
        self.visited[root]=True
        stack.append(root)

        while stack:
            node = stack.pop()
            scc.append(node)
            start_index=self.trans_vertex[node-1]+1     #each root has edges for index[root-1]+1~[root]
            end_index=self.trans_vertex[node]
            for j in range(start_index, end_index+1):
                if self.visited[self.trans_edge[j]]==False:
                    self.visited[self.trans_edge[j]]=True
                    stack.append(self.trans_edge[j])
    
            

    def getSCC(self):
        for i in range(1, self.n+1):
            if self.visited[i]==False:
                self.DFS(i, self.stack)
                
        
        trans_start=time.time()
        self.transpose()  ##transpose
        trans_end=time.time()
        self.trans_time=trans_end-trans_start
        
        self.visited=[False for length in range(self.n+1)] #make self.visited empty for rDFS 
        
        while self.ftime:
            self.scclist=[]
            root = self.ftime.pop()         #root is the last ftime component
            if self.visited[root]==False:
                self.rDFS(root, self.scclist, self.stack)
                self.result.append(" ".join(map(str, sorted(self.scclist))))
                
        sort_start=time.time()
        self.result.sort()     #sort for lexicographic order
        sort_end=time.time()
        self.sort_time=sort_end-sort_start
        
        



################main#####################
input = open(sys.argv[1], 'r') #read input file
output = open(sys.argv[2], 'w') #write output file 

n = int(input.readline()) #first line of input is number of vertices



if sys.argv[3] == "adj_mat": 
    adj_mat = Adj_matrix(n)
    for i in range(n):
        temparray = list(map(int, input.readline().split())) #make each line as int array
        num_edge=temparray[0] 
        for j in range(1, num_edge+1):
            adj_mat.make_matrix(i, temparray[j]-1) #-1 for index that starts from 0
                                                   #i means vertex, temparray[j]-1 means edges
    start_time=time.time()
    adj_mat.getSCC()
    result=adj_mat.result
    end_time=time.time()-adj_mat.sort_time
            
elif sys.argv[3] == "adj_list":
    adj_list=Adj_list(n) #entire list

    for i in range(1, n+1):
        
        temparray=list(map(int, input.readline().split()))
        num_edge=temparray[0]
        if num_edge==0:
            continue #do nothing for 0 edge
        else:
            for j in range(1, num_edge+1):
                adj_list.entire_list[i].append(temparray[j])
                adj_list.trans_list[temparray[j]].append(i)

    start_time=time.time()
    adj_list.getSCC()
    result=adj_list.result
    end_time=time.time()-adj_list.sort_time
    
    
elif sys.argv[3] == "adj_arr":
    adj_arr= Adj_array(n)
    for i in range(1,n+1):
        temparray=list(map(int, input.readline().split()))
        num_edge=temparray[0]
        if num_edge==0:
            adj_arr.make_array(i, None, num_edge)   #if don't have edges, just update vertex_array
        else:
            adj_arr.make_array(i, temparray[1:], num_edge) #extend temparray[1:]==array of edges

    start_time=time.time()
    adj_arr.getSCC()
    
    result=adj_arr.result
    end_time=time.time()-adj_arr.trans_time-adj_arr.sort_time
    
    

    
for i in range(len(result)):
    output.write(result[i])
    output.write("\n")
output.write(str(round((end_time-start_time)*1000))+ "ms")

    