import random
from mutation import *
from math import *

'''
Class containing functions that generate and operate on 
the trees generated by the genetic program.
'''

#################################################################################
#                              Class & Constants                                #
#################################################################################

# Bounds on the constant coefficients
lowerBound = -10.0
upperBound = 10.0

# Operators
binary = ["+","-","*","/"]
unary = ["sqrt,sin,cos,tan"]

# Set an upper bound on the tree depth
maxDepth = 5

# Tree Node
class Node(object):

	def __init__(self):
		self.left = None
		self.right = None
		self.data = None

	# Det. if tree is unary op.
	def isUnary(self):
		if (self.data in unary):
			return True
		return False

	# Det. if tree is binary op.
	def isBinary(self):
		if (self.data in binary):
			return True
		return False

	# Det. if tree is a leaf node
	def isLeaf(self):
		return (self.left == None) and (self.right == None)

	# Det. if tree is an internal node
	def isInternal(self):
		return not Node.isLeaf(self)

#################################################################################
#                                   Creation                                    #
#################################################################################

# Probabilistically generates a binary tree representing
# a mathematical formula with height at most <depthLeft>
def generateTree(depthLeft,nested):
  # Max depth exceeded - generation must terminate
  if (depthLeft <= 0):
    return None
  # Root of tree to be generated + rand. var. to select op.
  root = Node()
  k = random.randint(1,9)
  # Either we are at leaf level or with prob 1/3 create a leaf
  if (depthLeft == 1 or k ==1 or nested):
    if (random.randint(0,5)==0 or depthLeft == 1 and nested):
      root.data = str(random.uniform(lowerBound,upperBound))
    else:
      if (nested and depthLeft > 1):
      	root.data = binary[random.randint(0,len(binary)-1)]
      	root.left = Node()
      	root.left.data = "x"
      	root.right = Node()
      	root.right.data = "x"
      else:
        root.data = "x"
  # Create binary operator
  elif (k <= 8):
    root.data = binary[random.randint(0,len(binary)-1)]
    root.left = generateTree(depthLeft-1,False)
    root.right = generateTree(depthLeft-1,False)
  # Create unary operator
  else:
    root.data = str(unary[random.randint(0,len(unary)-1)])
    root.left = None
    root.right = generateTree(depthLeft-1,True)
  return root

# Construct initial forest
def generateForest(count):
	forest = []
	for x in range(count):
		forest.append(generateTree(maxDepth,False))
	return forest

#################################################################################

# Converts tree into string for a valid mathematical expression
def treeString(tree):
	if (Node.isLeaf(tree)):
		return str(tree.data)

	left = ""
	right = ""

	if (not tree.left == None):
		left = treeString(tree.left)

	e = str(tree.data)

	if (not tree.right == None):
		right = treeString(tree.right)	

	if (tree.data in unary):
		return left + e + "(" + right + ")"
	else:
		return left + e + right

# Scores a tree over all points
def treeFitness(tree, points):
	# Attempt to evaluate - can throw exceptions
	# for invalid mathematical operations
	try:
		en = treeString(tree)
		ev = en.replace("sqrt","-sqrt")
		error = 0.0
		for p in points:
			x = p[0]
			enVal = eval(en)
			evVal = eval(ev)
			error += min(abs(p[1]-enVal),abs(p[1]-evVal))**2
		return 1.0/(error/len(points))
	# If tree is invalid, then it could not possibly be
	# the true function - return low fitness to remove from
	# population
	except:
		return -1.0

