from cmu_112_graphics import *
import math


def appStarted(app):
    app.rows = 10
    app.cols = 10

    app.tileWidth = app.width//app.rows
    app.tileHeight = app.height//app.cols
    app.isoTileWidth = 1.25
    app.totalWidth= 3
    app.startTotalHeight = 4.5
    app.totalHeight = app.startTotalHeight
    app.currentLocation = (0, 0)

    app.colors = [([0] * app.cols) for row in range(app.rows)]
    app.currentGreenX = 0
    app.currentGreenY = 0
    app.rotateMode = False
    app.panMode = False
    app.rotationMatrix = [[math.cos(0), - math.sin(0)],
                          [math.sin(0),   math.cos(0)]]
    
    app.isoMatrix = [[app.isoTileWidth/app.totalWidth, app.isoTileWidth/app.totalWidth],
                     [-app.isoTileWidth/app.totalHeight, app.isoTileWidth/app.totalHeight]]

    app.transformation = [[math.sqrt(3)/5, 0/5],
                          [1/5, 2/5]]
    #app.transformation = matrixMultiply(app.transformation, app.isoMatrix)

def keyPressed(app, event):
    if event.key == 'Down':
        if app.currentGreenY < app.cols - 1:
            app.currentGreenY += 1  
            changeColor(app, app.currentGreenX, app.currentGreenY) 

    elif event.key == 'Up':
        if app.currentGreenY > 0:
            app.currentGreenY -= 1 
            changeColor(app, app.currentGreenX, app.currentGreenY) 

    elif event.key == 'Right':
        if app.currentGreenX < app.rows - 1:
            app.currentGreenX += 1
            changeColor(app, app.currentGreenX, app.currentGreenY) 

    elif event.key == 'Left':
        if app.currentGreenX > 0:
            app.currentGreenX -= 1
            changeColor(app, app.currentGreenX, app.currentGreenY)
    
    elif event.key == 'p':
        app.panMode = not app.panMode
        app.rotateMode = False
    
    elif event.key == 'r':
        app.rotateMode = not app.rotateMode
        app.panMode = False


def timerFired(app):
    pass

def mousePressed(app, event):
    app.currentLocation = (event.x, event.y)
    pass

def mouseDragged(app, event):
    if app.panMode:
        locationChange = (app.currentLocation[0] - event.x,  event.y - app.currentLocation[1])
        print(locationChange)
        app.tempTotalHeight = app.totalHeight - locationChange[1]//25
        print(app.tempTotalHeight)
        if 1/app.tempTotalHeight > 0 and 1/app.tempTotalHeight <= 1/app.startTotalHeight:
            app.totalHeight = app.tempTotalHeight
            app.isoMatrix = [[app.isoTileWidth/app.totalWidth, app.isoTileWidth/app.totalWidth],
                     [-app.isoTileWidth/app.totalHeight, app.isoTileWidth/app.totalHeight]]
    elif app.rotateMode:
        theta = getAngle(app, event)
        app.rotationMatrix = [[math.cos(theta), - math.sin(theta)],
                              [math.sin(theta),   math.cos(theta)]]

def getAngle(app, event):
    cx = app.width/2
    cy = app.height/2
    leg1 = cx - event.x
    leg2 = cy - event.y
    hypo = math.sqrt(leg1**2 + leg2**2)
    angle = math.sin(leg1/hypo)
    return angle

def changeColor(app, currentX, currentY):
    app.colors = [([0] * app.cols) for row in range(app.rows)]
    app.colors[currentX][currentY] = 1

def drawBoard(app, canvas):
    canvas.create_oval(0, app.height/app.cols, app.width, 
                        app.height - 30, 
                        fill = '#9CD3DB', outline = '#a9edff')
    for row in range(app.rows):
        for col in range(app.cols):
            x0 = row*app.tileWidth
            y0 = col*app.tileWidth
            x1 = (row + 1)*app.tileWidth
            y1 = (col + 1)*app.tileHeight
            color = '#9CD3DB'
            placeTile(app, x0, y0, x1, y1, canvas, 
                    color)

