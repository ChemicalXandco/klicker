class Base:
    '''
    Basic construct for all option widgets
    '''
    def __init__(self, parent, spacing, logger, numbers):
        self.parent = parent
        self.spacing = spacing
        self.logger = logger
        self.numbers = numbers

    @property
    def args(self):
        return [
            self.logger,
            self.numbers
        ]