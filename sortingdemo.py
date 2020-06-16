import time
import random

# Create an array already in order
def idealArray(arrayLength):
    return [int(i) for i in xrange(arrayLength)]

# Create an array where 90% is in order and the rest are only slightly out of place
def modifiedArray(arrayLength):
    return [int(i if random.random() < 0.9 else (i + 10 * random.random() - 5 )) for i in xrange(arrayLength)]

# Create an array where 90% is in order and the rest are random
def approxArray(arrayLength):
    return [int(i if random.random() < 0.9 else arrayLength*random.random()) for i in xrange(arrayLength)]

# Create a completely random array
def randomArray(arrayLength):
    return [int(arrayLength*random.random()) for i in xrange(arrayLength)]

# Create an array  in reverse order
def reversedArray(arrayLength):
    return [int(arrayLength - i) for i in xrange(arrayLength)]


# Loop through the array moving item in the right direction until all sorted
def bubbleSort(items):
    swapped = True #Assume something is in the wrong position at first
    while(swapped): # Loop through entire array while not sorted
        swapped = False # Maybe its sorted this time, lets check
        for i in range(len(items)-1): # For each set of items next to each other
            a = items[i]
            b = items[i+1]
            if a > b:   # If they are in the wrong order, swap them and set flag
                items[i] = b
                items[i+1] = a
                swapped = True

# Like bubble sort but we can ignore items we already know are done
def shakerSort(items):
    swapped = True #Assume something is in the wrong position at first
    while(swapped): # Loop through entire array while not sorted
        swapped = False # Maybe its sorted this time, lets check
        startIndex = 0 # These hold the bounds numbers
        endIndex = len(items) -1
        for i in range(startIndex, endIndex): # For each set of items next to each other ascending
            a = items[i]
            b = items[i+1]
            if a > b:   # If they are in the wrong order, swap them and set flag
                items[i] = b
                items[i+1] = a
                swapped = True
        endIndex = endIndex - 1 # An item was pushed to the last index so we can skip that next iteration
        for i in range(endIndex, startIndex, -1): # For each set of items next to each other descending
            a = items[i]
            b = items[i-1]
            if a < b:   # If they are in the wrong order, swap them and set flag
                items[i] = b
                items[i-1] = a
                swapped = True
        startIndex = startIndex + 1 # An item was pushed to the first index so we can skip that next iteration

# Place items in the correct location in the sorted portion of the list list starting with the second
def insertionSort(items):
    for i in range(1, len(items)): # For each item starting at the second
        j = i
        while j > 0 and items[j-1] > items[j]: # Move it backwards in the array until it is right compared to the left item
            a = items[j]
            b = items[j-1]
            items[j] = b
            items[j-1] = a
            j = j-1

# Recursively sort small lists and zip the smaller lists together
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
def patienceSort(items):
    stacks = [] # We will make stacks of items held here
    for i in range(len(items)):
        placed = False
        for stack in stacks: # Put each item either on the top or bottom of a stack in order or make a new stack
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
   

if __name__ == "__main__":
    arrayLength = 10000
    sortTrials = 10

    arrayLengths = []
    arrayLengths.append(100)
    arrayLengths.append(1000)
    arrayLengths.append(10000)

    arrayModes = {}
    arrayModes["Ideal\t"] = idealArray
    arrayModes["Modified"] = modifiedArray
    arrayModes["Approx\t"] = approxArray
    arrayModes["Random\t"] = randomArray
    arrayModes["Reverse"] = reversedArray

    algorithms = {}
    algorithms["Bubble Sort"] = bubbleSort
    algorithms["Shaker Sort"] = shakerSort
    algorithms["Insertion Sort"] = insertionSort
    algorithms["Merge Sort"] = mergeSort

    algorithms["Patience Sort"] = patienceSort

    for a in algorithms:
        for l in arrayLengths:
            for m in arrayModes:
                startTimer = time.time();
                for i in range(sortTrials):
                    algorithms[a](arrayModes[m](l));
                endTimer = time.time();
                print a, "\t", l, "\t", m, "\t", 100*(endTimer - startTimer)
        print
