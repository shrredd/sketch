class MSImageCollection(object):
    def __init__(self, images):
        self._images = images

    @property
    def images(self):
        # <list>
        return self._images
