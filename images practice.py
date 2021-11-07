from cmu_112_graphics import *


def appStarted(app):
    url = 'https://www.freepnglogos.com/uploads/dna-png/dna-profiling-esr-12.png'
    app.image1 = app.loadImage(url)

def keyPressed(app, event):
    pass

def timerFired(app):
    pass

def mousePressed(app, event):
    pass

def redrawAll(app, canvas):
    canvas.create_image(app.width//2, app.height//2, image=
                        ImageTk.PhotoImage(app.image1))

runApp(width=1200, height=1200)