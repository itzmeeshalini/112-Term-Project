# Major parts of the project to get working:
# Get 3 different types of good cells

from cmu_112_graphics import *
import random
import math

class GoodCell(object):
    
    def __init__(self, app, name, pointValue, imgUrl):
        self.name = name
        self.pointValue = pointValue
        self.imgUrl = imgUrl
        self.image = app.loadImage(imgUrl)
        self.image = app.scaleImage(self.image, 1/8)

def appStarted(app):
    app.rows = 15
    app.cols = 15
    app.tileWidth = app.width//app.rows
    app.tileHeight = app.height//app.cols

    app.colors = [([0] * app.cols) for row in range(app.rows)]
    app.currentGreenX = random.randint(0, app.cols)
    app.currentGreenY = 0
    #app.colors[app.currentGreenX][app.currentGreenY] = 1
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
    
    app.cardWidth = 75
    app.cardHeight = 90
    app.cardImgWidth = 15
    app.cardImgHeight = 15

    app.atp = []
    app.collectedATP = 0
    
    app.rotationMatrix = [[math.cos(0), - math.sin(0)],
                          [math.sin(0),   math.cos(0)]]
    
    app.goodCells = []
    app.goodCells.append(GoodCell(app, "good cell 1", 25, "cell.jpeg"))
    app.goodCells.append(GoodCell(app, "good cell 2", 50, "cell.jpeg"))
    app.goodCells.append(GoodCell(app, "good cell 3", 75, "cell.jpeg"))


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
        if app.currentGreenY < (app.cols - 2):
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

        #checking if mouse click is in an atp
        if ((event.x >= atp[0] - halfWidth and event.x <= atp[0] + halfWidth) and 
            (event.y >= atp[1] - halfHeight and event.y <= atp[1] + halfHeight)):
            app.atp.pop(i)
            print(app.atp)
            app.collectedATP += 25
        else:
            i += 1

def placeATP(app):
    randomx = random.randint(0, app.width)
    randomy = 0
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
    canvas.create_image(50, 50, image=ImageTk.PhotoImage(app.atpImage))
    font = 'Sans 18'
    canvas.create_text(45, 50 + 40, text= str(app.collectedATP), 
                       font=font, anchor = 'center')

def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, 
              x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, 
              x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, 
              x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, 
              x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)

def drawTopBar(app, canvas):
    startX, startY = 5, 5
    endX, endY = 500, 105
    height, width = endX - startX, endY - startY
    round_rectangle(canvas, startX, startY, endX, endY, fill = '#BB8D6F')
    drawCollectedATP(app, canvas)
    for i in range(len(app.goodCells)):
        goodCell = app.goodCells[i]
        drawGoodCellCard(goodCell, app, canvas, 80 + i*app.cardWidth, startY + 5)
    
def drawGoodCellCard(goodCell, app, canvas, x, y):
    if app.collectedATP < goodCell.pointValue:
        color = '#D3D3D3'
    else: color = 'white'
    round_rectangle(canvas, x + 5, y, x + app.cardWidth, y + app.cardHeight, r = 10, fill = color)
    font = 'Sans 12'
    #canvas.create_image(x, y, image=ImageTk.PhotoImage(goodCell.image))
    canvas.create_text(x + app.cardWidth/2, y + app.cardHeight - 25, text= str(goodCell.name), 
                       font=font, anchor = 'center')
    canvas.create_text(x + app.cardWidth/2, y + app.cardHeight - 10, text= str(goodCell.pointValue), 
                       font=font, anchor = 'center')
    

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
    drawTopBar(app, canvas)

runApp(width=1200, height=1200)

# "zombies" are oncogenes
# if good, functioning genes come into contact with the oncogenes, 
# then there is a faster rate of them making mistakes and causing 
# more mutations, which produce more oncogenes
# or, the good genes also turn into mutated genes to fight the remaining bad genes
# each time the dna repairing 