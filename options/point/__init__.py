from options import getOptions, Base


class PointBase(Base):
    '''
    Basic construct for sequential option widgets
    '''
    def __init__(self, *args):
        super().__init__(*args)

    def get(self):
        raise NotImplementedError()


movable = False
optDict, optList = getOptions(__path__)