# Perform recombination between 2 trees
def recombTrees(treeX, treeY, mRate):

	# Punish extreme simplicity, force evolution when
	# solutions are too simple : i.e. a 1 node tree
	if (Node.isLeaf(treeX)):
		root = generateTree(maxDepth,False)
		treeX.data = root.data
		treeX.left = root.left
		treeX.right = root.right

	if (Node.isLeaf(treeY)):
		root = generateTree(maxDepth,False)
		treeY.data = root.data
		treeY.left = root.left
		treeY.right = root.right

	# Create tree copies
	childA = copyTree(treeX)
	childB = copyTree(treeY)

	# Count number of internal tree nodes
	aCt = countNodes(childA)
	bCt = countNodes(childB)

	# Select random subtrees for each child
	sa = findSubtree(childA,(random.randint(1,aCt),None))[1]
	sb = findSubtree(childB,(random.randint(1,bCt),None))[1]

	# Swap subtrees between copies to create children containing
	# genetic data from both parents
	temp = sa.data
	sa.data = sb.data
	sb.data = temp
	temp = sa.left
	sa.left = sb.left
	sb.left = temp
	temp = sa.right
	sa.right = sb.right
	sb.right = temp

	# Perform mutation
	if (random.randint(1,int(1/mRate)) == 1):
		mutateTree(childA)
	if (random.randint(1,int(1/mRate)) == 1):
		mutateTree(childB)

	# Check if height has been exceeded, regenerate
	# since likely expression is not good quality
	if (treeHeight(childA) > maxDepth):
		childA = generateTree(2,False)
	if (treeHeight(childB) > maxDepth):
		childB = generateTree(2,False)

	# Return tuple of children
	return (childA,childB)

# Counts the number of nodes in the tree
def countNodes(tree):
	if (tree == None):
		return 0
	elif (Node.isLeaf(tree)):
		return 1
	return 1 + countNodes(tree.left) + countNodes(tree.right)

# Creates an exact copy of the given tree
def copyTree(tree):
	if (tree == None):
		return None
	x = None
	if (Node.isLeaf(tree)):
		x = Node()
		x.data = tree.data
	elif (Node.isInternal(tree)):
		x = Node()
		x.data = tree.data
		x.left = copyTree(tree.left)
		x.right = copyTree(tree.right)
	return x

# Returns the subtree of tree rooted at the
# ctr'th internal node
def findSubtree(tree,ctr):
	if (tree == None or ctr[0] == 0):
		return ctr
	if (tree.isInternal):
		ctr = findSubtree(tree.left,ctr)
	if (ctr[0] == 0):
		return ctr
	if (ctr[0] == 1):
		return (0, tree)
	ctr = (ctr[0]-1,ctr[1])
	if (Node.isInternal(tree)):
		ctr = findSubtree(tree.right,ctr)
	return ctr

# Returns the height of the tree
def treeHeight(tree):
	if (tree == None):
		return 0
	return 1 + max(treeHeight(tree.left),treeHeight(tree.right))

# Mutates the tree by a small amount
def mutateTree(tree):
	# Select random node to mutate
	c = countNodes(tree)
	target = findSubtree(tree,(random.randint(1,c),None))[1]
	# Leaf mutations
	if (Node.isLeaf(target)):
		leafMutation(target)
	# Internal Node mutations
	else:
		internalMutation(target)

# Mutates a leaf node of the syntax tree
def leafMutation(target):
	f = random.randint(1,10)
	if (f<=3):
		target.data = binary[random.randint(0,len(binary)-1)]
		target.left = generateTree(1,True)
		target.right = generateTree(1,True)
	elif (f <= 6):
		target.data = "0"
	elif (target.data == "x"):
		target.data = random.uniform(lowerBound/5,upperBound/5)
	else:
		f = float(target.data)
		if (random.randint(0,1)==0):
			target.data = max(lowerBound,str(f-random.uniform(0.01,0.20)))
		else:
			target.data = min(upperBound,str(f+random.uniform(0.01,0.20)))

# Mutates an internal node of the syntax tree
def internalMutation(target):
	if (target.data in binary):
		j = random.randint(0,2)
		if (j == 0):
			target.data = binary[random.randint(0,len(binary)-1)]
		elif (j==1):
			k = Node()
			k.data = binary[random.randint(0,len(binary)-1)]
			k.left = target
			k.right = generateTree(maxDepth/2,True)
		else:
			k = Node()
			k.data = binary[random.randint(0,len(binary)-1)]
			k.right = target
			k.left = generateTree(maxDepth/2,True)
	elif (target.data in unary):
		target.data = unary[random.randint(0,len(unary)-1)]

# Generate random tree score for benchmarking
def randomTreeScore(points):
	x = random.uniform(lowerBound,upperBound)
	n = Node()
	n.data = str(x)
	k = treeFitness(n,points)
	return k