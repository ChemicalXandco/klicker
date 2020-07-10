from options import getOptions, Base


class BooleanBase(Base):
    '''
    Basic construct for boolean option widgets
    '''
    def __init__(self, *args):
        super().__init__(*args)

    def evaluate(self):
        raise NotImplementedError()


optDict, optList = getOptions(__path__)
