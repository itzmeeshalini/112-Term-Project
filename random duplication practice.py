from cmu_112_graphics import *
import random


def appStarted(app):
    app.rows = 15
    app.cols = 15

    app.tileWidth = app.width//app.rows
    app.tileHeight = app.height//app.cols

    app.cells = [[app.width, 100, 0]]
    
    url = 'https://www.pngall.com/wp-content/uploads/10/Body-Cell-Vector-PNG-File.png'
    app.image1 = app.loadImage(url)
    app.image1 = app.scaleImage(app.image1, 1/7)
    app.timerDelay = 100
    app.currentTime = 0

def keyPressed(app, event):
    pass

def timerFired(app):
    app.currentTime += app.timerDelay
    for i in range(len(app.cells)):
        cell = app.cells[i]
        cellBirthTime = cell[2]
        cellBirthTime += app.timerDelay
        if (app.currentTime - cellBirthTime) % 500 >= 400:
            duplication(app, cell)
        if (app.currentTime - cellBirthTime) >= 10000:
            death(app, i)
    #print(app.cells)

def mousePressed(app, event):
    pass


def drawCells(app, canvas):
    for cell in app.cells:
        x = cell[0]
        y = cell[1]
        placeCell(app, canvas, x, y)
        #canvas.create_oval(0, app.height/app.cols, app.width, 
                        #app.height - app.height/app.cols, 
                        #fill = '#9CD3DB', outline = '#a9edff')

def placeCell(app, canvas, x, y):
    
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image1))

    pass

def duplication(app, cell):
    cellX = cell[0]
    cellY = cell[1]
    randX = random.randint(0, app.width)
    randY = random.randint(cellY, app.height)
    app.cells.append([randX, randY, 0])
    pass

def death(app, i):
    app.cells.pop(i)

def redrawAll(app, canvas):
    drawCells(app, canvas)
    #canvas.create_image(600, 600, image=ImageTk.PhotoImage(app.image1))

runApp(width=1200, height=1200)