def placeTile(app, x0, y0, x1, y1, canvas, color):

    isox0, isoy0 = getIsoCoordinates(app, x0, y0)
    isox0, isoy0 = isox0 - app.width/2, isoy0 - app.height/2
    rotation = matrixMultiply(app.rotationMatrix, [[isox0], [isoy0]])
    isox0, isoy0 = rotation[0][0], rotation[1][0]
    isox0, isoy0 = isox0 + app.width/2, isoy0 + app.height/2
    isox0, isoy0 = isox0 - 415/2, isoy0 - 480/2

    
    isox1, isoy1 = getIsoCoordinates(app, x1, y0)
    isox1, isoy1 = isox1 - app.width/2, isoy1 - app.height/2  
    rotation = matrixMultiply(app.rotationMatrix, [[isox1], [isoy1]])
    isox1, isoy1 = rotation[0][0], rotation[1][0]
    isox1, isoy1 = isox1 + app.width/2, isoy1 + app.height/2
    isox1, isoy1 = isox1 - 415/2, isoy1 - 480/2


    isox2, isoy2 = getIsoCoordinates(app, x1, y1)
    isox2, isoy2 = isox2 - app.width/2, isoy2 - app.height/2    
    rotation = matrixMultiply(app.rotationMatrix, [[isox2], [isoy2]])
    isox2, isoy2 = rotation[0][0], rotation[1][0]
    isox2, isoy2 = isox2 + app.width/2, isoy2 + app.height/2
    isox2, isoy2 = isox2 - 415/2, isoy2 - 480/2

    
    isox3, isoy3 = getIsoCoordinates(app, x0, y1)
    isox3, isoy3 = isox3 - app.width/2, isoy3 - app.height/2    
    rotation = matrixMultiply(app.rotationMatrix, [[isox3], [isoy3]])
    isox3, isoy3 = rotation[0][0], rotation[1][0]
    isox3, isoy3 = isox3 + app.width/2, isoy3 + app.height/2
    isox3, isoy3 = isox3 - 415/2, isoy3 - 480/2


    canvas.create_polygon(isox0, isoy0, isox1, isoy1,
                          isox2, isoy2, isox3, isoy3, 
                          fill = color, outline = '#a9edff')
    canvas.create_text(isox0, isoy0, text= f'{isox0//1}, {isoy0//1}', 
                       font="Sans 8", anchor = 'center')
    canvas.create_text(isox1, isoy1, text= f'{isox1//1}, {isoy1//1}', 
                       font="Sans 8", anchor = 'center')
    canvas.create_text(isox2, isoy2, text= f'{isox2//1}, {isoy2//1}', 
                       font="Sans 8", anchor = 'center')
    canvas.create_text(isox3, isoy3, text= f'{isox3//1}, {isoy3//1}', 
                       font="Sans 8", anchor = 'center')

def getIsoCoordinates(app, x, y):
    x_grid = app.width/2 + app.isoTileWidth*(x - y)/app.totalWidth
    y_grid = app.height/2 + app.isoTileWidth*(x + y)/app.totalHeight
    
    stretching = matrixMultiply(app.transformation, [[x], [y]])
    x_grid, y_grid = stretching[0][0] + app.width/2, stretching[1][0] + app.height/2

    return(x_grid, y_grid)

def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

def matrixMultiply(m1,m2):
    #get the sizes of both lists
    m1Rows, m1Cols = len(m1), len(m1[0])
    m2Rows, m2Cols = len(m2), len(m2[0])
    #if the dimensions don't match for matrix multiplication, return None
    if m1Cols != m2Rows:
        return None
    #make a new list, loop through the rows of m1 and cols of m2
    newMatrix = make2dList(m1Rows, m2Cols)
    for i in range(m1Rows):
        for j in range(m2Cols):
            dotProduct = 0
            #loop through each index in the row/column and add to dot product
            for k in range(m1Cols):
                dotProduct += m1[i][k] * m2[k][j]
            #add the dotproduct to the ij'th position of the new matrix
            newMatrix[i][j] = dotProduct
    return newMatrix

def calculateAngle(app, x, y):
    cx = app.width/2
    cy = app.height/2
    leg1 = abs(y - cy)
    leg2 = abs(x - cx)
    hypo = math.sqrt(leg1**2 + leg2**2)
    
    return math.sin(leg2/hypo)
    
def redrawAll(app, canvas):
    drawBoard(app, canvas)

runApp(width=1200, height=1200) 




