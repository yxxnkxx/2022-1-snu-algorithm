
import sys
import time
sys.setrecursionlimit(10**9)

class Node():
    def __init__(self, data):
        self.data = data
        self.parent=None
        self.left=None
        self.right=None
        self.color=1 #Red:1, Black:0
        self.size=1
        
        
        
class OSTree():
    
    def __init__(self):
        self.nil=Node(0)
        self.nil.color=0
        self.nil.size=0
        self.nil.left=self.nil
        self.nil.right=self.nil
        self.nil.parent=self.nil
        self.root=self.nil


        
    def update_size(self, x):
        if x==self.nil:
            return
        x.size=x.left.size+x.right.size+1
    
    
    def left_rotate(self, x):
        y=x.right
        x.right=y.left
        if y.left!=self.nil:
            y.left.parent=x
        y.parent=x.parent
        if x.parent==self.nil:
            self.root=y
        elif x==x.parent.left:
            x.parent.left=y
        else:
            x.parent.right=y
        y.left=x
        x.parent=y
        y.size=x.size
        self.update_size(x)


        
        
    def right_rotate(self, x):
        y=x.left
        x.left=y.right
        if y.right!=self.nil:
            y.right.parent=x
        y.parent=x.parent
        if x.parent==self.nil:
            self.root=y
        elif x==x.parent.right:
            x.parent.right=y
        else:
            x.parent.left=y
        y.right=x
        x.parent=y
        y.size=x.size
        self.update_size(x)

        

    def insert_fixup(self, z):
        while z.parent.color==1: #parent==RED
            if z.parent==z.parent.parent.left:  #parent is left child
                y=z.parent.parent.right
                if y.color==1: #if sibling is red
                    z.parent.color=0
                    y.color=0
                    z.parent.parent.color=1
                    z=z.parent.parent
                else:
                    if z==z.parent.right: #sibling is black and z is right child
                        z=z.parent
                        self.left_rotate(z)
                
                    z.parent.color=0
                    z.parent.parent.color=1
                    self.right_rotate(z.parent.parent)
            else: #parent is right child
                y=z.parent.parent.left
                if y!=self.nil and y.color==1:
                    z.parent.color=0
                    y.color=0
                    z.parent.parent.color=1
                    z=z.parent.parent
                else: 
                    if z==z.parent.left:
                        z=z.parent
                        self.right_rotate(z)
                
                    z.parent.color=0
                    z.parent.parent.color=1
                    self.left_rotate(z.parent.parent) 
                    

        self.root.color=0

            
        
        
        
    def os_insert(self, z):
        
        y=self.nil
        x=self.root

        zNode = Node(z)
        zNode.left=self.nil
        zNode.right=self.nil
        zNode.parent=self.nil
        zNode.size=1
        
        #check if z is in Tree
        while x!=self.nil:
            # x.size+=1
            y=x
            if z < x.data:
                x=x.left
            elif z > x.data:
                x=x.right
            else:
                return 0
            
            
    
        zNode.parent=y
        if y==self.nil: #if tree is empty, x=root, color BLACK
            self.root=zNode
            self.root.color=0
            return zNode.data   
            
        if zNode.data<y.data:
            y.left=zNode
        else:
            y.right=zNode
        zNode.left=self.nil
        zNode.right=self.nil
        zNode.color=1
        self.insert_fixup(zNode)
        
        #size update
        sizetemp=zNode
        while sizetemp!=self.nil:
            self.update_size(sizetemp)
            sizetemp=sizetemp.parent
        

        return zNode.data
        
        
        
    def transplant(self, u, v):
        if u.parent==self.nil:
            self.root=v
        elif u==u.parent.left:
            u.parent.left=v
        else:
            u.parent.right=v
        v.parent=u.parent

        
        
    def tree_minimum(self, x):
        while x.left!=self.nil:
            x=x.left
        return x

        
        
    def delete_fixup(self, x):
        while x!=self.root and x.color==0:
            if x==x.parent.left:
                w=x.parent.right
                if w.color==1:
                    w.color=0
                    x.parent.color=1
                    self.left_rotate(x.parent)
                    w=x.parent.right
                if w.left.color==0 and w.right.color==0:
                    w.color=1
                    x=x.parent
                else: 
                    if w.right.color==0:
                        w.left.color=0
                        w.color=1
                        self.right_rotate(w)
                        w=x.parent.right
                
                    w.color=x.parent.color
                    x.parent.color=0
                    w.right.color=0
                    self.left_rotate(x.parent)
                    x=self.root
            else:
                w=x.parent.left
                if w.color==1:
                    w.color=0
                    x.parent.color=1
                    self.right_rotate(x.parent)
                    w=x.parent.left
                if w.right.color==0 and w.left.color==0:
                    w.color=1
                    x=x.parent
                else:
                    if w.left.color==0:
                        w.right.color=0
                        w.color=1
                        self.left_rotate(w)
                        w=x.parent.left
                
                    w.color=x.parent.color
                    x.parent.color=0
                    w.left.color=0
                    self.right_rotate(x.parent)
                    x=self.root
        x.color=0
        
        
    def os_delete(self, z):


        y=self.nil
        x=self.root

        #check if z in Tree
        while x!=self.nil:
            y=x
            if z<x.data:
                x=x.left
            elif z>x.data:
                x=x.right
            else:
                break
        if x==self.nil:
            return 0
                   
        #x is node to delete
        
        y=x
        y_original_color = y.color
        temp = self.nil
 
    
        if x.left==self.nil:
            temp=x.right
            self.transplant(x, x.right)
            
            #size update
            sizetemp=x.parent
            while sizetemp!=self.nil:
                self.update_size(sizetemp)
                sizetemp=sizetemp.parent    
        elif x.right==self.nil:
            temp=x.left
            self.transplant(x, x.left)
            
            #sizeupdate
            sizetemp=x.parent
            while sizetemp!=self.nil:
                self.update_size(sizetemp)
                sizetemp=sizetemp.parent    
        else:
            y=self.tree_minimum(x.right)
            y_original_color=y.color
            temp=y.right
            if y.parent==x:
                temp.parent=y
            else:
                self.transplant(y, y.right)
                y.right=x.right
                y.right.parent=y
                
            self.transplant(x,y)
            y.left=x.left
            y.left.parent=y
            y.color=x.color
            
            #size update
            sizetemp=temp.parent
            while sizetemp!=self.nil:
                self.update_size(sizetemp)
                sizetemp=sizetemp.parent    


        if y_original_color==0:
            self.delete_fixup(temp)

    
        return x.data
    
    
    def os_select(self, root, i):
        if self.root.size < i:
            return 0
        r = root.left.size+1
        if i==r:
            return root.data
        elif i<r:
            return self.os_select(root.left, i)
        else:
            return self.os_select(root.right, i-r)
        
        
    def os_rank(self, x):
        
        root=self.root
        node=self.nil

        #check if x is in tree
        while root!=self.nil:
            node=root
            if x<root.data:
                root=root.left
            elif x>root.data:
                root=root.right
            else:
                break
        if root==self.nil:
            return 0
        
        
        r = node.left.size+1
        y=node
        while y!=self.root:
            if y==y.parent.right:
                r = r+ y.parent.left.size+1
            y=y.parent
        return r
    
    
            
