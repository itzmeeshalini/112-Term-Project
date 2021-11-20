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
        
        self.available = self.count > 0
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
        self.count -= 1
        self.available = self.count > 0
        
    #updates the time for each enzyme on the board
    def updateTime(self):
        for i in range(len(self.times)):
            self.times[i] += 100
    
    #changes the image for the object if it needs to be changed
    def setImage(self, app, i, imgUrl):
        image = app.loadImage(imgUrl)
        self.images[i] = app.scaleImage(image, self.scale)