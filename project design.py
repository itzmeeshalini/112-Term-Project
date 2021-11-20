# Major parts of the project to get working:
# Get 3 different types of good cells
# ATP Synthase produces Energy
# DNA Polymerase stops the mutation temporarily 
# in its tracks to try to correct it
# - can turn into a mutation since you use it so early on

from cmu_112_graphics import *
import random
import math
from Enzyme import *
from Mutation import *


def appStarted(app):
    app.rows = 9
    app.cols = 9
    app.tileWidth = app.width//app.rows
    app.tileHeight = app.height//app.cols

    app.colors = [([0] * app.cols) for row in range(app.rows)]
    app.currentGreenX = random.randint(0, app.cols - 1)
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
    
    app.atpImage = app.loadImage('images/sun.png')
    app.atpImage = app.scaleImage(app.atpImage, 1/20)
    app.atpWidth, app.atpHeight = app.atpImage.size
    
    app.cardWidth = 80
    app.cardHeight = 90
    app.cardImgWidth = 15
    app.cardImgHeight = 15

    app.atp = []
    app.collectedATP = 100
    
    app.rotationMatrix = [[math.cos(0), - math.sin(0)],
                          [math.sin(0),   math.cos(0)]]
    
    app.enzymes = []
    app.enzymes.append(Enzyme(app, "ATP Synthase", 25, "images/atp synthase.png", 0, 3, 1/4))
    app.enzymes.append(Enzyme(app, "DNA Polymerase", 50, "images/cell.jpeg", 1, 3, 1/10))
    app.enzymes.append(Enzyme(app, "Telomerase", 100, "images/cell.jpeg", 2, 3, 1/10))
    app.enzymes.append(["Shovel", 0, 0])

    for i in range(len(app.enzymes)):
        enzyme = app.enzymes[i]
        if isinstance(enzyme, Enzyme):
            enzyme.setPosition(80 + i*app.cardWidth, 5 + 5)
        else:
            enzyme[1], enzyme[2] = 80 + i*app.cardWidth, 5 + 5
        
    app.boardEnzymes = []
        
    app.mutations = []
    
    app.dragCard = False
    app.enzymeX = 0
    app.enzymeY = 0
    app.enzyme = None
    
    app.messageBoxWidth = 200
    app.messageBoxHeight = 300
    
    app.directions = [(-1, 0), (+1, 0), (0, +1), (0, -1)]
    
    app.shovelImage = app.loadImage('images/shovel.png')
    app.shovelImage = app.scaleImage(app.shovelImage, 1/30)
    app.shovelImage = app.shovelImage.transpose(Image.FLIP_LEFT_RIGHT)

def getSprites(app, strip):
    sprites = [ ]
    for i in range(6):
        sprite = strip.crop((7.5+65*i, 7.5, 57.5+65*i, 62.5))
        sprites.append(sprite)
    return sprites

def keyPressed(app, event):
    if event.key == 'Down':
        if app.currentGreenY < app.cols - 1:
            app.colors[app.currentGreenX][app.currentGreenY] = 0
            app.currentGreenY += 1
            app.colors[app.currentGreenX][app.currentGreenY] = 1

    elif event.key == 'Up':
        if app.currentGreenY > 0:
            app.colors[app.currentGreenX][app.currentGreenY] = 0
            app.currentGreenY -= 1
            app.colors[app.currentGreenX][app.currentGreenY] = 1
        
    elif event.key == 'Right':
        if app.currentGreenX < app.rows - 1:
            app.colors[app.currentGreenX][app.currentGreenY] = 0
            app.currentGreenX += 1
            app.colors[app.currentGreenX][app.currentGreenY] = 1

    elif event.key == 'Left':
        if app.currentGreenX > 0:
            app.colors[app.currentGreenX][app.currentGreenY] = 0
            app.currentGreenX -= 1
            app.colors[app.currentGreenX][app.currentGreenY] = 1

def timerFired(app):
    app.currentTime += app.timerDelay
    for enzyme in app.boardEnzymes:
        if isinstance(enzyme, Enzyme):
            enzyme[0].updateTime()
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    if app.currentTime % 5000 == 0:
        print("updating")
        updateMutationLocation(app, app.currentGreenX, app.currentGreenY + 1)

    if app.currentTime % 8000 == 200:
        randomx = random.randint(0, app.width)
        randomy = 400
        placeATP(app, randomx, randomy)
    
    for atp in app.atp:
        if atp[1] <= app.width:
            atp[1] += 1
    
    for enzyme in app.enzymes:
        if isinstance(enzyme, Enzyme):
            if app.collectedATP >= enzyme.pointValue:
                enzyme.notEnoughATP = False
            else: enzyme.notEnoughATP = True
    
    for enzyme in app.boardEnzymes:
        if isinstance(enzyme, Enzyme):
            if enzyme[0].name == "ATP Synthase" and enzyme[0].time % 10000 == 0:
                placeATP(app, enzyme[1], enzyme[2])
            
