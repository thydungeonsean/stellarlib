

class AnimationMap(object):

    def __init__(self, (w, h)):

        self.w = w
        self.h = h

        self.map = [[0 for my in range(self.h)] for mx in range(self.w)]

