import time
import random
import math

# Create an array already in order
def idealArray(arrayLength):
    return [int(i) for i in xrange(arrayLength)]

# Create an array where 90% is in order and the rest are only slightly out of place
def modifiedArray(arrayLength):
    return [int(i if random.random() < 0.9 else (i + 10 * random.random() - 5 )) for i in xrange(arrayLength)]

# Create an array where 90% is in order and the rest are random
def approxArray(arrayLength):
    return [int(i if random.random() < 0.9 else arrayLength*random.random()) for i in xrange(arrayLength)]

# Create a completely random array with values bounded by array length
def randomArray(arrayLength):
    return [int(arrayLength*random.random()) for i in xrange(arrayLength)]

# Create an array  in reverse order
def reversedArray(arrayLength):
    return [int(arrayLength - i) for i in xrange(arrayLength)]

# Create a random array with a greater (100x) range of possible values
def sparseArray(arrayLength):
    return [int(arrayLength*random.random()*100) for i in xrange(arrayLength)]


# Loop through the array moving item in the right direction until all sorted
# In place
# Comparison
# Stable
def bubbleSort(items):
    swapped = True #Assume something is in the wrong position at first
    while(swapped): # Loop through entire array while not sorted
        swapped = False # Maybe its sorted this time, lets check
        for i in range(len(items)-1): # For each set of items next to each other
            if items[i] > items[i+1]:   # If they are in the wrong order, swap them and set flag
                items[i], items[i+1] = items[i+1], items[i]
                swapped = True

# Like bubble sort but goes both directions and we can ignore items we already know are done
# In place
# Comparison
# Stable
def shakerSort(items):
    swapped = True #Assume something is in the wrong position at first
    while(swapped): # Loop through entire array while not sorted
        swapped = False # Maybe its sorted this time, lets check
        startIndex = 0 # These hold the bounds numbers
        endIndex = len(items) -1
        for i in range(startIndex, endIndex): # For each set of items next to each other ascending
            if items[i] > items[i]:   # If they are in the wrong order, swap them and set flag
                items[i], items[i+1] = items[i+1], items[i]
                swapped = True
        endIndex = endIndex - 1 # An item was pushed to the last index so we can skip that next iteration
        for i in range(endIndex, startIndex, -1): # For each set of items next to each other descending
            if items[i] < items[i-1]:   # If they are in the wrong order, swap them and set flag
                items[i], items[i-1] = items[i-1], items[i]
                swapped = True
        startIndex = startIndex + 1 # An item was pushed to the first index so we can skip that next iteration

# Sort by building a sorted list starting with the first 2 items and adding more in the correct positions
# In place
# Comparison
# Stable
def insertionSort(items):
    for i in range(1, len(items)): # For each item starting at the second
        j = i
        while j > 0 and items[j-1] > items[j]: # If the next lowest item is bigger
            items[j], items[j-1] = items[j-1], items[j] # Swap them so the lower item is to the left
            j = j-1

# Break lists into smaller sorted lists and zip the smaller lists together (recursive)
# Allocated
# Comparison
# Stable
def mergeSort(items):
    if(len(items) > 1): # If there is only one item, you are 'sorted' so do nothing
        midpoint = len(items)/2 # Split your items in half
        A = items[0:midpoint]
        B = items[midpoint:]
        mergeSort(A) # Merge sort both halves (recursive)
        mergeSort(B)
        AIndex = 0
        BIndex = 0
        for i in range(len(items)): # Zip the two halves back together taking the lower item, A item if tied
            nextA = None
            nextB = None
            if AIndex < len(A): #Grab the items at those indexes if they exist
                nextA = A[AIndex]
            if BIndex < len(B):
                nextB = B[BIndex]

            if nextA == None: #End of the A half, take the B half item
                items[i] = nextB
                BIndex = BIndex + 1
                continue
            if nextB == None: #End of the B half, take the A half item
                items[i] = nextA
                AIndex = AIndex + 1
                continue

            if nextA <= nextB: #If A is less or equal take from that half; else B half
                items[i] = nextA
                AIndex = AIndex + 1
            else:
                items[i] = nextB
                BIndex = BIndex + 1

# Emulates putting cards into sorted stacks based on the outer values of the stack
# Allocated
# Comparison
# Unstable
def patienceSort(items):
    stacks = [] # We will make stacks of items held here
    for i in range(len(items)):
        placed = False
        for stack in stacks: # Put each item on the top of a stack in order if possible or make a new stack
            if items[i] <= stack[0]:
                stack.insert(0,items[i])
                placed = True
                break
        if not placed:
            stacks.append([items[i]])
    for i in range(len(items)): # Rebuild the array from the stacks
        lowestStack = stacks[0] # The lowest item will always be visible at the front of at least one of the stacks
        for stack in stacks: # Find the lowest one and pull it from the stack and insert into the sorted array
            if stack[0] < lowestStack[0]:
                lowestStack = stack
        items[i] = lowestStack.pop(0)
        if(len(lowestStack)==0): # If a stack is empty, remove it so we stop iterating over it
            stacks.remove(lowestStack)

