from cmu_112_graphics import *


def appStarted(app):
    app.rows = 15
    app.cols = 15

    app.tileWidth = app.width//app.rows
    app.tileHeight = app.height//app.cols

    app.colors = [([0] * app.cols) for row in range(app.rows)]
    app.currentGreenX = 0
    app.currentGreenY = 0
    app.colors[0][0] = 1
    url = 'https://www.freepnglogos.com/uploads/dna-png/dna-profiling-esr-12.png'
    app.image1 = app.loadImage(url)
    app.image1 = app.scaleImage(app.image1, 1/8)

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


def timerFired(app):
    pass

def mousePressed(app, event):
    pass

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
                placeTile(app, x0, y0, x1, y1, canvas, 'white')
                x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2)
                canvas.create_image(x, y, image=
                        ImageTk.PhotoImage(app.image1))

            else:
                color = '#9CD3DB'
                placeTile(app, x0, y0, x1, y1, canvas, 
                    color)

def placeTile(app, x0, y0, x1, y1, canvas, color):

    isox0, isoy0 = getIsoCoordinates(app, x0, y0)
    isox1, isoy1 = getIsoCoordinates(app, x1, y0)
    isox2, isoy2 = getIsoCoordinates(app, x1, y1)
    isox3, isoy3 = getIsoCoordinates(app, x0, y1)

    canvas.create_polygon(isox0, isoy0, isox1, isoy1,
                          isox2, isoy2, isox3, isoy3, 
                          fill = color, outline = '#a9edff')

def getIsoCoordinates(app, x, y):
    x_grid = app.width/2 + (x - y)/2
    y_grid = app.height/app.cols + (x + y)/(app.cols/4)

    return(x_grid, y_grid)

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    pass

runApp(width=1200, height=1200)