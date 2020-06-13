class Base:
    '''
    Basic construct for all option widgets
    '''
    def __init__(self, parent, spacing, save, logger, numbers, recordings):
        self.parent = parent
        self.spacing = spacing
        self.save = save
        self.logger = logger
        self.numbers = numbers
        self.recordings = recordings

    @property
    def args(self):
        return [
            self.save,
            self.logger,
            self.numbers,
            self.recordings
        ]