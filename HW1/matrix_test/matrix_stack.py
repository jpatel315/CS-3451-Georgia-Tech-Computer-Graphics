# Matrix Stack Library

# you should modify the routines below to complete the assignment

class Stack(object):

    def __init__(self):
        self.__storage = []

    def push(self, item):
        self.__storage.append(item)

    def peek(self):
        return self.__storage[len(self.__storage) - 1]

    def pop(self):
        if len(self.__storage) == 1:
            print("cannot pop the matrix stack")
        else:
            self.__storage.pop()

    def updateTop(self, newArr):
        top = self.peek()
        for i in range(4):
            for j in range(4):
                top[i][j] = newArr[i][j]

    def clear(self):
        self.__storage = []

stack = Stack()
pi = 3.1415926513589793238462643383

def createIdentity():
    return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

def _createEmpty():
    return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


def multiply(trans, stackMatrix):
    newArray = _createEmpty()
    for i in range(4):
        for j in range(4):
            for k in range(4):
                newArray[i][j] += stackMatrix[i][k] * trans[k][j]
    return newArray

def gtInitialize():
    stack.clear()
    arr = createIdentity()
    stack.push(arr)

def gtPushMatrix():
    arr = stack.peek()
    newCopy = [row[:] for row in arr]
    stack.push(newCopy)

def gtPopMatrix():
    stack.pop()

def gtTranslate(x, y, z):
    trans = createIdentity()
    trans[0][3] = x
    trans[1][3] = y
    trans[2][3] = z
    stack.updateTop(multiply(trans, stack.peek()))


def gtScale(x, y, z):
    trans = createIdentity()
    trans[0][0] = x
    trans[1][1] = y
    trans[2][2] = z
    stack.updateTop(multiply(trans, stack.peek()))
    pass

def gtRotateX(theta):
    theta = theta * pi / 180
    trans = createIdentity()
    cosTheta = cos(theta)
    sinTheta = sin(theta)
    trans[1][1] = cosTheta
    trans[1][2] = -sinTheta
    trans[2][1] = sinTheta
    trans[2][2] = cosTheta
    stack.updateTop(multiply(trans, stack.peek()))

def gtRotateY(theta):
    theta = theta * pi / 180
    trans = createIdentity()
    cosTheta = cos(theta)
    sinTheta = sin(theta)
    trans[0][0] = cosTheta
    trans[0][2] = sinTheta
    trans[2][0] = -sinTheta
    trans[2][2] = cosTheta
    stack.updateTop(multiply(trans, stack.peek()))

def gtRotateZ(theta):
    theta = theta * pi / 180
    trans = createIdentity()
    cosTheta = cos(theta)
    sinTheta = sin(theta)
    trans[0][0] = cosTheta
    trans[0][1] = -sinTheta
    trans[1][0] = sinTheta
    trans[1][1] = cosTheta
    stack.updateTop(multiply(trans, stack.peek()))

def gtGetMatrix():
    pass

def print_ctm():
    arr = stack.peek()
    for line in arr:
        print(line)
    print('') # empty line for readability