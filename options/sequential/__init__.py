from options import getOptions, Base


class SequentialBase(Base):
    '''
    Basic construct for sequential option widgets
    '''
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        raise NotImplementedError()


movable = True
optDict, optList = getOptions(__path__)
