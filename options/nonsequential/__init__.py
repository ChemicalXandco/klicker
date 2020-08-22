from options import getOptions, Base


class NonsequentialBase(Base):
    '''
    Basic construct for nonsequential option widgets
    '''
    def __init__(self, *args):
        super().__init__(*args)

    def start(self):
        return

    def stop(self):
        return

    def update(self):
        return


movable = False
optDict, optList = getOptions(__path__)
