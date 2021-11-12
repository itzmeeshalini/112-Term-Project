from cmu_112_graphics import *
import random
import math

def appStarted(app):
    app.rows = 15
    app.cols = 15

    app.tileWidth = app.width//app.rows
    app.tileHeight = app.height//app.cols

    app.colors = [([0] * app.cols) for row in range(app.rows)]
    app.currentGreenX = random.randint(0, app.cols)
    app.currentGreenY = 0
    app.colors[app.currentGreenX][app.currentGreenY] = 1
    url = 'https://www.freepnglogos.com/uploads/dna-png/dna-profiling-esr-12.png'
    app.image1 = app.loadImage(url)
    app.image1 = app.scaleImage(app.image1, 1/8)
    
    url = 'http://www.cs.cmu.edu/~112/notes/sample-spritestrip.png'
    app.spritestrip = app.loadImage(url)
    app.spritestrip = app.scaleImage(app.spritestrip, 1/4)
    app.spritestrip = app.spritestrip.transpose(Image.FLIP_LEFT_RIGHT)

    app.sprites = getSprites(app, app.spritestrip)    
    app.spriteCounter = 0
    app.currentTime = 0
    
    app.atpImage = app.loadImage('sun.png')
    app.atpImage = app.scaleImage(app.atpImage, 1/20)
    app.atpWidth, app.atpHeight = app.atpImage.size

    app.atp = []
    app.collectedATP = 0
    
    app.rotationMatrix = [[math.cos(0), - math.sin(0)],
                      [math.sin(0), math.cos(0)]]

def getSprites(app, strip):
    sprites = [ ]
    for i in range(6):
        sprite = strip.crop((7.5+65*i, 7.5, 57.5+65*i, 62.5))
        sprites.append(sprite)
    return sprites

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
    
    elif event.key == 'r':
        app.colors = [([0] * app.cols) for row in range(app.rows)]
        app.currentGreenX = random.randint(0, app.cols)
        app.currentGreenY = 0
        app.colors[app.currentGreenX][app.currentGreenY] = 1

def timerFired(app):
    app.currentTime += app.timerDelay
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    if app.currentTime % 3000 == 0:
        if app.currentGreenY < app.cols - 1:
            app.currentGreenY += 1  
            changeColor(app, app.currentGreenX, app.currentGreenY)
    
    if app.currentTime == 2000 or app.currentTime % 8000 == 0:
        placeATP(app)
    
    for atp in app.atp:
        if atp[1] <= app.width:
            atp[1] += 1
    
def mousePressed(app, event):
    i = 0
    while (i < len(app.atp)):
        atp = app.atp[i]
        halfWidth = app.atpWidth//2
        halfHeight = app.atpHeight//2

        if ((event.x >= atp[0] - halfWidth and event.x <= atp[0] + halfWidth) and 
            (event.x >= atp[0] - halfHeight and event.x <= atp[0] + halfHeight)):
            app.atp.pop(i)
            print(app.atp)
            app.collectedATP += 1
        else:
            i += 1

def placeATP(app):
    randomx = random.randint(0, app.width)
    randomy = 20
    app.atp.append([randomx, randomy])

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

def changeColor(app, currentX, currentY):
    app.colors = [([0] * app.cols) for row in range(app.rows)]
    app.colors[currentX][currentY] = 1

def drawBoard(app, canvas):
    canvas.create_oval(0, app.height/app.cols, app.width, 
                        app.height - app.height/app.cols, 
                        fill = '#9CD3DB', outline = '#a9edff')
    for row in range(app.rows):
        for col in range(app.cols):
            x0 = row*app.tileWidth
            y0 = col*app.tileWidth
            x1 = (row + 1)*app.tileWidth
            y1 = (col + 1)*app.tileHeight
            if app.colors[row][col] == 1:
                placeTile(app, x0, y0, x1, y1, canvas, '#9CD3DB')
                x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2)
                point = [[x], [y]]
                point = matrixMultiply(app.rotationMatrix, point)
                sprite = app.sprites[app.spriteCounter]
                canvas.create_image(point[0][0], point[1][0] - 20, image=ImageTk.PhotoImage(sprite))


            else:
                color = '#9CD3DB'
                placeTile(app, x0, y0, x1, y1, canvas, 
                    color)

def drawATP(app, canvas):
    for atp in app.atp:
        canvas.create_image(atp[0], atp[1], image=ImageTk.PhotoImage(app.atpImage))

def drawCollectedATP(app, canvas):
    canvas.create_rectangle(5, 5, 230, 80)
    canvas.create_image(50, 40, image=ImageTk.PhotoImage(app.atpImage))
    font = 'Sans 18'
    canvas.create_text(50 + 30,  40, text= "ATP Collected: " + str(app.collectedATP), 
                       font=font, anchor = 'w')
    

def placeTile(app, x0, y0, x1, y1, canvas, color):

    isox0, isoy0 = getIsoCoordinates(app, x0, y0)
    rotation = matrixMultiply(app.rotationMatrix, [[isox0], [isoy0]])
    isox0, isoy0 = rotation[0], rotation[1]
    
    isox1, isoy1 = getIsoCoordinates(app, x1, y0)
    rotation = matrixMultiply(app.rotationMatrix, [[isox1], [isoy1]])
    isox1, isoy1 = rotation[0], rotation[1]
    
    isox2, isoy2 = getIsoCoordinates(app, x1, y1)
    rotation = matrixMultiply(app.rotationMatrix, [[isox2], [isoy2]])
    isox2, isoy2 = rotation[0], rotation[1]
    
    isox3, isoy3 = getIsoCoordinates(app, x0, y1)
    rotation = matrixMultiply(app.rotationMatrix, [[isox3], [isoy3]])
    isox3, isoy3 = rotation[0], rotation[1]

    canvas.create_polygon(isox0, isoy0, isox1, isoy1,
                          isox2, isoy2, isox3, isoy3, 
                          fill = color, outline = '#a9edff')

def getIsoCoordinates(app, x, y):
    x_grid = app.width/2 + (x - y)/2.1
    y_grid = app.height/app.cols + (x + y)/(app.cols/4)

    return(x_grid, y_grid)

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawATP(app, canvas)
    drawCollectedATP(app, canvas)

runApp(width=1200, height=1200)