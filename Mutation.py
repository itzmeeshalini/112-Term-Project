class Mutation(object):
    
    def __init__(self, app, name, imgUrl, hits, x, y):
        self.name = name
        self.imgUrl = imgUrl
        self.image = app.loadImage(imgUrl)
        self.image = app.scaleImage(self.image, 1/8)
        self.hits = hits
        self.x = x
        self.y = y
        
    
    # def getHit(self):
    #     change number of hits left
    #     change image if hits is in a certain region
    #     self.hits -= 1
    #     pass