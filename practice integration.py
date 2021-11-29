from cmu_112_graphics import *
import random
import math
from Enzyme import *
from Mutation import *
import ast

##########################################
# CITATIONS

# Matrix multiply method came from one of my previous homeworks
# rotation and projection adapted from: https://math.stackexchange.com/questions/296794/
    # finding-the-transform-matrix-from-4-projected-points-with-javascript/339033#339033
# image citations:
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.chegg.com%2Fhomework-help%2F
    # questions-and-answers%2Fconditions-illustrated-might-atp-synthase-operate-reverse-
    # using-energy-atp-hydrolysis-pump-q46619862&psig=AOvVaw1XjrQ3E4hTBzwWkbTg1w-2&ust=
    # 1637789636530000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCJiMi_63r_QCFQAAAAAdAAAAABAE

    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fmicrobenotes.com%2Fdna-polymerase
    # %2F&psig=AOvVaw1Rq5088FFLPW-qYsXIJSG7&ust=1637789747947000&source=images&cd=vfe&ved=
    # 0CAsQjRxqFwoTCMi6_rK4r_QCFQAAAAAdAAAAABAD
    
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fflexbooks.ck12.org%2Fcbook%2Fck-12-
    # biology-flexbook-2.0%2Fsection%2F1.17%2Fprimary%2Flesson%2Fenzymes-bio%2F&psig=AOvVaw0
    # GeDJR1JxQEVYQeMrZkAUq&ust=1637789835326000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLDey
    # ty4r_QCFQAAAAAdAAAAABAD

##########################################
# Home Screen Mode
##########################################

def homeScreenMode_redrawAll(app, canvas):
    font = 'Sans 26'
    canvas.create_text(app.width/2, 150, text='Play Enzymes vs. Mutations!', font=font)
    drawButtons(app, canvas)

def homeScreenMode_keyPressed(app, event):
    app.mode = 'gameMode'