class Checker():
    def __init__(self):
        self.checker = [0 for i in range(10000)]
        self.size=0
        
    def os_insert(self, x):
        if self.checker[x]==0:
            self.checker[x]=1
            self.size+=1
            return x
        elif self.checker[x]==1:
            return 0
        #if x is in Tree return 0 / if x is inserted return x
    
    def os_delete(self, x):
        if self.checker[x]==1:
            self.checker[x]=0
            self.size-=1
            return x
        elif self.checker[x]==0:
            return 0
        #if x is in Tree(successful delete) return x / if x is not in Tree, return 0
    
    def os_select(self, i):
        
        if self.size<i:
            return 0
        check_iter=iter(self.checker)   
        cnt = 0
        for j in range(len(self.checker)):
            if next(check_iter)==1:
                cnt+=1
            if cnt==i:
                return j
    #use iter

    
    def os_rank(self, x):
        if (self.checker[x]==0):
            return 0        
        
        cnt=0
        for i in range(1,x+1):
            if self.checker[i]==1:
                cnt+=1

        return cnt
            
         
         
def isCorrect(output, check):
    if (output==check):
        return ""
    else:
        return "Wrong, output should be "+ str(check) + " but " + str(output)
           



#main
if __name__ == "__main__":
    output=open("./input1/output.txt", 'w')
    checker =open("./input1/checker.txt", 'w')
    
    
    newTree = OSTree()
    resultList=[]
    inputList=[]
 
    # OS_start=time.time() #for time check
    with open("./input1/input.txt", 'r') as f:
        for line in f:
            if not line:
                break
            if line=="\n" or line=="":
                continue
            #ignore empty input 
    
    
    
            order, number = line.split()
            number=int(number)
            output.write(line)
            inputList.append(line)


            if order=="I":
                resultList.append(newTree.os_insert(number))
                
            elif order=="D":
                resultList.append(newTree.os_delete(number))

            
            elif order=="S":
                resultList.append(newTree.os_select(newTree.root, number))



            elif order=="R":
                resultList.append(newTree.os_rank(number))



    # OS_end=time.time() #for time check
    # checker.write("Program runtime:  " +str(round(OS_end-OS_start, 3)) + "s\n")

    newChecker = Checker()
    # check_start=time.time()  #for time check

    #for checker    
    result_iter=iter(resultList)
    input_iter=iter(inputList)

    
    for i in range(len(inputList)):
        resultNum=next(result_iter)
        output.write(str(resultNum)+"\n")
        order, number = next(input_iter).split()
        number=int(number)

        if order=="I":
            check=newChecker.os_insert(number)

        elif order=="D":
            check=newChecker.os_delete(number)

        elif order=="S":
            check=newChecker.os_select(number)

        elif order=="R":
            check=newChecker.os_rank(number)
        
        
        checkresult=isCorrect(resultNum, check)
        if checkresult!="":
            checker.write("Line "+ str(i+1)+ " "+ checkresult+ "\n")

    # check_end=time.time()
    # checker.write("Program runtime:  " +str(round(OS_end-OS_start, 3)) + "s\n")
    # checker.write("Checker runtime: " +str(round(check_end-check_start, 3)) + "s\n")
    ## for time check
    
    