def mousePressed(app, event):
    index = checkMouseInCard(app, event)
    print(index, type(app.enzyme))
    if index != None and (app.enzyme == None or isinstance(app.enzyme, Enzyme) or isinstance(app.enzyme, list)): 
        app.enzyme = app.enzymes[index]
        if (app.enzyme == None or isinstance(app.enzyme, Enzyme)):
            app.enzymeX = app.enzyme.x
            app.enzymeY = app.enzyme.y
        elif app.enzyme == None or not isinstance(app.enzyme, Enzyme):
            app.enzymeX = app.enzyme[1]
            app.enzymeY = app.enzyme[2]
        app.dragCard = True
        print(app.dragCard)
        
    i = 0
    while (i < len(app.atp)):
        atp = app.atp[i]
        halfWidth = app.atpWidth//2
        halfHeight = app.atpHeight//2

        #checking if mouse click is in an atp
        if ((event.x >= atp[0] - halfWidth and event.x <= atp[0] + halfWidth) and 
            (event.y >= atp[1] - halfHeight and event.y <= atp[1] + halfHeight)):
            app.atp.pop(i)
            app.collectedATP += 25
        else:
            i += 1

def mouseDragged(app, event):
    
    if (not isinstance(app.enzyme, Enzyme) and app.dragCard and 
        (event.x >= 0 and event.x < app.width) and 
        (event.y >= 0 and event.y < app.height)):
        app.enzymeX, app.enzymeY = event.x - app.cardWidth//2, event.y - app.cardHeight//2

    
    elif (app.dragCard and app.enzyme.available and not app.enzyme.notEnoughATP and 
        (event.x >= 0 and event.x < app.width) and 
        (event.y >= 0 and event.y < app.height)):
        app.enzymeX, app.enzymeY = event.x - app.cardWidth//2, event.y - app.cardHeight//2

def mouseReleased(app, event):
    if app.dragCard == True and app.enzyme != None and isinstance(app.enzyme, Enzyme) and app.enzymeY > 200:
        app.enzyme.changeAvailability()
        app.dragCard = False
        app.collectedATP -= app.enzyme.pointValue
        updateBoard(app, event)
            
    elif app.dragCard == True and app.enzyme != None and app.enzyme[0] == "Shovel" and app.enzymeY > 200:
        app.dragCard = False
        updateBoard(app, event)

def updateBoard(app, event):
    x, y = getCartesianCoordinates(app, event.x, event.y)
    print(x, y)
    row, col = getRowCol(app, x, y)

    app.boardEnzymes.append([app.enzyme, event.x, event.y])
    if not isinstance(app.enzyme, Enzyme):
        app.colors[row][col] = 0
    else:
        app.colors[row][col] = app.enzyme
    #app.dragCard = False
            
def checkMouseInCard(app, event):
    for enzyme in app.enzymes:
        if isinstance(enzyme, Enzyme):
            if ((event.x >= enzyme.x and event.x <= enzyme.x + app.cardWidth) and
                (event.y >= enzyme.y and event.y <= enzyme.y + app.cardHeight)):
                print(enzyme.listIndex)
                return enzyme.listIndex
        else:
            if ((event.x >= enzyme[1] and event.x <= enzyme[1] + app.cardWidth) and
                (event.y >= enzyme[2] and event.y <= enzyme[2] + app.cardHeight)):
                return len(app.enzymes) - 1
    return None

def getRowCol(app, x, y):
    col = int(y / app.tileHeight)
    row = int(x / app.tileWidth)
    return(row, col)

def placeATP(app, x, y):
    app.atp.append([x, y])

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

def updateMutationLocation(app, currentX, currentY):
    if app.currentGreenY < (app.cols - 1):
        # drow, dcol = app.directions[random.randint(0, 3)]
        # if ((app.currentGreenX + dcol >= 0 and app.currentGreenX + dcol <= app.cols) and
        if (isinstance(app.colors[currentX][currentY], Enzyme)):
            if app.colors[currentX][currentY].name == "DNA Polymerase":
                app.colors[app.currentGreenX][app.currentGreenY] = 1
        else:
            app.colors[app.currentGreenX][app.currentGreenY] = 0
            app.colors[currentX][currentY] = 1
            app.currentGreenY += 1  
   