# Expansion of patience sort to allow putting items on the bottom of stacks
# Allocated
# Comparison
# Unstable
def unshuffleSort(items):
    stacks = [] # We will make stacks of items held here
    for i in range(len(items)):
        placed = False
        for stack in stacks: # Put each item either on the top or bottom of a stack in order if possible or make a new stack
            if items[i] <= stack[0]:
                stack.insert(0,items[i])
                placed = True
                break
            elif items[i] >= stack[-1]:
                stack.append(items[i])
                placed = True
                break
        if not placed:
            stacks.append([items[i]])
    for i in range(len(items)): # Rebuild the array from the stacks
        lowestStack = stacks[0] # The lowest item will always be visible at the front of at least one of the stacks
        for stack in stacks: # Find the lowest one and pull it from the stack and insert into the sorted array
            if stack[0] < lowestStack[0]:
                lowestStack = stack
        items[i] = lowestStack.pop(0)
        if(len(lowestStack)==0): # If a stack is empty, remove it so we stop iterating over it
            stacks.remove(lowestStack)

# Order elements into a max heap then pop one at a time while pruning the tree
# In place
# Comparison
# Unstable
def heapSort(items):
    # Look at the children of an element and swap them so the largest is the parent (recursive)
    def heapify(items, i, max):
        lIndex = i*2 + 1 # Get indexes of child nodes
        rIndex = i*2 + 2
        if lIndex < len(items)-1 and lIndex < max and items[lIndex] > items[i]: # Has a left child and it is greater than the parent
            l = items[lIndex] # Swap them
            p = items[i]
            items[i] = l
            items[lIndex] = p
            heapify(items, lIndex, max)
        if rIndex < len(items)-1 and rIndex < max and items[rIndex] > items[i]: # Has a right child and it is greater than the parent
            r = items[rIndex] # Swap them
            p = items[i]
            items[i] = r
            items[rIndex] = p
            heapify(items, rIndex, max)
    lastParent = int(2**math.floor(math.log(len(items),2)))-2
    for i in range(lastParent, -1, -1): # Starting at last element that could have children and count backwards
        heapify(items, i, len(items)) # Fix heap into max-heap
    for i in range(len(items)-1, 0, -1): # Iterate backwards starting at the end
        items[0], items[i] = items[i], items[0] # Swap largest element (at the front of max heap) with the index
        heapify(items, 0, i)

# # In place
# # Comparison
# def gnomeSort(items):

# # In place
# # Comparison
# def inplacemergeSort(items):

# # In place
# # Comparison
# def mergeinsertionSort(items):

# # Key based
# def countingSort(items):

# # Comparison
# def quickSort(items):

# # Comparison
# def oddEvenSort(items):

# # Comparison
# def librarySort(items):

# # Comparison
# def selectionSort(items):

# # Comparison
# def timSort(items):

# # In place
# # Comparison
# def shellSort(items):

# # Comparison
# def combSort(items):

# # Key based
# def radixSort(items):

# # Comparison
# def treeSort(items):

# # Key based
# def bucketSort(items):

# # Comparison
# def cycleSort(items):

# # Key based
# def flashSort(items):

# # In place
# # Comparison
# # Stable
# def blockSort(items):

# # Allocated
# # Other
# # Unstable
# def spreadSort(items):

# # In place
# # Comparison
# # Unstable
# def smoothSort(items):

# # In place
# # Comparison
# # Stable
# def introSort(items):

# # In place
# # Other
# # Unstable
# def beadSort(items):

# # Key based
# def pigeonholeSort(items):

# # Comparison
# def tournamentSort(items):

# # Allocated
# # Comparision
# def strandSort(items):

# # In place
# # Comparison
# # Stable
# def stoogeSort(items):


if __name__ == "__main__":
    arrayLength = 10000
    sortTrials = 10

    arrayLengths = []
    arrayLengths.append(100)
    arrayLengths.append(200)
    arrayLengths.append(500)
    arrayLengths.append(1000)
    arrayLengths.append(2000)
    arrayLengths.append(5000)
    arrayLengths.append(10000)

    arrayModes = {}
    arrayModes["Ideal\t"] = idealArray
    arrayModes["Modified"] = modifiedArray
    arrayModes["Approx\t"] = approxArray
    arrayModes["Random\t"] = randomArray
    arrayModes["Reverse"] = reversedArray
    arrayModes["Sparse\t"] = sparseArray

    algorithms = {}
    algorithms["Bubble Sort"] = bubbleSort
    algorithms["Shaker Sort"] = shakerSort
    algorithms["Insertion Sort"] = insertionSort
    algorithms["Merge Sort"] = mergeSort
    algorithms["Patience Sort"] = patienceSort
    algorithms["Unshuffle Sort"] = unshuffleSort
    algorithms["Heap Sort"] = heapSort

    for a in algorithms:
        for l in arrayLengths:
            for m in arrayModes:
                startTimer = time.time();
                for i in range(sortTrials):
                    algorithms[a](arrayModes[m](l));
                endTimer = time.time();
                print a, "\t", l, "\t", m, "\t", 100*(endTimer - startTimer)
        print