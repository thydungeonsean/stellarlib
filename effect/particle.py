

class Particle(object):

    def __init__(self, collection, point):

        self.collection = collection
        self.point = point

        self.tick = 0

    def increment_tick(self):

        self.tick += 1

    def end(self):

        self.collection.remove(self)