def homeScreenMode_mousePressed(app, event):
    cx, cy = app.width//2, app.height//2
    if ((cx - app.margin - app.buttonWidth <= event.x <= cx - app.margin) and 
        (cy + 20 <= event.y <= cy + 20 + app.buttonHeight//2)):
        app.mode = 'loginMode'
    elif ((cx + app.margin <= event.x <= cx + app.margin + app.buttonWidth) and 
        (cy + 20 <= event.y <= cy + 20 + app.buttonHeight//2)):
        app.mode = 'signupMode'
        
def drawButtons(app, canvas):
    cx, cy = app.width//2, app.height//2
    canvas.create_rectangle(cx - app.margin - app.buttonWidth, cy + 20, cx - app.margin, cy + 20 + app.buttonHeight)
    canvas.create_text(cx - app.margin - app.buttonWidth//2, cy + 20 + app.buttonHeight//2, 
                       text = "Returning Player", font = 'Sans 14', anchor = 'center')
    canvas.create_rectangle(cx + app.margin, cy + 20, cx + app.margin + app.buttonWidth, cy + 20 + app.buttonHeight)
    canvas.create_text(cx + app.margin + app.buttonWidth//2, cy + 20 + app.buttonHeight//2, 
                       text = "New Player", font = 'Sans 14', anchor = 'center')
        
##########################################
# Login Screen
##########################################

def loginMode_redrawAll(app, canvas):
    font = 'Sans 26'
    canvas.create_text(app.width/2, 150, text='Login Mode!', font=font)

def loginMode_mousePressed(app, event):
    username = app.getUserInput('Username')
    if (username == None):
        app.mode = 'homeScreenMode'
    while username not in app.loginsDict:
        app.showMessage("That username does not exist")
        username = app.getUserInput('Username')
        if (username == None):
            app.mode = 'homeScreenMode'
            break
    else:
        password = app.getUserInput('Password')
        if (password == None):
            app.mode = 'homeScreenMode'
        while(password != app.loginsDict[username][0]):
            app.showMessage("You entered the wrong password")
            password = app.getUserInput('Incorrect password. Enter it again.')
            if (password == None):
                app.mode = 'homeScreenMode'
                break
        app.mode = 'playerMode'
        app.user = username
        app.level = app.loginsDict[app.user][1]
        print(app.level)


    
##########################################
# Sign Up Screen
##########################################

def signupMode_redrawAll(app, canvas):
    font = 'Sans 26'
    canvas.create_text(app.width/2, 150, text='Sign Up Mode!', font=font)
    
def signupMode_mousePressed(app, event):
    username = app.getUserInput('Enter a username')
    if (username == None):
        app.mode = 'homeScreenMode'
    while username in app.loginsDict:
        username = app.getUserInput('That username already exists. Enter another username')
    password1 = app.getUserInput('Enter a strong password')
    if (password1 == None):
        app.mode = 'homeScreenMode'
    password2 = app.getUserInput('Enter your password again')
    if (password2 == None):
        app.mode = 'homeScreenMode'
    while (password2 != password1):
        password2 = app.getUserInput('The passwords did not match. Enter it again.')
        
    level = 1
    app.loginsDict[username] = [password2, level]

    f = open("logins.txt","w")
    f.write( str(app.loginsDict) )
    f.close()
    
    app.user = username
    app.mode = 'playerMode'
    app.level = app.loginsDict[app.user][1]
    print(app.level)
    
##########################################
# Player Screen
##########################################

def playerMode_redrawAll(app, canvas):
    font = 'Sans 26'
    canvas.create_text(app.width/2, 150, text=f'Hello {app.user}!', font=font)
    canvas.create_text(app.width/2, 175, text=f'You are on level {app.level}!', font=font)
    canvas.create_text(app.width/2, 200, text='Press a key to play!', font=font)

def playerMode_keyPressed(app, event):
    app.mode = 'gameMode'


##########################################
# Win Screen
##########################################

def winMode_redrawAll(app, canvas):
    font = 'Sans 26'
    canvas.create_text(app.width/2, 150, text='You Win!', font=font)
    canvas.create_text(app.width/2, 200, text='Press a key for the next level!', font=font)

def winMode_keyPressed(app, event):
    app.mode = 'gameMode'
    app.mutationsKilled = 0
    app.level += 1
    app.loginsDict[app.user][1] = app.level
    f = open("logins.txt","w")
    f.write( str(app.loginsDict) )
    f.close()
    resetConfigs(app)
    
##########################################
# Lose Screen
##########################################

def loseMode_redrawAll(app, canvas):
    font = 'Sans 26'
    canvas.create_text(app.width/2, 150, text='Aww man! You lose', font=font)
    canvas.create_text(app.width/2, 200, text='Press a key to redo level!', font=font)

def loseMode_keyPressed(app, event):
    app.mode = 'gameMode'
    app.mutationsKilled = 0
    resetConfigs(app)

##########################################
# Game Mode
##########################################

#GIANT timer fired program...may need to break it up into smaller functions
def gameMode_timerFired(app):
    app.rotation_z = [[math.cos(app.angle), -math.sin(app.angle), 0],
                  [math.sin(app.angle), math.cos(app.angle), 0],
                  [0, 0 ,1]]
    
    #update current time and time for each enzyme
    #print(app.currentTime)
    app.currentTime += app.timerDelay
    
    checkWin(app, app.currentTime)
    checkLose(app)
    
    if app.winTime != None:        
        app.mode = 'winMode'
    #update the sprite image
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    
    #update the mutation location after a certain interval
    
    
    for mutation in app.mutations:
        if mutation.hits <= 0:
            app.board[mutation.row][mutation.col] = 0
            app.mutations.remove(mutation)
            app.mutationsKilled += 1
        if app.currentTime % app.mutationTime == 100:
            updateMutationLocation(app, mutation, mutation.row, mutation.col + 1)
        
    addNewMutation(app)
    #add an atp after a certain interval
    addNewATP(app)
    #update the atp location after each call to move it
    updateATPLocation(app)
    shootAtMutation(app)

    
    #constantly checks if the enzymes have enough atp and changes availability if not
    
    for enzyme in app.enzymes:
        checkEnoughATP(app, enzyme)
    
    #basically just does different things at different times for each enzyme group
    #by looping through all the different enzymes on the board
    for enzyme in app.boardEnzymes:
        if isinstance(enzyme[0], Enzyme):
            enzyme[0].updateTime()
            #if atp synthase, then place atp sporadically
            if enzyme[0].name == "ATP Synthase":
                atpSynthaseFunction(app, enzyme)

            #if dna polymerase, then lower duration
            if enzyme[0].name == "DNA Polymerase":
                dnaPolyFunction(app, enzyme)
            
            #if caspase, then shoot a ball after a certain time
            if enzyme[0].name == "Caspase":
                caspaseFunction(app, enzyme)
            
            if enzyme[0].name == "Star Shooter":
                starShooterFunction(app)
                
#function that takes care of what happens when mouse is pressed
#checks if user is collecting atp or moving a card
def gameMode_mousePressed(app, event):
    
    checkLogOutButton(app, event)
    
    index = checkMouseInCard(app, event)
    #print(index, type(app.enzyme))
    
    #this chunk takes care of whether or not an enzyme is being moved right now
    if index != None and (app.enzyme == None or isinstance(app.enzyme, Enzyme) or isinstance(app.enzyme, list)): 
        app.enzyme = app.enzymes[index]
        if (app.enzyme == None or isinstance(app.enzyme, Enzyme)):
            app.enzymeX = app.enzyme.x
            app.enzymeY = app.enzyme.y
        elif app.enzyme == None or not isinstance(app.enzyme, Enzyme):
            app.enzymeX = app.enzyme[1]
            app.enzymeY = app.enzyme[2]
        app.dragCard = True
        #print(app.dragCard)
        
    #this loop checks if the user is collecting atp and removes it from the list of atp locations
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

#function that takes care of what happens when mouse is dragged
def gameMode_mouseDragged(app, event):
    #if it's the shovel, then just draw it
    if (not isinstance(app.enzyme, Enzyme) and app.dragCard and 
        (event.x >= 0 and event.x < app.width) and 
        (event.y >= 0 and event.y < app.height)):
        app.enzymeX, app.enzymeY = event.x - app.cardWidth//2, event.y - app.cardHeight//2

    #if it's an enzyme, make sure you're able to drag it
    elif (app.dragCard and app.enzyme.available and not app.enzyme.notEnoughATP and 
        (event.x >= 0 and event.x < app.width) and 
        (event.y >= 0 and event.y < app.height)):
        app.enzymeX, app.enzymeY = event.x - app.cardWidth//2, event.y - app.cardHeight//2

#function that takes care of what happens when mouse is released
def gameMode_mouseReleased(app, event):
    #doesn't say that the user is dragging the card if mouse is released inside the top bar
    if app.enzymeY < 200:
        app.dragCard = False
        
    #if it's an enzyme, then change dragCard, remove cost from collected atp, 
    #and change the availability of the enzyme group if applicable and update the board
    elif app.dragCard == True and app.enzyme != None and isinstance(app.enzyme, Enzyme) and app.enzymeY > 200:
        app.enzyme.changeAvailability()
        app.dragCard = False
        app.collectedATP -= app.enzyme.pointValue
        updateBoard(app, event)
            
    #if it's the shovel, then only change dragCard and update the board
    elif app.dragCard == True and app.enzyme != None and app.enzyme[0] == "Shovel" and app.enzymeY > 200:
        app.dragCard = False
        print("need to use shovel")
        updateBoard(app, event)

def gameMode_keyPressed(app, event):
    if event.key == 'Right':
        if app.angle <= math.pi//2 + 0.25:
            app.angle += 0.25
    if event.key == 'Left':
        if app.angle >= -math.pi - 0.25:
            app.angle -= 0.25

#different key options for moving the mutation (helping when testing)
# def gameMode_keyPressed(app, event):
#     if event.key == 'Down':
#         if app.currentGreenY < app.cols - 1:
#             app.board[app.currentGreenX][app.currentGreenY] = 0
#             app.currentGreenY += 1
#             app.board[app.currentGreenX][app.currentGreenY] = 1

#     elif event.key == 'Up':
#         if app.currentGreenY > 0:
#             app.board[app.currentGreenX][app.currentGreenY] = 0
#             app.currentGreenY -= 1
#             app.board[app.currentGreenX][app.currentGreenY] = 1
        
#     elif event.key == 'Right':
#         if app.currentGreenX < app.rows - 1:
#             app.board[app.currentGreenX][app.currentGreenY] = 0
#             app.currentGreenX += 1
#             app.board[app.currentGreenX][app.currentGreenY] = 1

#     elif event.key == 'Left':
#         if app.currentGreenX > 0:
#             app.board[app.currentGreenX][app.currentGreenY] = 0
#             app.currentGreenX -= 1
#             app.board[app.currentGreenX][app.currentGreenY] = 1

#calls all the drawing helper functions
def gameMode_redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawATP(app, canvas)
    drawTopBar(app, canvas)
    drawShots(app, canvas)
    drawMessageBox(app, canvas)
    drawLogOutButton(app, canvas)
    #only draws the card on the board if the user is dragging the card
    if app.dragCard:
        drawenzymeCard(app.enzyme, app, canvas, app.enzymeX, app.enzymeY)
    canvas.create_text(20, app.height - 20, text = f'Level {app.level}', anchor = 'w')
    canvas.create_text(20, app.height - 40, text = f'Progress {app.progress}%', anchor = 'w')

##########################################
# Main App
##########################################
class Enzyme(object):
    
    def __init__(self, app, name, pointValue, imgUrl, index, count, scale):
        self.name = name
        self.pointValue = pointValue
        self.imgUrl = imgUrl
        self.image = app.loadImage(imgUrl)
        self.scale = scale
        self.image = app.scaleImage(self.image, scale)
        self.listIndex = index
        self.count = count
        self.times = []
        self.locations = []
        self.images = [self.image]*self.count
        if name == "DNA Polymerase":  
            self.left = []
        
        self.available = True
        self.notEnoughATP = True
        self.x = 0
        self.y = 0
        self.time = 0

    #sets the position in the top bar
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    #changes the availability of the enzyme group
    def changeAvailability(self):
        #self.count -= 1
        self.available = True
        
    #updates the time for each enzyme on the board
    def updateTime(self):
        for i in range(len(self.times)):
            self.times[i] += 100
    
    #changes the image for the object if it needs to be changed
    def setImage(self, app, i, imgUrl):
        image = app.loadImage(imgUrl)
        self.images[i] = app.scaleImage(image, self.scale)

class Mutation(object):
    
    def __init__(self, app, name, imgUrl, hits, x, y, row, col):
        self.name = name
        self.imgUrl = imgUrl
        self.image = app.loadImage(imgUrl)
        self.image = app.scaleImage(self.image, 1/8)
        self.hits = hits
        self.x = x
        self.y = y
        self.row = row
        self.col = col
    
    def getHit(self):
        self.hits -= 1

#sets up all the initial helper variables
def appStarted(app):
    app.loginsDict = dict()
    getLogins(app)
    print(app.loginsDict)

    
    app.user = ""
    app.level = 1
    
    app.buttonWidth = app.width//6
    app.buttonHeight = app.height//20
    app.margin = 20
    app.starShootRowCol = (0, 0)
    app.angle = -1.5
    x_angle = -math.pi/50

    app.rotation_x = [[1, 0, 0], 
                [0, math.cos(x_angle), - math.sin(x_angle)],
                [0, math.sin(x_angle), math.cos(x_angle)]]
    
    
    app.rotation_z = [[math.cos(app.angle), -math.sin(app.angle), 0],
                  [math.sin(app.angle), math.cos(app.angle), 0],
                  [0, 0 ,1]]
    
    app.translation = [[1, 0, -4.5],
                        [0, 1, -4.5], 
                        [0, 0,  1]]
    app.translation_back = [[1, 0, 4.5],
                   [0, 1, 4.5], 
                   [0, 0,  1]]
    
    
    app.mode = 'homeScreenMode'
    #setLevelConfig(app, app.level)
    #setting up board configurations
    app.rows = 9
    app.cols = 9
    app.tileWidth = app.width//app.rows
    app.tileHeight = app.height//app.cols
        
    #setting up sprite configurations
    app.url = 'http://www.cs.cmu.edu/~112/notes/sample-spritestrip.png'
    app.spritestrip = app.loadImage(app.url)
    app.spritestrip = app.scaleImage(app.spritestrip, 1/4)
    app.spritestrip = app.spritestrip.transpose(Image.FLIP_LEFT_RIGHT)
    app.sprites = getSprites(app, app.spritestrip)    
    app.spriteCounter = 0
    app.currentTime = 0
    
    app.timerDelay = 50

    #setting up atp configurations
    app.atpImage = app.loadImage('images/sun.png')
    app.atpImage = app.scaleImage(app.atpImage, 1/20)
    app.atpWidth, app.atpHeight = app.atpImage.size
    app.atp = []
    app.collectedATP = 50
    
    app.ballImage = app.loadImage('images/ball.png')
    app.ballImage = app.scaleImage(app.ballImage, 1/15)
    
    #setting up enzyme card configurations
    app.cardWidth = 80
    app.cardHeight = 90
    app.cardImgWidth = 15
    app.cardImgHeight = 15
    
    #setting up shovel image configurations
    app.shovelImage = app.loadImage('images/shovel.png')
    app.shovelImage = app.scaleImage(app.shovelImage, 1/30)
    app.shovelImage = app.shovelImage.transpose(Image.FLIP_LEFT_RIGHT)

    app.rotationMatrix = [[math.cos(0), - math.sin(0)],
                          [math.sin(0),   math.cos(0)]]
    
    #setting up starting enzyme configurations
    app.enzymes = []
    app.gameEnzymes = [["ATP Synthase", 25, "images/atp synthase.png", 1/4], 
                       ["DNA Polymerase", 50, "images/dna polymerase.png", 1/3], 
                       ["Caspase", 100, "images/caspase.png", 1/7], 
                       ["Star Shooter", 25, "images/atp synthase.png", 1/4]]
    app.availableEnzymeCount = 0


    #setting the position for each card to go in the top bar when I draw it. 
    
        
    #setting up helper lists
    app.boardEnzymes = []
    app.mutations = []
    app.caspaseShoot = []
    app.starShoot = []

    
    #setting up model configurations for the board 
    app.board = [([0] * app.cols) for row in range(app.rows)]
    row = 8
    col = random.randint(0, app.cols - 1)
    x, y = getCoordinates(app, row, col)
    app.mutations.append(Mutation(app, "Normal Mutation", app.url, 5, x, y, row, col))
    app.setNumberMutations = 0
    app.mutationsPassed = 1
    app.mutationsKilled = 0
    app.progress = 0
    app.hits = 0
    app.hitsPerMutation = 0
    app.winTime = None

    
    #helper variables for dragging
    app.dragCard = False
    app.enzymeX = 0
    app.enzymeY = 0
    app.enzyme = None
    
    #setting up message box configurations
    app.messageBoxWidth = 200
    app.messageBoxHeight = 300
    
    generateConfigs(app)
    
    app.totalHits = app.setNumberMutations*app.hitsPerMutation
    app.mutationTime = 2000

    
    for i in range(len(app.enzymes)):
        enzyme = app.enzymes[i]
        if isinstance(enzyme, Enzyme):
            enzyme.setPosition(80 + i*app.cardWidth, 5 + 5)
        else:
            enzyme[1], enzyme[2] = 80 + i*app.cardWidth, 5 + 5
    
def getLogins(app):
    file = open("logins.txt", "r")

    contents = file.read()
    app.loginsDict = ast.literal_eval(contents)

    file.close()

def generateConfigs(app):
    randomSeed = random.seed(app.level)
    app.setNumberMutations = app.level
    if app.level < 10:
        app.hitsPerMutation = 5
    else:
        app.hitsPerMutation = random.randint(app.level//4, app.level//2, randomSeed)
    app.mutationTime = mutationTimeFunction(app.level)
    #if app.level <= 1:
        #app.availableEnzymeCount = 4
    #elif app.level <= 2:
        #app.availableEnzymeCount = 4
    app.availableEnzymeCount = 4
    
    for i in range(app.availableEnzymeCount):
        app.enzymes.append(Enzyme(app, app.gameEnzymes[i][0], app.gameEnzymes[i][1], app.gameEnzymes[i][2], len(app.enzymes), 3, app.gameEnzymes[i][3]))
    app.enzymes.append(["Shovel", 0, 0])


def mutationTimeFunction(x):
    return (0.5)**(x - 10) * 800

def resetConfigs(app):
    app.currentTime = 0
    app.atp = []
    app.collectedATP = 50
    app.rotationMatrix = [[math.cos(0), - math.sin(0)],
                        [math.sin(0),   math.cos(0)]]
    app.progress = 0
    app.enzymes = []

    for i in range(len(app.enzymes)):
        enzyme = app.enzymes[i]
        if isinstance(enzyme, Enzyme):
            enzyme.setPosition(80 + i*app.cardWidth, 5 + 5)
        else:
            enzyme[1], enzyme[2] = 80 + i*app.cardWidth, 5 + 5

    app.boardEnzymes = []
    app.mutations = []
    app.caspaseShoot = []

    #setting up model configurations for the board 
    app.board = [([0] * app.cols) for row in range(app.rows)]
    row = 8
    col = random.randint(0, app.cols - 1)
    x, y = getCoordinates(app, row, col)
    app.mutations.append(Mutation(app, "Normal Mutation", app.url, app.hitsPerMutation, x, y, row, col))
    app.setNumberMutations = app.level
    app.mutationsPassed = 1
    app.mutationsKilled = 0
    app.progress = 0
    app.hits = 0
    app.hitsPerMutation = 5
    app.totalHits = app.setNumberMutations*app.hitsPerMutation
    app.winTime = None


    #helper variables for dragging
    app.dragCard = False
    app.enzymeX = 0
    app.enzymeY = 0
    app.enzyme = None
    
    generateConfigs(app)
    
    app.totalHits = app.setNumberMutations*app.hitsPerMutation

    
    for i in range(len(app.enzymes)):
        enzyme = app.enzymes[i]
        if isinstance(enzyme, Enzyme):
            enzyme.setPosition(80 + i*app.cardWidth, 5 + 5)
        else:
            enzyme[1], enzyme[2] = 80 + i*app.cardWidth, 5 + 5
    

#crops the sprite sheet
def getSprites(app, strip):
    sprites = [ ]
    for i in range(6):
        sprite = strip.crop((7.5+65*i, 7.5, 57.5+65*i, 62.5))
        sprites.append(sprite)
    return sprites

def getCoordinates(app, row, col):
    x0 = row
    y0 = col
    x1 = (row + 1)
    y1 = (col + 1)
    x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2) 
    
    return (x, y)

def find_row_col(app, x, y):
    for row in range(app.rows):
        for col in range(app.cols):
            x0 = row
            y0 = col
            x1 = (row + 1)
            y1 = (col + 1)
            isox1, isoy1 = getIsoCoordinates(app, x0, y0)
            isox2, isoy2 = getIsoCoordinates(app, x1, y0) 
            isox3, isoy3 = getIsoCoordinates(app, x1, y1) 
            isox4, isoy4 = getIsoCoordinates(app, x0, y1)
            
            maxX, minX, maxY, minY = findXYBounds(isox1, isoy1, isox2, isoy2, isox3, isoy3, isox4, isoy4)

            
            if (minX <= x <= maxX and minY <= y <= maxY):
                #print(row, col)
                return row, col
    return -1, -1

def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum = 0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix

    else:
        print("columns of the first matrix must be equal to the rows of the second matrix")
        return None

#updates the model of the board
def updateBoard(app, event):
    #gets the cartesian coordinates of the event (i dont think this is needed)    
    #gets the row and column of the location
    row, col = find_row_col(app, event.x, event.y)
    
    if not isinstance(app.enzyme, Enzyme):
            print("need to remove enzyme")
            removeEnzymeFromBoard(app, app.board[row][col], 0)
            app.board[row][col] = 0

    elif app.board[row][col] == 0:
    #adds a new enzyme to the board since mouse was released
        if row != -1 and col != -1:
            
            app.boardEnzymes.append([app.enzyme, event.x, event.y])
        
        #if the enzyme added was caspase, then start shooting
            if isinstance(app.enzyme, Enzyme) and app.enzyme.name == "Caspase":
                x0 = row
                y0 = col
                x1 = (row + 1)
                y1 = (col + 1)
                x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2)
                app.caspaseShoot.append((x, y)) 
                app.board[row][col] = app.enzyme     
        
            elif isinstance(app.enzyme, Enzyme) and app.enzyme.name == "Star Shooter":
                x0 = row
                y0 = col
                x1 = (row + 1)
                y1 = (col + 1)
                x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2)
                app.starShoot = [(x, y)] * 8
                app.starShootRowCol = (x0+x1)/2, (y0+y1)/2
                app.board[row][col] = app.enzyme            
        
        #else, add the enzyme to the board, and update the enzyme group's locations and times
            else:  
                app.board[row][col] = app.enzyme
                app.enzyme.times.append(0)
                app.enzyme.locations.append((event.x, event.y))
                
                #if the enzyme is dna polymerase, then start its "time left on the board"
                if isinstance(app.enzyme, Enzyme) and app.enzyme.name == "DNA Polymerase":
                    app.enzyme.left.append(40)
    #app.dragCard = False

#returns back the index of the card that was clicked in the top bar 
def checkMouseInCard(app, event):
    for enzyme in app.enzymes:
        if isinstance(enzyme, Enzyme):
            if ((event.x >= enzyme.x and event.x <= enzyme.x + app.cardWidth) and
                (event.y >= enzyme.y and event.y <= enzyme.y + app.cardHeight)):
                #print(enzyme.listIndex)
                return enzyme.listIndex
        else:
            if ((event.x >= enzyme[1] and event.x <= enzyme[1] + app.cardWidth) and
                (event.y >= enzyme[2] and event.y <= enzyme[2] + app.cardHeight)):
                return len(app.enzymes) - 1
    return None

#places the atp at the location specified by adding it to the atp list 
def placeATP(app, x, y):
    app.atp.append([x, y])

#takes out the enzyme from the board list by checking which location needs to be removed
def removeEnzymeFromBoard(app, enzyme, index):
    i = 0
    if not isinstance(enzyme, int):
        while i < len(app.boardEnzymes):
            boardEnzyme = app.boardEnzymes[i]
            #print((boardEnzyme[1], boardEnzyme[2]), enzyme.locations[index])
            if ((boardEnzyme[1] == enzyme.locations[index][0]) and 
                (boardEnzyme[2] == enzyme.locations[index][1])):
                app.boardEnzymes.pop(i)
            else:
                i += 1

#makes an empty 2dlist
#retrieved from 112 course website
def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

#multiplies matrices
#retrieved from previous 112 homework (my own code that I submitted that week)
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

#changes the location of the mutation object by 
#changing previous location to 0 and next location to 1
#doesn't move if dna polymerase is there
def addNewMutation(app):
    if app.mutationsPassed < app.setNumberMutations:
        randomTime = random.randrange(0, 1000, 100)
        if app.currentTime % 1000 == randomTime:
            row = random.randint(0, app.cols - 1)
            col = 8
            x, y = getIsoCoordinates(app, row, col)
            app.mutations.append(Mutation(app, "Normal Mutation", app.url, app.hitsPerMutation, x, y, row, col))
            app.mutationsPassed += 1

def atpSynthaseFunction(app, enzyme):
    #print("i'm here!'")
    for time in enzyme[0].times:
        if time % 10000 == 1000:
            placeATP(app, enzyme[1], enzyme[2])

def dnaPolyFunction(app, enzyme):
    for i in range(len(enzyme[0].left)):
        x, y = enzyme[0].locations[i][0], enzyme[0].locations[i][1]
        row, col = find_row_col(app, x, y)
        #print(row, col)
        if app.board[row][col - 1] == 1:
            enzyme[0].left[i] -= 1
        #print(enzyme[0].left)
        if enzyme[0].left[i] <= 0:
            #print("removing enzyme!")
            removeEnzymeFromBoard(app, enzyme[0], i)
            app.board[row][col] = 0
        elif enzyme[0].left[i] <= 20:
            enzyme[0].setImage(app, i, 'images/dna polymerase broken.png')

def caspaseFunction(app, enzyme):    
    for i in range(len(enzyme[0].times)):
        x, y = enzyme[0].locations[i][0], enzyme[0].locations[i][1]
        time = enzyme[0].times[i]
        if app.currentTime % 3000 == 0:
            app.caspaseShoot.append((x, y))

def getSlope(app, row, col):
    x0, y0 = 7.5, col + 0.5
    x1, y1 = row - 0.5, col + 0.5
    
    dx, dy = (y1 - y0), (x1 - x0)
    return dx, dy

def starShooterFunction(app):

    directions = [(0, -1), (0, +1), (-1, 0), (+1, 0), (+1, -1), (+1, +1), (-1, -1), (-1, +1)]
    if len(app.starShoot) > 0:
        for i in range(len(app.starShoot)):
            dx, dy = getSlope(app, app.starShootRowCol[0], app.starShootRowCol[1])
            app.starShoot[i] = (app.starShoot[i][0] + dx*10*directions[i][0], app.starShoot[i][1] - dy*10*directions[i][1])
            # just know that this way, if one collides, then the other ones will switch direction...
                
def shootAtMutation(app):
    i = 0
    while i < (len(app.caspaseShoot)):
        if app.caspaseShoot[i][0] <= app.width and app.caspaseShoot[i][1] >= 0:
            app.caspaseShoot[i] = (app.caspaseShoot[i][0], app.caspaseShoot[i][1] - 20)
            i += 1
        else:
            app.caspaseShoot.pop(i)

    # i = 0
    # while i < (len(app.starShoot)):
    #     if 0 <= app.starShoot[i][0] <= app.width and 0 <= app.starShoot[i][1] <= app.height:
    #         i += 1
    #     else:
    #         app.starShoot.pop(i)
            
    removeMutations = []
    for mutation in app.mutations:
        i = 0
        while i < (len(app.caspaseShoot)):
            if len(app.caspaseShoot) > 0 and checkCaspaseCollision(app, app.caspaseShoot[i][0], app.caspaseShoot[i][1], 
                                    mutation):
                app.caspaseShoot.pop(i)
                #print("mutation was hit!!")
                mutation.getHit()
                app.hits += 1 
                app.progress = int(100*app.hits/app.totalHits)
            else:
                i += 1
        
        i = 0
        while i < (len(app.starShoot)):
            if checkCaspaseCollision(app, app.starShoot[i][0], app.starShoot[i][1], 
                                    mutation):
                app.starShoot.pop(i)
                #print("mutation was hit!!")
                mutation.getHit()
                app.hits += 1
                app.progress = int(100*app.hits/app.totalHits)
            else:
                i += 1
    for mutation in removeMutations:
        app.mutations.remove(mutation)
        
            
#update the atp location after each call to move it
def updateATPLocation(app):
    for atp in app.atp:
        if atp[1] <= app.width:
            atp[1] += 1

def checkEnoughATP(app, enzyme):
        if isinstance(enzyme, Enzyme):
            if app.collectedATP >= enzyme.pointValue:
                enzyme.notEnoughATP = False
            else: enzyme.notEnoughATP = True

#add an atp after a certain interval
def addNewATP(app):
    if app.currentTime % 8000 == 200:
        randomx = random.randint(0, app.width)
        randomy = 400
        placeATP(app, randomx, randomy)

def updateMutationLocation(app, mutation, currentX, currentY):
    #print("updating!", app.board)
    if mutation.col < (app.cols - 1):
        if mutation.hits <= 0:
            app.board[mutation.row][mutation.col] = 0
            app.mutations.remove(mutation)
        elif (isinstance(app.board[currentX][currentY], Enzyme)):
            if app.board[currentX][currentY].name == "DNA Polymerase":
                app.board[currentX + 1][currentY] = mutation
        else:
            app.board[currentX][currentY] = mutation
            if currentX < 8:
                app.board[currentX + 1][currentY] = 0
            mutation.row -= 1
            position = getIsoCoordinates(app, mutation.row, mutation.col)
            mutation.x = position[0]
            mutation.y = position[1]
          
def checkWin(app, currentTime):
    if app.winTime == None:
        if app.setNumberMutations == app.mutationsKilled:
            app.winTime = currentTime

def checkLose(app):
    for tile in range(len(app.board[0])):
        if isinstance(app.board[0][tile], Mutation):
            app.mode = 'loseMode'

def checkCaspaseCollision(app, caspaseX, caspaseY, mutation):
    (width, height) = mutation.image.size
    x, y = caspaseX, caspaseY
    mx, my = getIsoCoordinates(app, mutation.row, mutation.col)
    return ((mx - width//4 <= x <= mx + width//4) and 
        (my + height//4 >= y >= my - height//4))


#big function for drawing the main board
def drawBoard(app, canvas):
    #creates the background oval
    canvas.create_oval(0, app.height/app.cols, app.width, 
                        app.height - 20, 
                        fill = '#9CD3DB', outline = '#a9edff')
    
    #loops through each row and col in the board, 
    # gets x and y coordinates, and gets isometric coordinates from there
    
    for row in range(app.rows):
        for col in range(app.cols):
            color = '#9CD3DB'
            x0 = row
            y0 = col
            x1 = (row + 1)
            y1 = (col + 1)
            x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2)
            placeTile(app, x0, y0, x1, y1, canvas, color)
    
    for row in range(app.rows):
        for col in range(app.cols):
            x0 = row
            y0 = col
            x1 = (row + 1)
            y1 = (col + 1)
            x, y = getIsoCoordinates(app, (x0+x1)/2, (y0+y1)/2)
        
            #if the enzyme is the shovel, then remove whatever enzyme was there
            if isinstance(app.board[row][col], list):
                color = '#9CD3DB'
                placeTile(app, x0, y0, x1, y1, canvas, color)
            
            #if the value on the board here is 1, then place the mutation there
            elif isinstance(app.board[row][col], Mutation):
                if app.board[row][col].hits > 0:
                    placeTile(app, x0, y0, x1, y1, canvas, '#9CD3DB')
                    sprite = app.sprites[app.spriteCounter]
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(sprite))                
                else:
                    placeTile(app, x0, y0, x1, y1, canvas, '#9CD3DB')
            #if the value on the board here is 0, then place the empty tile there
            
            #for all other enzymes, place the image of the enzyme
            elif isinstance(app.board[row][col], Enzyme):
                placeTile(app, x0, y0, x1, y1, canvas, color)
                canvas.create_image(x, y, image=ImageTk.PhotoImage(app.board[row][col].image))                

#draws the atp image for every atp in the list
def drawATP(app, canvas):
    for atp in app.atp:
        canvas.create_image(atp[0], atp[1], image=ImageTk.PhotoImage(app.atpImage))

#draws the atp image and amount in the top bar
def drawCollectedATP(app, canvas):
    canvas.create_image(50, 50, image=ImageTk.PhotoImage(app.atpImage))
    font = 'Sans 18'
    canvas.create_text(45, 50 + 40, text= str(app.collectedATP), 
                       font=font, anchor = 'center')

#draws the ball for caspase's shots
def drawShots(app, canvas):
    print(app.caspaseShoot)
    for ball in app.caspaseShoot:
        x, y = ball[0], ball[1]
        canvas.create_image(x, y, image=ImageTk.PhotoImage(app.ballImage))
    for starBall in app.starShoot:
        x, y = starBall[0], starBall[1]
        canvas.create_image(x, y, image=ImageTk.PhotoImage(app.ballImage))

#draws the main message box for text input (placeholder for now)
def drawMessageBox(app, canvas):
    x0 = app.width - app.messageBoxWidth - 30
    y0 = 20
    x1 = x0 + app.messageBoxWidth
    y1 = 5 + app.messageBoxHeight
    round_rectangle(canvas, x0, y0, x1, y1, fill = '#BB8D6F')
    canvas.create_rectangle(x0 + 10, y0 + 10, x1 - 10, y1 - 30, fill = '#f7f3f1')
    canvas.create_text(x0 + 10, y1 - 15, text = "MESSAGE BOX", anchor = 'w')

#creates a rectangle with rounded corners
#retrieved from 
#https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners

def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, 
              x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, 
              x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, 
              x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, 
              x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)

#this function draws the entire top bar, calling the smaller functions to help
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
    
#draws the card for the enzyme
def drawenzymeCard(enzyme, app, canvas, x, y):
    
    #if the card is a shovel, then just draw the card where we want
    if not isinstance(enzyme, Enzyme):        
        color = '#f7f3f1'
        round_rectangle(canvas, x + 5, y, x + app.cardWidth, y + app.cardHeight, r = 10, fill = color)
        font = 'Sans 10'
        canvas.create_image(x + app.cardWidth/2, y + app.cardHeight/2 - 10, image=ImageTk.PhotoImage(app.shovelImage))
        canvas.create_text(x + app.cardWidth/2, y + app.cardHeight - 25, text= "shovel", 
                        font=font, anchor = 'center')
    
    #if the card is an actual enzyme, then draw the card where we want
    #color changes based on if all the enzymes in that group are used or if there isn't enough atp to use the card
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

#gets the coordinates at each corner of the square
#uses isometric function to calculate isometric coordinates
#rotates the tile if needed
#creates a polygon with these 4 points 

def checkLogOutButton(app, event):
    if ((app.width - 70 <= event.x <= app.width - 5) and 
        (app.height - 30 <= event.y <= app.height - 5)):
        app.mode = 'homeScreenMode'

def drawLogOutButton(app, canvas):
    round_rectangle(canvas, app.width - 70, app.height - 30, app.width - 5, app.height - 5, fill = '#69C6AF')
    canvas.create_text(app.width - 38, app.height - 18, text = "Log Out", anchor = 'center', fill = 'black')

def placeTile(app, x0, y0, x1, y1, canvas, color):

    isox0, isoy0 = getIsoCoordinates(app, x0, y0)
    
    isox1, isoy1 = getIsoCoordinates(app, x1, y0)
    
    isox2, isoy2 = getIsoCoordinates(app, x1, y1)
    
    isox3, isoy3 = getIsoCoordinates(app, x0, y1)
    
    canvas.create_polygon(isox0, isoy0, isox1, isoy1,
                          isox2, isoy2, isox3, isoy3, 
                          fill = color, outline = '#a9edff')

def findXYBounds(isox0, isoy0, isox1, isoy1, isox2, isoy2, isox3, isoy3):
    maxX = max([isox0, isox1, isox2, isox3])
    minX = min([isox0, isox1, isox2, isox3])
    maxY = max([isoy0, isoy1, isoy2, isoy3])
    minY = min([isoy0, isoy1, isoy2, isoy3])
    
    return maxX, minX, maxY, minY



#gets the isometric coordinates by performing a system of equations
#I actually did not adapt this from anywhere
#I manually drew out a board and came up with my own formula
#I have a page in my notebook where I did this for proof, if needed :)
def getIsoCoordinates(app, x, y):
    point = [[x], [y], [1]]
    point = matrix_multiplication(app.translation, point)
    
    
    
    new_point = matrix_multiplication(app.rotation_z, point)
    new_point = matrix_multiplication(app.rotation_x, new_point)
    new_point = matrix_multiplication(app.translation_back, new_point)

        
    z_new = new_point[2][0]
    #print(z_new)

    x_new = new_point[0][0]/z_new
    y_new = new_point[1][0]/z_new


    return x_new*50 + 400, y_new*50 + 100

#does the reverse of getIsoCoordinates
#i solved the system of equations and rewrote the new variable formulas
#but i will change this when I get rotation working
def getCartesianCoordinates(app, x_grid, y_grid):
    x = (6*x_grid + app.cols*y_grid - app.height - 3*app.width)/5
    y = (app.cols*y_grid - 6*x_grid - app.height + 3*app.width)/5
    return(x, y)

runApp(width=1200, height=1200)