def drawBoard(app, canvas):
    canvas.create_oval(0, app.height/app.cols, app.width, 
                        app.height - 20, 
                        fill = '#9CD3DB', outline = '#a9edff')
    for row in range(app.rows):
        for col in range(app.cols):
            x0 = row*app.tileWidth
            y0 = col*app.tileWidth
            x1 = (row + 1)*app.tileWidth
            y1 = (col + 1)*app.tileHeight
            x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2)
            if isinstance(app.colors[row][col], list):
                color = '#9CD3DB'
                placeTile(app, x0, y0, x1, y1, canvas, color)
            elif app.colors[row][col] == 1:
                placeTile(app, x0, y0, x1, y1, canvas, '#9CD3DB')
                point = [[x], [y]]
                point = matrixMultiply(app.rotationMatrix, point)
                sprite = app.sprites[app.spriteCounter]
                canvas.create_image(point[0][0], point[1][0] - 20, image=ImageTk.PhotoImage(sprite))                
            elif app.colors[row][col] == 0:
                color = '#9CD3DB'
                placeTile(app, x0, y0, x1, y1, canvas, color)
            elif isinstance(app.colors[row][col], Enzyme):
                placeTile(app, x0, y0, x1, y1, canvas, color)
                canvas.create_image(x, y - 20, image=ImageTk.PhotoImage(app.colors[row][col].image))                

def drawATP(app, canvas):
    for atp in app.atp:
        canvas.create_image(atp[0], atp[1], image=ImageTk.PhotoImage(app.atpImage))

def drawCollectedATP(app, canvas):
    canvas.create_image(50, 50, image=ImageTk.PhotoImage(app.atpImage))
    font = 'Sans 18'
    canvas.create_text(45, 50 + 40, text= str(app.collectedATP), 
                       font=font, anchor = 'center')

def drawMessageBox(app, canvas):
    x0 = app.width - app.messageBoxWidth - 30
    y0 = 20
    x1 = x0 + app.messageBoxWidth
    y1 = 5 + app.messageBoxHeight
    round_rectangle(canvas, x0, y0, x1, y1, fill = '#BB8D6F')
    canvas.create_rectangle(x0 + 10, y0 + 10, x1 - 10, y1 - 30, fill = '#f7f3f1')
    canvas.create_text(x0 + 10, y1 - 15, text = "MESSAGE BOX", anchor = 'w')

def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, 
              x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, 
              x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, 
              x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, 
              x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)

def drawTopBar(app, canvas):
    startX, startY = 5, 5
    endX, endY = startX + (app.cardWidth + 5)*len(app.enzymes) + 80, 105
    #endX, endY = 500, 105
    height, width = endX - startX, endY - startY
    round_rectangle(canvas, startX, startY, endX, endY, fill = '#BB8D6F')
    drawCollectedATP(app, canvas)
    for i in range(len(app.enzymes)):
        enzyme = app.enzymes[i]
        drawenzymeCard(enzyme, app, canvas, 80 + i*app.cardWidth, startY + 5)
    
def drawenzymeCard(enzyme, app, canvas, x, y):
    if not isinstance(enzyme, Enzyme):        
        color = '#f7f3f1'
        round_rectangle(canvas, x + 5, y, x + app.cardWidth, y + app.cardHeight, r = 10, fill = color)
        font = 'Sans 10'
        canvas.create_image(x + app.cardWidth/2, y + app.cardHeight/2 - 10, image=ImageTk.PhotoImage(app.shovelImage))
        canvas.create_text(x + app.cardWidth/2, y + app.cardHeight - 25, text= "shovel", 
                        font=font, anchor = 'center')
    else:
        if enzyme.available == False:
            color = '#8C9295'
        elif enzyme.notEnoughATP:
            color = '#D3D3D3'
        else: color = '#f7f3f1'
        round_rectangle(canvas, x + 5, y, x + app.cardWidth, y + app.cardHeight, r = 10, fill = color)
        font = 'Sans 10'
        canvas.create_image(x + app.cardWidth/2, y + app.cardHeight/2 - 10, image=ImageTk.PhotoImage(enzyme.image))
        canvas.create_text(x + app.cardWidth/2, y + app.cardHeight - 25, text= str(enzyme.name), 
                        font=font, anchor = 'center')
        canvas.create_text(x + app.cardWidth/2, y + app.cardHeight - 10, text= str(enzyme.pointValue), 
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
    x_grid = app.width/2 + 1.25*(x - y)/3
    y_grid = app.height/app.cols + 1.25*(x + y)/(app.cols/2)
    #print(x_grid, y_grid)
    return(x_grid, y_grid)

def getCartesianCoordinates(app, x_grid, y_grid):
    x = (6*x_grid + app.cols*y_grid - app.height - 3*app.width)/5
    y = (app.cols*y_grid - 6*x_grid - app.height + 3*app.width)/5
    return(x, y)

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawATP(app, canvas)
    drawTopBar(app, canvas)
    drawMessageBox(app, canvas)
    if app.dragCard:
        drawenzymeCard(app.enzyme, app, canvas, app.enzymeX, app.enzymeY)

runApp(width=1200, height=1200)

# "zombies" are oncogenes
# if good, functioning genes come into contact with the oncogenes, 
# then there is a faster rate of them making mistakes and causing 
# more mutations, which produce more oncogenes
# or, the good genes also turn into mutated genes to fight the remaining bad genes
# each time the dna repairing 